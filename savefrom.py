import os
import json
import logging
import subprocess
import shutil
import tempfile
import requests
import urllib3
from typing import Any, Dict, List, Optional
from proxy_manager import proxy_pool

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger("savefrom")

EXTRACTOR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "savefrom_extractor.js")


import threading

def _ensure_jsdom():
    """Ensures jsdom is installed in /tmp if not found."""
    if not shutil.which("node") or not shutil.which("npm"):
        return
    try:
        # Fast check if already installed
        if os.path.exists("/tmp/node_modules/jsdom"):
            return
        r = subprocess.run(["node", "-e", "require('jsdom')"], capture_output=True, timeout=5)
        if r.returncode == 0:
            return
        logger.info("Auto-installing jsdom in /tmp for SaveFrom engine...")
        subprocess.run(["npm", "install", "--prefix", "/tmp", "jsdom", "--no-save"], capture_output=True, timeout=90)
        logger.info("jsdom installed successfully in /tmp!")
    except Exception as e:
        logger.warning(f"Error checking/installing jsdom: {e}")

# Run in background thread so it doesn't block server startup
threading.Thread(target=_ensure_jsdom, daemon=True).start()


def _sign_with_node(url: str, msec: Optional[float] = None) -> Dict[str, Any]:
    """Generates signed payload using savefrom_extractor.js."""
    node_bin = shutil.which("node") or "node"
    cmd = [node_bin, EXTRACTOR_PATH, "sign", url]
    if msec:
        cmd.append(str(msec))
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
    if proc.returncode != 0:
        raise RuntimeError(f"Signer failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return json.loads(proc.stdout.strip())


def _decrypt_with_node(js_content: str) -> Dict[str, Any]:
    """Decrypts JS worker response using savefrom_extractor.js."""
    node_bin = shutil.which("node") or "node"
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as tf:
        tf.write(js_content)
        tf_name = tf.name

    try:
        cmd = [node_bin, EXTRACTOR_PATH, "decrypt", tf_name]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            raise RuntimeError(f"Decryptor failed: {proc.stderr.strip() or proc.stdout.strip()}")
        return json.loads(proc.stdout.strip())
    finally:
        if os.path.exists(tf_name):
            try:
                os.remove(tf_name)
            except Exception:
                pass


def extract_raw(url: str) -> Dict[str, Any]:
    """Extracts raw metadata from SaveFrom utilizing proxies to avoid datacenter Cloudflare blocks."""
    if not os.path.exists(EXTRACTOR_PATH):
        raise FileNotFoundError(f"SaveFrom extractor script not found at {EXTRACTOR_PATH}")

    # 1. Fetch live msec
    msec = None
    proxies = proxy_pool.get_dict()
    try:
        msec_res = requests.get("https://en1.savefrom.net/msec", headers={"User-Agent": "Mozilla/5.0"}, proxies=proxies, timeout=6, verify=False)
        if msec_res.status_code == 200:
            msec = msec_res.json().get("msec")
    except Exception as e:
        logger.debug(f"msec fetch error: {e}")

    # 2. Sign request
    signed = _sign_with_node(url, msec=msec)

    payload = {
        "sf_url": signed["url"],
        "new": "2",
        "lang": "en",
        "app": "",
        "sf-nomad": "1",
        "ts": signed["ts"],
        "_ts": signed["_ts"],
        "_tsc": signed["_tsc"],
        "_s": signed["_s"],
        "_x": signed["_x"]
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://en1.savefrom.net",
        "Referer": "https://en1.savefrom.net/19wr/",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # 3. Post to worker (Zero-Proxy Direct mode by default, or with free fallback proxy)
    worker_url = "https://worker.savefrom.net/savefrom.php"
    last_err = None

    proxy_attempts = [proxy_pool.get_dict()]
    fallback_p = proxy_pool.get_fallback_dict()
    if fallback_p and fallback_p != proxy_attempts[0]:
        proxy_attempts.append(fallback_p)

    for attempt, cur_proxies in enumerate(proxy_attempts):
        try:
            resp = requests.post(worker_url, data=payload, headers=headers, proxies=cur_proxies, timeout=12, verify=False)
            text = resp.text
            if "/*js-response*/" in text:
                # Successfully received encrypted JS response
                return _decrypt_with_node(text)
            elif "<!DOCTYPE" in text or "<html" in text:
                logger.warning(f"SaveFrom attempt {attempt+1} got HTML challenge. Retrying with fallback proxy...")
                continue
            else:
                last_err = f"Unexpected response (status {resp.status_code}): {text[:200]}"
        except Exception as e:
            logger.warning(f"SaveFrom worker request error on attempt {attempt+1}: {e}")
            last_err = str(e)

    # 4. Fallback to direct Node execution if proxy attempts were exhausted
    logger.info("Falling back to direct node execution for SaveFrom...")
    node_bin = shutil.which("node") or "node"
    proc = subprocess.run([node_bin, EXTRACTOR_PATH, url], capture_output=True, text=True, timeout=20)
    if proc.returncode == 0:
        return json.loads(proc.stdout.strip())

    raise RuntimeError(f"SaveFrom extraction failed: {last_err or proc.stderr.strip() or proc.stdout.strip()}")


def parse_media(url: str) -> Dict[str, Any]:
    """Parses video/audio metadata and available streams into standard Down-API format."""
    raw = extract_raw(url)
    meta = raw.get("meta", {})
    title = meta.get("title") or "video"
    duration = meta.get("duration")
    thumb = raw.get("thumb")
    video_id = raw.get("id")

    urls = raw.get("url", [])
    videos: List[Dict[str, Any]] = []
    audios: List[Dict[str, Any]] = []

    seen_v = set()
    seen_a = set()

    for item in urls:
        stream_url = item.get("url")
        if not stream_url or stream_url.startswith("#"):
            continue

        raw_type = str(item.get("type", "")).lower()
        ext = (item.get("ext") or "mp4").lower()
        quality_str = str(item.get("quality") or "")
        filesize = item.get("filesize")
        is_audio = item.get("audio") is True or "audio" in raw_type or ext in ("m4a", "opus", "mp3", "aac", "ogg")
        no_audio = item.get("no_audio") is True

        if is_audio:
            q_label = f"{quality_str}kbps" if quality_str.isdigit() else (quality_str or "audio")
            key = (q_label, ext)
            if key not in seen_a:
                seen_a.add(key)
                audios.append({
                    "quality": q_label,
                    "format": ext,
                    "size": filesize,
                    "download_url": stream_url
                })
        else:
            q_label = f"{quality_str}p" if quality_str.isdigit() else (quality_str or "video")
            key = (q_label, ext, no_audio)
            if key not in seen_v:
                seen_v.add(key)
                videos.append({
                    "quality": q_label,
                    "format": ext,
                    "size": filesize,
                    "has_audio": not no_audio,
                    "download_url": stream_url
                })

    return {
        "status": "success",
        "engine": "savefrom",
        "id": video_id,
        "title": title,
        "duration": duration,
        "thumbnail": thumb,
        "videos": videos,
        "audios": audios
    }


def get_direct_download(url: str, media_type: str = "video", quality: str = "best", info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Resolves the best direct download link from SaveFrom."""
    if not info:
        info = parse_media(url)
    media_type = (media_type or "video").lower()
    quality = (quality or "best").lower()

    if media_type == "audio":
        audios = info.get("audios", [])
        if not audios:
            raise ValueError("No audio streams found on SaveFrom")

        def parse_bitrate(a):
            q = a.get("quality", "").lower().replace("kbps", "")
            try:
                return int(q)
            except ValueError:
                return 0

        selected = max(audios, key=parse_bitrate)
        return {
            "status": "success",
            "engine": "savefrom",
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "type": "audio",
            "quality": selected.get("quality"),
            "format": selected.get("format"),
            "filesize": selected.get("size"),
            "download_url": selected["download_url"]
        }
    else:
        videos = info.get("videos", [])
        if not videos:
            raise ValueError("No video streams found on SaveFrom")

        with_audio = [v for v in videos if v.get("has_audio")]
        pool = with_audio if with_audio else videos

        selected = None
        if quality != "best":
            q_clean = quality.lower().replace("p", "")
            matched = [v for v in pool if v.get("quality", "").lower().replace("p", "") == q_clean]
            if not matched:
                matched = [v for v in videos if v.get("quality", "").lower().replace("p", "") == q_clean]
            if matched:
                selected = matched[0]

        if not selected:
            def parse_res(v):
                q = v.get("quality", "").lower().replace("p", "")
                try:
                    return int(q)
                except ValueError:
                    return 0

            selected = max(pool, key=parse_res)

        return {
            "status": "success",
            "engine": "savefrom",
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "type": "video",
            "quality": selected.get("quality"),
            "format": selected.get("format"),
            "filesize": selected.get("size"),
            "download_url": selected["download_url"]
        }
