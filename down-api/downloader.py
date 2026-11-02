#!/usr/bin/env python3
"""
⚡ AnyDownloader CLI — Universal Video & Audio Downloader
Downloads YouTube, Shorts, Instagram Reels, TikTok, Twitter/X, and Facebook videos directly using Down-API.

Usage:
    python downloader.py <video_url> [--type video|audio] [--quality 1080p|720p|360p|best] [--output ./downloads]
"""

import sys
import os
import argparse
import urllib.parse
import requests

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")
FALLBACK_API = "https://down-api-fuye.onrender.com"


def format_size(bytes_num):
    if not bytes_num:
        return "Unknown size"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.1f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.1f} TB"


def get_api_base():
    """Detects whether local server or production Render should be used."""
    try:
        r = requests.get(f"{API_BASE}/api/logs", timeout=1.5)
        if r.status_code == 200:
            return API_BASE
    except Exception:
        pass
    return FALLBACK_API


def download_media(url: str, media_type: str = "video", quality: str = "best", output_dir: str = "./downloads"):
    api = get_api_base()
    print(f"\n⚡ AnyDownloader CLI (connected to: {api})")
    print(f"🔗 Target URL : {url}")
    print(f"🎬 Media Type : {media_type} | Desired Quality: {quality}")
    print("⏳ Resolving direct stream from API (Waterfall: VidsSave -> SaveFrom -> YT-DLP)...")

    # 1. Call /api/download
    download_api_url = f"{api}/api/download?url={urllib.parse.quote(url)}&type={media_type}&quality={quality}"
    try:
        res = requests.get(download_api_url, timeout=60)
        if res.status_code != 200:
            print(f"❌ Error from API (Status {res.status_code}): {res.text}")
            sys.exit(1)
        data = res.json()
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        sys.exit(1)

    title = data.get("title", "download")
    ext = data.get("format", "mp4" if media_type == "video" else "mp3")
    stream_url = data.get("download_url")
    engine = data.get("engine", "Auto")
    resolved_quality = data.get("quality", quality)

    if not stream_url:
        print(f"❌ Failed to extract stream URL: {data}")
        sys.exit(1)

    print(f"✅ Resolved Stream:")
    print(f"   📌 Title    : {title}")
    print(f"   ⚙️ Engine   : {engine}")
    print(f"   📊 Quality  : {resolved_quality} ({ext.upper()})")

    # 2. Download File
    os.makedirs(output_dir, exist_ok=True)
    clean_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip()[:70]
    filename = f"{clean_title}.{ext.lower()}"
    filepath = os.path.join(output_dir, filename)

    print(f"📥 Downloading to: {filepath}")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    with requests.get(stream_url, headers=headers, stream=True, timeout=25) as r:
        r.raise_for_status()
        total_size = int(r.headers.get("Content-Length", 0))
        downloaded = 0

        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 128):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        pct = (downloaded / total_size) * 100
                        bar_len = 30
                        filled = int(bar_len * downloaded // total_size)
                        bar = "█" * filled + "░" * (bar_len - filled)
                        sys.stdout.write(f"\r[{bar}] {pct:.1f}% ({format_size(downloaded)} / {format_size(total_size)})")
                    else:
                        sys.stdout.write(f"\rDownloading: {format_size(downloaded)} received...")
                    sys.stdout.flush()

    print(f"\n🎉 Download Completed Successfully! Saved at: {filepath}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="⚡ AnyDownloader — Universal Video & Audio Downloader CLI")
    parser.add_argument("url", help="Video URL (YouTube, Shorts, Instagram Reels, TikTok, Twitter, Facebook)")
    parser.add_argument("-t", "--type", default="video", choices=["video", "audio"], help="Media type (video or audio)")
    parser.add_argument("-q", "--quality", default="best", help="Quality (e.g. 1080p, 720p, 360p, or best)")
    parser.add_argument("-o", "--output", default="./downloads", help="Output directory (default: ./downloads)")

    args = parser.parse_args()
    download_media(url=args.url, media_type=args.type, quality=args.quality, output_dir=args.output)
