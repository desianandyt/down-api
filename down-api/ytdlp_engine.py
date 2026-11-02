import logging
from typing import Any, Dict, Optional
import yt_dlp

logger = logging.getLogger("ytdlp_engine")


def get_ytdlp_info(url: str) -> Dict[str, Any]:
    """Extracts video metadata and formats using yt-dlp."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "socket_timeout": 12,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "ios", "mweb"]
            }
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return ydl.sanitize_info(info)


def get_ytdlp_direct_link(url: str, media_type: str = "video", quality: Optional[str] = None) -> Dict[str, Any]:
    """Resolves direct stream URL using yt-dlp."""
    info = get_ytdlp_info(url)
    formats = info.get("formats", [])

    if media_type == "audio":
        audio_formats = [f for f in formats if f.get("vcodec") == "none" and f.get("acodec") != "none"]
        best = max(audio_formats, key=lambda x: x.get("abr") or 0) if audio_formats else None
        if not best and formats:
            best = formats[0]
        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "direct_url": best.get("url") if best else None,
            "format": best.get("ext") if best else "mp3",
            "filesize": best.get("filesize") or best.get("filesize_approx") if best else None,
            "quality": f"{best.get('abr', 128)}kbps" if best else "standard"
        }
    else:
        video_formats = [f for f in formats if f.get("vcodec") != "none"]
        best = None
        if quality and quality.lower() != "best":
            q_clean = quality.lower().replace("p", "")
            matched = [f for f in video_formats if str(f.get("height")) == q_clean]
            best = matched[-1] if matched else None

        if not best and video_formats:
            # Pick best video format
            best = max(video_formats, key=lambda x: (x.get("height") or 0))

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "direct_url": best.get("url") if best else None,
            "format": best.get("ext") if best else "mp4",
            "filesize": best.get("filesize") or best.get("filesize_approx") if best else None,
            "quality": f"{best.get('height')}p" if best and best.get("height") else "best"
        }
