import datetime
import logging
import time
import urllib.parse
from collections import deque
from typing import Optional
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel
import requests

import vidssave
import ytdlp_engine
import savefrom
from proxy_manager import proxy_pool
from frontend import get_downloader_html

# --- In-Memory Ring Buffer Logging ---
class RingBufferLogHandler(logging.Handler):
    def __init__(self, maxlen: int = 250):
        super().__init__()
        self.logs = deque(maxlen=maxlen)

    def emit(self, record):
        try:
            entry = {
                "timestamp": datetime.datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S"),
                "level": record.levelname,
                "name": record.name,
                "message": record.getMessage()
            }
            if record.exc_info:
                entry["exception"] = self.format(record)
            self.logs.append(entry)
        except Exception:
            self.handleError(record)


log_handler = RingBufferLogHandler()
log_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(log_handler)

logger = logging.getLogger("api")
START_TIME = time.time()
REQUEST_STATS = {"total": 0, "success": 0, "errors": 0}

app = FastAPI(
    title="Media Downloader API",
    description="High-speed REST API wrapper for downloading Video and Audio with live logs and monitoring.",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    REQUEST_STATS["total"] += 1
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        REQUEST_STATS["success"] += 1
        # Skip logging internal log polling to prevent log clutter
        if not request.url.path.startswith("/api/logs"):
            logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({process_time:.1f}ms)")
        return response
    except Exception as e:
        REQUEST_STATS["errors"] += 1
        logger.error(f"{request.method} {request.url.path} FAILED: {str(e)}")
        raise


class MediaInfoRequest(BaseModel):
    url: str
    engine: Optional[str] = None


class DownloadRequest(BaseModel):
    url: str
    type: Optional[str] = "video"
    quality: Optional[str] = "best"
    format: Optional[str] = None
    engine: Optional[str] = None


@app.get("/", response_model=None)
def home(request: Request):
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        return HTMLResponse(get_downloader_html())
    return {
        "status": "online",
        "service": "Media Downloader API",
        "uptime": f"{int(time.time() - START_TIME)}s",
        "features": "Automatic smart engine selection with multi-tier fallback (VidsSave -> SaveFrom -> YT-DLP)",
        "endpoints": {
            "GET /": "Web Downloader UI (Browser) or JSON Health Check (API)",
            "GET /app": "Web Downloader UI Direct Link",
            "GET /api/info?url={video_url}": "Get video metadata, thumbnail, duration, and all available qualities",
            "GET /api/download?url={video_url}&type=video|audio&quality=best": "Get direct instant download link (auto-picks best format)",
            "GET /api/stream?url={video_url}&type=video|audio": "1-click direct file streaming download",
            "GET /api/logs": "Server logs and metrics in JSON",
            "GET /logs": "Live Web Logs Dashboard",
            "GET /docs": "Interactive Swagger UI"
        }
    }


@app.get("/app", response_class=HTMLResponse)
@app.get("/downloader", response_class=HTMLResponse)
def web_downloader():
    """Universal Web Downloader User Interface."""
    return get_downloader_html()


# --- Logs Endpoints ---
@app.get("/api/logs")
def get_logs(limit: int = Query(50, ge=1, le=250), level: Optional[str] = Query(None)):
    """Returns server logs in JSON format."""
    entries = list(log_handler.logs)
    if level:
        level_upper = level.upper()
        entries = [log for log in entries if log["level"] == level_upper]
    entries = entries[-limit:]
    entries.reverse()

    return {
        "server_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "uptime_seconds": int(time.time() - START_TIME),
        "stats": REQUEST_STATS,
        "credentials": {
            "auth": vidssave.creds_manager.auth_code,
            "domain": vidssave.creds_manager.domain,
            "last_refresh": int(time.time() - vidssave.creds_manager.last_refresh) if vidssave.creds_manager.last_refresh else "never"
        },
        "proxies_count": len(proxy_pool.get_all()),
        "count": len(entries),
        "logs": entries
    }


@app.get("/logs", response_class=HTMLResponse)
def logs_dashboard():
    """Live web-based visual log dashboard."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>API Live Logs & Monitoring</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body { font-family: monospace, Consolas, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
    .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 15px; margin-bottom: 15px; }
    h1 { margin: 0; font-size: 20px; color: #38bdf8; }
    .stats { display: flex; gap: 15px; font-size: 13px; color: #94a3b8; }
    .badge { background: #1e293b; padding: 4px 10px; border-radius: 6px; border: 1px solid #334155; }
    .logs-container { background: #020617; border-radius: 8px; border: 1px solid #1e293b; padding: 15px; height: 75vh; overflow-y: auto; }
    .log-row { padding: 6px 0; border-bottom: 1px solid #0f172a; font-size: 13px; display: flex; gap: 10px; }
    .log-time { color: #64748b; min-width: 150px; }
    .log-level { font-weight: bold; min-width: 60px; }
    .level-INFO { color: #38bdf8; }
    .level-WARNING { color: #fbbf24; }
    .level-ERROR { color: #f87171; }
    .log-msg { color: #e2e8f0; word-break: break-all; }
    .btn { background: #38bdf8; color: #020617; border: none; padding: 6px 14px; font-weight: bold; border-radius: 6px; cursor: pointer; }
    .btn:hover { background: #7dd3fc; }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <h1>⚡ Live Server Logs & Metrics</h1>
      <div id="stats" class="stats" style="margin-top: 8px;">Loading stats...</div>
    </div>
    <div>
      <button class="btn" onclick="fetchLogs()">🔄 Refresh Now</button>
      <a href="/docs" target="_blank" style="color: #38bdf8; margin-left: 10px; font-size: 14px;">Swagger Docs &rarr;</a>
    </div>
  </div>
  <div class="logs-container" id="logsBox">Connecting...</div>

  <script>
    async function fetchLogs() {
      try {
        const res = await fetch('/api/logs?limit=100');
        const data = await res.json();
        
        document.getElementById('stats').innerHTML = `
          <span class="badge">Uptime: <b>${data.uptime_seconds}s</b></span>
          <span class="badge">Proxies: <b style="color:#38bdf8;">${data.proxies_count || 0} active</b></span>
          <span class="badge">Total: <b>${data.stats.total}</b></span>
          <span class="badge">Success: <b style="color:#4ade80;">${data.stats.success}</b></span>
          <span class="badge">Errors: <b style="color:#f87171;">${data.stats.errors}</b></span>
        `;

        const box = document.getElementById('logsBox');
        if (!data.logs || data.logs.length === 0) {
          box.innerHTML = '<div style="color: #64748b; padding: 20px;">No logs captured yet.</div>';
          return;
        }

        box.innerHTML = data.logs.map(log => `
          <div class="log-row">
            <span class="log-time">${log.timestamp}</span>
            <span class="log-level level-${log.level}">[${log.level}]</span>
            <span class="log-msg">${escapeHtml(log.message)}</span>
          </div>
        `).join('');
      } catch (err) {
        console.error(err);
      }
    }

    function escapeHtml(str) {
      return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    fetchLogs();
    setInterval(fetchLogs, 3000);
  </script>
</body>
</html>"""


# --- Core Logic ---
def _run_vidssave_info(target_url: str):
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
        "status": "success",
        "engine": "vidssave",
        "id": vs_data.get("id"),
        "title": vs_data.get("title"),
        "duration": vs_data.get("duration"),
        "thumbnail": vs_data.get("thumbnail"),
        "videos": videos,
        "audios": audios
    }


