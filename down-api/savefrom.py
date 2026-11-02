import os
import json
import logging
import subprocess
import shutil
from typing import Any, Dict, List, Optional

logger = logging.getLogger("savefrom")

EXTRACTOR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "savefrom_extractor.js")


def _ensure_jsdom():
    """Ensures jsdom dependency is available if node is installed."""
    if not shutil.which("node"):
        logger.warning("Node.js is not found on PATH. SaveFrom engine requires Node.js.")
        return False
    
    test_cmd = ["node", "-e", "try{require('jsdom')}catch(e){try{require('/tmp/node_modules/jsdom')}catch(e2){try{require('/data/data/com.termux/files/usr/lib/node_modules/jsdom')}catch(e3){process.exit(1)}}}"]
    try:
        r = subprocess.run(test_cmd, capture_output=True, timeout=5)
        if r.returncode != 0 and shutil.which("npm"):
            logger.info("Installing jsdom in /tmp for SaveFrom engine...")
            subprocess.run(["npm", "install", "--prefix", "/tmp", "jsdom", "--no-save"], capture_output=True, timeout=60)
    except Exception as e:
        logger.warning(f"Error checking/installing jsdom: {e}")
    return True


_ensure_jsdom()


def extract_raw(url: str) -> Dict[str, Any]:
    """Invokes savefrom_extractor.js via Node.js to fetch raw SaveFrom metadata."""
    if not os.path.exists(EXTRACTOR_PATH):
        raise FileNotFoundError(f"SaveFrom extractor script not found at {EXTRACTOR_PATH}")

    node_bin = shutil.which("node") or "node"
    env = os.environ.copy()
    
    # Try running the node extractor
    cmd = [node_bin, EXTRACTOR_PATH, url]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=25,
            env=env
        )
    except subprocess.TimeoutExpired:
        raise TimeoutError("SaveFrom extraction timed out after 25s")

    if proc.returncode != 0:
        err_msg = proc.stderr.strip() or proc.stdout.strip()
        try:
            parsed_err = json.loads(err_msg)
            if "error" in parsed_err:
                err_msg = parsed_err["error"]
        except Exception:
            pass
        raise RuntimeError(f"SaveFrom extraction failed (exit {proc.returncode}): {err_msg}")

    try:
        data = json.loads(proc.stdout.strip())
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode SaveFrom output as JSON: {proc.stdout[:200]}") from e


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
        
        # Pick highest bitrate
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

        # Prioritize videos with audio
        with_audio = [v for v in videos if v.get("has_audio")]
        pool = with_audio if with_audio else videos

        selected = None
        if quality != "best":
            q_clean = quality.lower().replace("p", "")
            # Try to match quality with audio first
            matched = [v for v in pool if v.get("quality", "").lower().replace("p", "") == q_clean]
            if not matched:
                matched = [v for v in videos if v.get("quality", "").lower().replace("p", "") == q_clean]
            if matched:
                selected = matched[0]

        if not selected:
            # Pick highest height/quality available with audio, or best in pool
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
