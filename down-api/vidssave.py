import base64
import json
import logging
import urllib.parse
from typing import Any, Dict, List, Optional
from Crypto.Cipher import AES
import requests

logger = logging.getLogger("vidssave")

KEYS = ["4c9b7d2e" * 3 + "4c9b7d21", "rz18efAXUbdiaO7k"]
API_BASE = "https://api.vidssave.com"
AUTH_CODE = "4c9b7d21"
DOMAIN = "api-ak.vidssave.com"
AUTH_QUERY = "20250901majwlqo"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://vidssave.com",
    "Referer": "https://vidssave.com/"
}


def decrypt_payload(ciphertext_b64: str) -> Any:
    """Decrypts AES-CBC encrypted response from vidssave backend."""
    raw = base64.b64decode(ciphertext_b64)
    last_err = None
    for key_str in KEYS:
        key = key_str.encode("utf-8")
        iv = key[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(raw).rstrip(b"\x00")
        try:
            text = decrypted.decode("utf-8")
            try:
                return json.loads(text)
            except Exception:
                return text
        except Exception as e:
            last_err = e
    raise ValueError(f"AES decryption failed: {last_err}")


def parse_media(url: str) -> Dict[str, Any]:
    """
    Calls vidssave parse endpoint to retrieve media details and format list.
    """
    parse_url = f"{API_BASE}/api/contentsite_api/media/parse"
    payload = {
        "hostname": "vidssave.com",
        "auth": AUTH_CODE,
        "domain": DOMAIN,
        "origin": "source",
        "link": url
    }
    
    resp = requests.post(parse_url, data=payload, headers=DEFAULT_HEADERS, timeout=20)
    resp.raise_for_status()
    res_json = resp.json()

    if res_json.get("status") != 1:
        error_msg = res_json.get("msg") or res_json.get("message") or "Failed to parse URL"
        raise ValueError(f"VidsSave API error: {error_msg}")

    data_field = res_json.get("data")
    if isinstance(data_field, str):
        data = decrypt_payload(data_field)
    else:
        data = data_field

    return data


def resolve_download_link(resource_content: str, output_format: Optional[str] = None, timeout: int = 35) -> Dict[str, Any]:
    """
    Given a resource_content token, requests media/download and listens
    to SSE stream to resolve the final download URL.
    """
    download_url = f"{API_BASE}/api/contentsite_api/media/download"
    payload = {
        "hostname": "vidssave.com",
        "auth": AUTH_CODE,
        "domain": DOMAIN,
        "request": resource_content,
        "no_encrypt": 1
    }
    if output_format:
        payload["output"] = output_format

    resp = requests.post(download_url, data=payload, headers=DEFAULT_HEADERS, timeout=20)
    resp.raise_for_status()
    res_json = resp.json()

    if res_json.get("status") != 1:
        raise ValueError(f"Download request failed: {res_json}")

    raw_data = res_json.get("data")
    if isinstance(raw_data, str):
        data = decrypt_payload(raw_data)
    else:
        data = raw_data

    task_id = data.get("task_id")
    if not task_id:
        raise ValueError(f"No task_id in response: {data}")

    # Listen to SSE download_query
    task_id_enc = urllib.parse.quote(task_id)
    sse_url = (
        f"{API_BASE}/sse/contentsite_api/media/download_query"
        f"?auth={AUTH_QUERY}&domain={DOMAIN}&task_id={task_id_enc}"
        f"&download_domain=vidssave.com&origin=content_site"
    )

    sse_headers = {
        "Accept": "text/event-stream",
        "User-Agent": DEFAULT_HEADERS["User-Agent"],
        "Origin": DEFAULT_HEADERS["Origin"],
        "Referer": DEFAULT_HEADERS["Referer"]
    }

    with requests.get(sse_url, headers=sse_headers, stream=True, timeout=timeout) as sse_resp:
        for line in sse_resp.iter_lines():
            if not line:
                continue
            line_str = line.decode("utf-8")
            if line_str.startswith("data:"):
                payload_str = line_str[5:].strip()
                try:
                    event_data = json.loads(payload_str)
                    if event_data.get("status") == "success" and event_data.get("download_link"):
                        redirect_link = event_data["download_link"]
                        # Resolve final direct link from redirect
                        try:
                            head_resp = requests.get(
                                redirect_link,
                                headers={"User-Agent": DEFAULT_HEADERS["User-Agent"]},
                                allow_redirects=False,
                                timeout=10
                            )
                            final_link = head_resp.headers.get("Location") or redirect_link
                        except Exception:
                            final_link = redirect_link

                        event_data["direct_url"] = final_link
                        return event_data
                    elif event_data.get("status") == "failed":
                        raise ValueError(f"Conversion/Download task failed: {event_data}")
                except json.JSONDecodeError:
                    pass

    raise TimeoutError("SSE connection ended without download_link")
