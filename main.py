import logging
import urllib.parse
from typing import Optional
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, HttpUrl
import requests

import vidssave
import ytdlp_engine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("api")

app = FastAPI(
    title="Media Downloader API (VidsSave Wrapper)",
    description="High-speed REST API wrapper for downloading Video and Audio from YouTube, Instagram, Facebook, TikTok, Twitter/X, and more.",
    version="1.0.0"
)

# Enable CORS for frontend integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MediaInfoRequest(BaseModel):
    url: str


class DownloadRequest(BaseModel):
    url: str
    type: Optional[str] = "video"  # "video" or "audio"
    quality: Optional[str] = "best"
    format: Optional[str] = None


@app.get("/api/debug")
def debug():
    import requests
    try:
        ip_info = requests.get("https://api.ipify.org?format=json", timeout=5).json()
    except Exception as e:
        ip_info = {"error": str(e)}

    test_payload = {
        "hostname": "vidssave.com",
        "auth": vidssave.AUTH_CODE,
        "domain": vidssave.DOMAIN,
        "origin": "source",
        "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }
    try:
        r = requests.post(f"{vidssave.API_BASE}/api/contentsite_api/media/parse", data=test_payload, headers=vidssave.DEFAULT_HEADERS, timeout=10)
        vs_res = {"status_code": r.status_code, "text": r.text, "headers": dict(r.headers)}
    except Exception as e:
        vs_res = {"error": str(e)}

    return {
        "render_ip": ip_info,
        "vidssave_response": vs_res
    }


@app.get("/")
def home():
    return {
        "message": "Welcome to VidsSave Media Downloader API",
        "docs": "/docs",
        "endpoints": {
            "GET /api/info?url={video_url}": "Get video metadata and available qualities",
            "POST /api/info": "Get metadata via JSON body {'url': '...'}",
            "GET /api/download?url={video_url}&type=video|audio&quality=720p": "Get direct download link",
            "POST /api/download": "Get direct download link via JSON body",
            "GET /api/stream?url={video_url}&type=video|audio": "Directly download/stream the file"
        }
    }


def _process_info(target_url: str):
    # Try VidsSave first
    try:
        vs_data = vidssave.parse_media(target_url)
        resources = vs_data.get("resources", [])
        
        videos = []
        audios = []
        for r in resources:
            item = {
                "quality": r.get("quality"),
                "format": r.get("format"),
                "size": r.get("size"),
                "resource_id": r.get("resource_content"),
                "direct_url": r.get("download_url")
            }
            if r.get("type") == "audio":
                audios.append(item)
            else:
                videos.append(item)

        return {
            "engine": "vidssave",
            "id": vs_data.get("id"),
            "title": vs_data.get("title"),
            "duration": vs_data.get("duration"),
            "thumbnail": vs_data.get("thumbnail"),
            "videos": videos,
            "audios": audios
        }
    except Exception as e:
        logger.warning(f"VidsSave parse failed ({e}), falling back to yt-dlp...")
        try:
            ydl_data = ytdlp_engine.get_ytdlp_info(target_url)
            return {
                "engine": "yt-dlp",
                "id": ydl_data.get("id"),
                "title": ydl_data.get("title"),
                "duration": ydl_data.get("duration"),
                "thumbnail": ydl_data.get("thumbnail"),
                "formats": [
                    {
                        "format_id": f.get("format_id"),
                        "ext": f.get("ext"),
                        "resolution": f.get("resolution"),
                        "filesize": f.get("filesize"),
                        "url": f.get("url")
                    }
                    for f in ydl_data.get("formats", [])
                    if f.get("url")
                ]
            }
        except Exception as ydl_err:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch media information: {str(e)} | Fallback error: {str(ydl_err)}"
            )


@app.get("/api/info")
def get_info(url: str = Query(..., description="Target video URL")):
    return _process_info(url)


@app.post("/api/info")
def post_info(req: MediaInfoRequest):
    return _process_info(req.url)


