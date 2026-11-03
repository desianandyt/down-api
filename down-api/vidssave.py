import os
import base64
import json
import logging
import re
import time
import urllib.parse
from typing import Any, Dict, List, Optional
from Crypto.Cipher import AES
import requests
from proxy_manager import proxy_pool

logger = logging.getLogger("vidssave")

DEFAULT_KEYS = ["4c9b7d2e" * 3 + "4c9b7d21", "rz18efAXUbdiaO7k"]
DEFAULT_AUTH_CODE = "4c9b7d21"
DEFAULT_DOMAIN = "api-ak.vidssave.com"
DEFAULT_AUTH_QUERY = "20250901majwlqo"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://vidssave.com",
    "Referer": "https://vidssave.com/",
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site"
}

ENDPOINTS = [
    {
        "name": "test-api",
        "api_base": "https://test-api.vidssave.com/vapi/contentsite_api",
        "sse_base": "https://test-api.vidssave.com/vsse/contentsite_api"
    },
    {
        "name": "prod-api",
        "api_base": "https://api.vidssave.com/api/contentsite_api",
        "sse_base": "https://api.vidssave.com/sse/contentsite_api"
    }
]


class CredentialsManager:
    def __init__(self):
        self.auth_code = DEFAULT_AUTH_CODE
        self.auth_query = DEFAULT_AUTH_QUERY
        self.domain = DEFAULT_DOMAIN
        self.keys = list(DEFAULT_KEYS)
        self.last_refresh = 0

    def refresh(self, force: bool = False):
        """Scrapes vidssave.com frontend to extract new credentials dynamically."""
        now = time.time()
        # Cooldown of 60 seconds unless forced
        if not force and (now - self.last_refresh < 60):
            logger.info("Credentials refresh skipped (cooldown active)")
            return

        logger.info("Fetching fresh credentials from vidssave.com...")
        try:
            r = requests.get("https://vidssave.com/", headers=DEFAULT_HEADERS, proxies=proxy_pool.get_dict(), timeout=10)
            if r.status_code != 200:
                logger.warning(f"Could not load homepage: HTTP {r.status_code}")
                return

            chunks = re.findall(r'https://res\.vidssave\.com/vidssave-com/_next/static/chunks/[^\s\"\'\`]+\.js', r.text)
            new_keys = list(DEFAULT_KEYS)

            for chunk_url in chunks:
                if any(k in chunk_url for k in ["1074", "6215", "layout", "page", "app"]):
                    try:
                        js_text = requests.get(chunk_url, headers=DEFAULT_HEADERS, timeout=6).text

                        # 1. auth code
                        m_auth = re.search(r'auth:[\"\'\`]([a-zA-Z0-9_\-]+)[\"\'\`]', js_text)
                        if m_auth:
                            self.auth_code = m_auth.group(1)

                        # 2. auth query
                        m_query = re.search(r'auth=([a-zA-Z0-9_\-]+)', js_text)
                        if m_query:
                            self.auth_query = m_query.group(1)

                        # 3. domain
                        m_domain = re.search(r'VIDEODOWNLOAD:[\"\'\`]([^\"\'\`]+)[\"\'\`]', js_text)
                        if m_domain:
                            self.domain = m_domain.group(1)

                        # 4. aes keys
                        if "repeat(3)" in js_text:
                            m_rep = re.search(r'[\"\'\`](\w+)[\"\'\`]\.repeat\(3\)\.concat\([\"\'\`](\w+)[\"\'\`]\)', js_text)
                            if m_rep:
                                k1 = m_rep.group(1) * 3 + m_rep.group(2)
                                if k1 not in new_keys:
                                    new_keys.insert(0, k1)
                    except Exception as e:
                        logger.debug(f"Error inspecting chunk {chunk_url}: {e}")

            self.keys = new_keys
            self.last_refresh = time.time()
            logger.info(f"Credentials updated: auth={self.auth_code}, domain={self.domain}")
        except Exception as e:
            logger.error(f"Failed to refresh credentials: {e}")


creds_manager = CredentialsManager()
AUTH_CODE = creds_manager.auth_code
API_BASE = "https://test-api.vidssave.com/vapi/contentsite_api"
DOMAIN = creds_manager.domain


def decrypt_payload(ciphertext_b64: str) -> Any:
    """Decrypts AES-CBC encrypted response from vidssave backend."""
    raw = base64.b64decode(ciphertext_b64)
    last_err = None
    for key_str in creds_manager.keys:
        try:
            key = key_str.encode("utf-8")
            iv = key[:16]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(raw).rstrip(b"\x00")
            text = decrypted.decode("utf-8")
            try:
                return json.loads(text)
            except Exception:
                return text
        except Exception as e:
            last_err = e
    raise ValueError(f"AES decryption failed: {last_err}")