def _run_savefrom_info(target_url: str):
    return savefrom.parse_media(target_url)


def _run_ytdlp_info(target_url: str):
    ydl_data = ytdlp_engine.get_ytdlp_info(target_url)
    formats = ydl_data.get("formats", [])
    videos = []
    audios = []
    for f in formats:
        if f.get("ext") in ("mhtml", "jpg", "jpeg", "webp"):
            continue
        if f.get("vcodec") == "none" and f.get("acodec") and f.get("acodec") != "none":
            res_val = f"{int(f.get('abr'))}kbps" if f.get("abr") else (f.get("format_note") or "audio")
            audios.append({
                "quality": res_val,
                "format": f.get("ext"),
                "size": f.get("filesize") or f.get("filesize_approx"),
                "download_url": f.get("url")
            })
        elif f.get("vcodec") and f.get("vcodec") != "none":
            res_val = f.get("resolution") or (f"{f.get('height')}p" if f.get("height") else None)
            videos.append({
                "quality": res_val or f.get("format_note") or "video",
                "format": f.get("ext"),
                "size": f.get("filesize") or f.get("filesize_approx"),
                "download_url": f.get("url")
            })

    return {
        "status": "success",
        "engine": "yt-dlp",
        "id": ydl_data.get("id"),
        "title": ydl_data.get("title"),
        "duration": ydl_data.get("duration"),
        "thumbnail": ydl_data.get("thumbnail"),
        "videos": videos[:15],
        "audios": audios[:10]
    }


def _process_info(target_url: str, engine: Optional[str] = None):
    engine = (engine or "").lower().strip()

    if engine == "savefrom":
        return _run_savefrom_info(target_url)
    if engine == "vidssave":
        return _run_vidssave_info(target_url)
    if engine in ("ytdlp", "yt-dlp"):
        return _run_ytdlp_info(target_url)

    # Automatic Smart Waterfall: VidsSave -> SaveFrom -> YT-DLP
    errors = []
    try:
        return _run_vidssave_info(target_url)
    except Exception as e:
        logger.warning(f"VidsSave parse failed for {target_url}: {e}. Auto-switching to SaveFrom...")
        errors.append(f"vidssave: {e}")

    try:
        return _run_savefrom_info(target_url)
    except Exception as e:
        logger.warning(f"SaveFrom parse failed for {target_url}: {e}. Auto-switching to yt-dlp fallback...")
        errors.append(f"savefrom: {e}")

    try:
        return _run_ytdlp_info(target_url)
    except Exception as e:
        logger.error(f"All 3 engines failed for {target_url}: {e}")
        errors.append(f"yt-dlp: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Unable to parse media: {' | '.join(errors)}"
        )


