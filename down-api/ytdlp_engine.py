import os
import logging
from typing import Any, Dict, Optional
import yt_dlp

from proxy_manager import proxy_pool

logger = logging.getLogger("ytdlp_engine")


def get_ytdlp_info(url: str) -> Dict[str, Any]:
    """Extracts video metadata and formats using yt-dlp with datacenter-safe clients (Zero-Proxy ready)."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "socket_timeout": 15,
        "geo_bypass": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        },
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "android_creator"]
            }
        }
    }
    proxy = proxy_pool.get_proxy()
    if proxy:
        ydl_opts["proxy"] = proxy

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return ydl.sanitize_info(info)
    except Exception as e:
        fallback_proxy = proxy_pool.get_fallback_proxy()
        if fallback_proxy and fallback_proxy != proxy:
            logger.info(f"yt-dlp direct failed: {e}. Retrying with free public fallback proxy...")
            ydl_opts["proxy"] = fallback_proxy
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return ydl.sanitize_info(info)
        raise


def get_ytdlp_direct_link(url: str, media_type: str = "video", quality: Optional[str] = None) -> Dict[str, Any]:
    """Resolves direct stream URL using yt-dlp."""
    info = get_ytdlp_info(url)
    formats = info.get("formats", [])

    if media_type == "audio":
        audio_formats = [
            f for f in formats
            if f.get("acodec") and f.get("acodec") != "none" and f.get("ext") not in ("mhtml", "jpg", "jpeg", "webp")
        ]
        # Prefer pure audio formats first
        pure_audio = [f for f in audio_formats if f.get("vcodec") == "none"]
        pool = pure_audio if pure_audio else audio_formats
        best = max(pool, key=lambda x: x.get("abr") or 0) if pool else None
        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "direct_url": best.get("url") if best else None,
            "format": best.get("ext") if best else "mp3",
            "filesize": best.get("filesize") or best.get("filesize_approx") if best else None,
            "quality": f"{int(best.get('abr'))}kbps" if best and best.get("abr") else "128kbps"
        }
    else:
        video_formats = [f for f in formats if f.get("vcodec") != "none"]
        best = None
        if quality and quality.lower() != "best":
            q_clean = quality.lower().replace("p", "")
            matched = [f for f in video_formats if str(f.get("height")) == q_clean]
            best = matched[-1] if matched else None

        if not best and video_formats:
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