def _execute_parse(url: str) -> Dict[str, Any]:
    payload = {
        "hostname": "vidssave.com",
        "auth": creds_manager.auth_code,
        "domain": creds_manager.domain,
        "origin": "source",
        "link": url
    }

    last_error = None
    proxy_attempts = [proxy_pool.get_dict()]
    fallback_p = proxy_pool.get_fallback_dict()
    if fallback_p and fallback_p != proxy_attempts[0]:
        proxy_attempts.append(fallback_p)

    # 1. Try Direct first. 2. If analyze_risk or blocked on datacenter, retry with free fallback proxy.
    for proxies in proxy_attempts:
        for ep in ENDPOINTS:
            parse_url = f"{ep['api_base']}/media/parse"
            try:
                resp = requests.post(parse_url, data=payload, headers=DEFAULT_HEADERS, proxies=proxies, timeout=12)
                if resp.status_code != 200:
                    continue
                res_json = resp.json()
                if res_json.get("status") == 1:
                    data_field = res_json.get("data")
                    if isinstance(data_field, str):
                        return decrypt_payload(data_field)
                    return data_field
                else:
                    last_error = res_json.get("status_code") or res_json.get("msg") or "parse_failed"
                    if last_error == "analyze_risk":
                        break
            except Exception as e:
                last_error = str(e)

    raise ValueError(f"VidsSave API error: {last_error}")


def parse_media(url: str) -> Dict[str, Any]:
    """
    Parses media link. If it fails, checks if credentials need refresh, else raises error.
    """
    try:
        return _execute_parse(url)
    except Exception as e:
        err_str = str(e)
        logger.warning(f"VidsSave parse error ({err_str}), refreshing creds...")
        creds_manager.refresh()
        return _execute_parse(url)


def _execute_download(resource_content: str, output_format: Optional[str] = None, timeout: int = 25) -> Dict[str, Any]:
    payload = {
        "hostname": "vidssave.com",
        "auth": creds_manager.auth_code,
        "domain": creds_manager.domain,
        "request": resource_content,
        "no_encrypt": 1
    }
    if output_format:
        payload["output"] = output_format

    proxy_attempts = [proxy_pool.get_dict()]
    fallback_p = proxy_pool.get_fallback_dict()
    if fallback_p and fallback_p != proxy_attempts[0]:
        proxy_attempts.append(fallback_p)

    for proxies in proxy_attempts:
        for ep in ENDPOINTS:
            download_url = f"{ep['api_base']}/media/download"
            try:
                resp = requests.post(download_url, data=payload, headers=DEFAULT_HEADERS, proxies=proxies, timeout=12)
                if resp.status_code != 200:
                    continue
                res_json = resp.json()
                if res_json.get("status") != 1:
                    continue

                raw_data = res_json.get("data")
                data = decrypt_payload(raw_data) if isinstance(raw_data, str) else raw_data
                task_id = data.get("task_id")
                if not task_id:
                    continue

                # Listen to SSE download_query
                task_id_enc = urllib.parse.quote(task_id)
                sse_url = (
                    f"{ep['sse_base']}/media/download_query"
                    f"?auth={creds_manager.auth_query}&domain={creds_manager.domain}&task_id={task_id_enc}"
                    f"&download_domain=vidssave.com&origin=content_site"
                )

                sse_headers = {
                    "Accept": "text/event-stream",
                    "User-Agent": DEFAULT_HEADERS["User-Agent"],
                    "Origin": DEFAULT_HEADERS["Origin"],
                    "Referer": DEFAULT_HEADERS["Referer"]
                }

                with requests.get(sse_url, headers=sse_headers, proxies=proxies, stream=True, timeout=timeout) as sse_resp:
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
                                    try:
                                        head_resp = requests.get(
                                            redirect_link,
                                            headers={"User-Agent": DEFAULT_HEADERS["User-Agent"]},
                                            proxies=proxies,
                                            allow_redirects=False,
                                            timeout=6
                                        )
                                        final_link = head_resp.headers.get("Location") or redirect_link
                                    except Exception:
                                        final_link = redirect_link

                                    event_data["direct_url"] = final_link
                                    return event_data
                                elif event_data.get("status") == "failed":
                                    raise ValueError(f"Conversion task failed: {event_data}")
                            except json.JSONDecodeError:
                                pass
            except Exception as e:
                logger.warning(f"Download endpoint {ep['api_base']} error: {e}")
                continue

    raise TimeoutError("SSE connection ended without download_link")


def resolve_download_link(resource_content: str, output_format: Optional[str] = None, timeout: int = 25) -> Dict[str, Any]:
    return _execute_download(resource_content, output_format=output_format, timeout=timeout)