def _process_download(target_url: str, media_type: str = "video", quality: str = "best", output_format: Optional[str] = None):
    media_type = (media_type or "video").lower()
    quality = (quality or "best").lower()

    # 1. Try VidsSave API
    try:
        vs_data = vidssave.parse_media(target_url)
        resources = vs_data.get("resources", [])
        title = vs_data.get("title", "download")
        thumbnail = vs_data.get("thumbnail")
        duration = vs_data.get("duration")

        matching_resources = [r for r in resources if r.get("type") == media_type]
        if not matching_resources:
            matching_resources = resources

        selected = None
        if quality != "best":
            q_clean = quality.upper().replace("P", "")
            for r in matching_resources:
                rq = str(r.get("quality", "")).upper().replace("P", "")
                if rq == q_clean:
                    selected = r
                    break

        if not selected and matching_resources:
            selected = matching_resources[-1] if media_type == "video" else matching_resources[0]

        if not selected:
            raise ValueError("No matching media stream found")

        # Check if direct url is provided
        if selected.get("download_url"):
            direct_url = selected["download_url"]
            return {
                "status": "success",
                "engine": "vidssave",
                "title": title,
                "thumbnail": thumbnail,
                "duration": duration,
                "type": media_type,
                "quality": selected.get("quality"),
                "format": selected.get("format"),
                "filesize": selected.get("size"),
                "download_url": direct_url
            }

        # Otherwise resolve via SSE download endpoint
        resolved = vidssave.resolve_download_link(
            resource_content=selected["resource_content"],
            output_format=output_format or selected.get("format", "").lower()
        )

        return {
            "status": "success",
            "engine": "vidssave",
            "title": title,
            "thumbnail": thumbnail,
            "duration": duration,
            "type": media_type,
            "quality": selected.get("quality"),
            "format": selected.get("format"),
            "filesize": resolved.get("filesize") or selected.get("size"),
            "download_url": resolved.get("direct_url") or resolved.get("download_link")
        }

    except Exception as e:
        logger.warning(f"VidsSave download flow failed ({e}), attempting yt-dlp fallback...")
        try:
            res = ytdlp_engine.get_ytdlp_direct_link(target_url, media_type=media_type, quality=quality)
            if not res.get("direct_url"):
                raise ValueError("Could not extract direct stream URL")
            return {
                "status": "success",
                "engine": "yt-dlp",
                "title": res.get("title"),
                "thumbnail": res.get("thumbnail"),
                "duration": res.get("duration"),
                "type": media_type,
                "quality": res.get("quality"),
                "format": res.get("format"),
                "filesize": res.get("filesize"),
                "download_url": res.get("direct_url")
            }
        except Exception as ydl_err:
            raise HTTPException(
                status_code=400,
                detail=f"Download failed: {str(e)} | Fallback error: {str(ydl_err)}"
            )


@app.get("/api/download")
def get_download(
    url: str = Query(..., description="Target video URL"),
    type: str = Query("video", description="'video' or 'audio'"),
    quality: str = Query("best", description="Quality (e.g. 720p, 1080p, 360p, or best)"),
    format: Optional[str] = Query(None, description="Output format (mp4, mp3)")
):
    return _process_download(url, media_type=type, quality=quality, output_format=format)


@app.post("/api/download")
def post_download(req: DownloadRequest):
    return _process_download(req.url, media_type=req.type, quality=req.quality, output_format=req.format)


@app.get("/api/stream")
def stream_media(
    url: str = Query(..., description="Target video URL"),
    type: str = Query("video", description="'video' or 'audio'"),
    quality: str = Query("best", description="Quality (e.g. 720p, 1080p, 360p, or best)")
):
    """
    Streams file bytes directly to the browser / client as a download attachment.
    """
    dl_info = _process_download(url, media_type=type, quality=quality)
    direct_url = dl_info.get("download_url")

    if not direct_url:
        raise HTTPException(status_code=404, detail="Could not obtain direct streaming URL")

    headers = {"User-Agent": vidssave.DEFAULT_HEADERS["User-Agent"]}
    r = requests.get(direct_url, headers=headers, stream=True)
    
    clean_title = "".join(c for c in dl_info.get("title", "media") if c.isalnum() or c in (" ", "-", "_")).strip()
    ext = dl_info.get("format") or ("mp3" if type == "audio" else "mp4")
    filename = f"{clean_title}.{ext.lower()}"
    quoted_filename = urllib.parse.quote(filename)

    def iter_content():
        for chunk in r.iter_content(chunk_size=1024 * 64):
            if chunk:
                yield chunk

    response_headers = {
        "Content-Disposition": f"attachment; filename=\"{filename}\"; filename*=UTF-8''{quoted_filename}",
        "Content-Type": r.headers.get("Content-Type", "application/octet-stream")
    }
    if "Content-Length" in r.headers:
        response_headers["Content-Length"] = r.headers["Content-Length"]

    return StreamingResponse(iter_content(), headers=response_headers)