@app.get("/api/info")
def get_info(
    url: str = Query(..., description="Target video URL (YouTube, Shorts, Instagram, TikTok, etc.)"),
    engine: Optional[str] = Query(None, description="Optional engine override (e.g. 'vidssave', 'savefrom', 'yt-dlp'). Default is automatic smart fallback.")
):
    return _process_info(url, engine=engine)


@app.post("/api/info")
def post_info(req: MediaInfoRequest):
    return _process_info(req.url, engine=req.engine)


def _run_vidssave_download(target_url: str, media_type: str = "video", quality: str = "best", output_format: Optional[str] = None):
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
        if media_type == "audio":
            selected = matching_resources[-1]
        else:
            mp4_resources = [r for r in matching_resources if (r.get("format") or "").upper() == "MP4"]
            high_mp4 = [r for r in mp4_resources if str(r.get("quality", "")).upper() in ("1080P", "720P")]
            if high_mp4:
                selected = high_mp4[-1]
            elif mp4_resources:
                selected = mp4_resources[-1]
            else:
                selected = matching_resources[-1]

    if not selected:
        raise ValueError("No matching media stream found on VidsSave")

    if selected.get("download_url"):
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
            "download_url": selected["download_url"]
        }

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


def _run_savefrom_download(target_url: str, media_type: str = "video", quality: str = "best"):
    return savefrom.get_direct_download(target_url, media_type=media_type, quality=quality)


def _run_ytdlp_download(target_url: str, media_type: str = "video", quality: str = "best"):
    res = ytdlp_engine.get_ytdlp_direct_link(target_url, media_type=media_type, quality=quality)
    if not res.get("direct_url"):
        raise ValueError("Could not extract direct stream URL via yt-dlp")
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


def _process_download(
    target_url: str,
    media_type: str = "video",
    quality: str = "best",
    output_format: Optional[str] = None,
    engine: Optional[str] = None
):
    media_type = (media_type or "video").lower()
    quality = (quality or "best").lower()
    engine = (engine or "").lower().strip()

    if engine == "savefrom":
        return _run_savefrom_download(target_url, media_type=media_type, quality=quality)
    if engine == "vidssave":
        return _run_vidssave_download(target_url, media_type=media_type, quality=quality, output_format=output_format)
    if engine in ("ytdlp", "yt-dlp"):
        return _run_ytdlp_download(target_url, media_type=media_type, quality=quality)

    # Automatic Smart Waterfall: VidsSave -> SaveFrom -> YT-DLP
    errors = []
    try:
        return _run_vidssave_download(target_url, media_type=media_type, quality=quality, output_format=output_format)
    except Exception as e:
        logger.warning(f"VidsSave download failed for {target_url}: {e}. Auto-switching to SaveFrom...")
        errors.append(f"vidssave: {e}")

    try:
        return _run_savefrom_download(target_url, media_type=media_type, quality=quality)
    except Exception as e:
        logger.warning(f"SaveFrom download failed for {target_url}: {e}. Auto-switching to yt-dlp fallback...")
        errors.append(f"savefrom: {e}")

    try:
        return _run_ytdlp_download(target_url, media_type=media_type, quality=quality)
    except Exception as e:
        logger.error(f"All 3 engines failed download for {target_url}: {e}")
        errors.append(f"yt-dlp: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Download failed: {' | '.join(errors)}"
        )


@app.get("/api/download")
def get_download(
    url: str = Query(..., description="Target video URL (YouTube, Shorts, Instagram, TikTok, etc.)"),
    type: str = Query("video", description="'video' or 'audio'"),
    quality: str = Query("best", description="Quality (e.g. 720p, 1080p, 360p, or 'best')"),
    format: Optional[str] = Query(None, description="Output format (mp4, mp3)"),
    engine: Optional[str] = Query(None, description="Optional engine override ('vidssave', 'savefrom', 'yt-dlp'). Default is automatic smart fallback.")
):
    return _process_download(url, media_type=type, quality=quality, output_format=format, engine=engine)


@app.post("/api/download")
def post_download(req: DownloadRequest):
    return _process_download(req.url, media_type=req.type, quality=req.quality, output_format=req.format, engine=req.engine)


@app.get("/api/stream")
def stream_media(
    url: str = Query(..., description="Target video URL"),
    type: str = Query("video", description="'video' or 'audio'"),
    quality: str = Query("best", description="Quality (e.g. 720p, 1080p, 360p, or 'best')"),
    engine: Optional[str] = Query(None, description="Optional engine override. Default is automatic.")
):
    dl_info = _process_download(url, media_type=type, quality=quality, engine=engine)
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
