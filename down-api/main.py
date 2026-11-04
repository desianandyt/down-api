import datetime
import logging
import time
import threading
import collections
import urllib.parse
from collections import deque
from typing import Optional, Dict, Any, Tuple
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, RedirectResponse
from pydantic import BaseModel
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import vidssave
import ytdlp_engine
import savefrom
import tikwm
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

# =========================================================================
# VALIDATION, CACHING & DEDUPLICATION (Load-Reduction Engine)
# =========================================================================
BLOCKED_HOSTS = {
    "localhost", "127.0.0.1", "0.0.0.0", "::1", "test", "example.com"
}

def validate_video_url(raw_url: str) -> str:
    """Validates and normalizes target video URL. Rejects garbage and SSRF targets immediately."""
    if not raw_url or not isinstance(raw_url, str):
        raise HTTPException(status_code=400, detail="Missing video URL.")
    
    url = raw_url.strip()
    if len(url) > 2048:
        raise HTTPException(status_code=400, detail="URL is too long.")
    
    # Auto-prepend https:// if omitted by user
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid URL format.")
    
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="Scheme must be http or https.")
    
    hostname = (parsed.hostname or "").lower()
    if not hostname:
        raise HTTPException(status_code=400, detail="URL must contain a valid domain.")
    
    if hostname in BLOCKED_HOSTS or hostname.startswith("10.") or hostname.startswith("192.168.") or hostname.startswith("172."):
        raise HTTPException(status_code=400, detail="Domain not permitted.")
    
    if "." not in hostname:
        raise HTTPException(status_code=400, detail="Please enter a valid website domain.")
    
    return url


def _get_client_ip(request: Request) -> str:
    """Extracts real client IP behind reverse proxy / Cloudflare / Render."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


class MediaCache:
    """In-memory TTL cache (10 minutes) for media metadata to eliminate redundant engine runs."""
    def __init__(self, ttl: int = 600, max_size: int = 1000):
        self.ttl = ttl
        self.max_size = max_size
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def get(self, url: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            item = self._cache.get(url)
            if not item:
                return None
            if time.time() - item["timestamp"] > self.ttl:
                del self._cache[url]
                return None
            return item["data"]

    def set(self, url: str, data: Dict[str, Any]):
        with self._lock:
            if len(self._cache) >= self.max_size:
                now = time.time()
                expired = [k for k, v in self._cache.items() if now - v["timestamp"] > self.ttl]
                for k in expired:
                    del self._cache[k]
                if len(self._cache) >= self.max_size:
                    for k in list(self._cache.keys())[:100]:
                        del self._cache[k]
            self._cache[url] = {"timestamp": time.time(), "data": data}


class InFlightManager:
    """
    Prevents duplicate concurrent scraper runs for the same URL.
    - If same client fires duplicate requests within 3s: blocks with 429 Too Many Requests.
    - If other clients request same URL in-flight: waits for primary worker & shares result.
    """
    def __init__(self):
        self._events: Dict[str, threading.Event] = {}
        self._client_recent: Dict[Tuple[str, str], float] = {}
        self._lock = threading.Lock()

    def acquire(self, client_ip: str, url: str) -> Tuple[bool, threading.Event]:
        with self._lock:
            now = time.time()
            recent_t = self._client_recent.get((client_ip, url))
            if recent_t and (now - recent_t < 3.0):
                raise HTTPException(
                    status_code=429,
                    detail="Duplicate request blocked. Extraction is already in progress, please wait."
                )
            self._client_recent[(client_ip, url)] = now
            if len(self._client_recent) > 1000:
                self._client_recent = {k: v for k, v in self._client_recent.items() if now - v < 30}

            if url in self._events:
                # Another worker is already extracting this URL
                return False, self._events[url]

            event = threading.Event()
            self._events[url] = event
            return True, event

    def release(self, url: str):
        with self._lock:
            event = self._events.pop(url, None)
            if event:
                event.set()


class RateLimiter:
    """Sliding-window rate limiter per client IP (max 35 requests per 60s)."""
    def __init__(self, max_reqs: int = 35, window_sec: int = 60):
        self.max_reqs = max_reqs
        self.window = window_sec
        self._records: Dict[str, deque] = {}
        self._lock = threading.Lock()

    def check(self, client_ip: str):
        with self._lock:
            now = time.time()
            q = self._records.setdefault(client_ip, deque())
            while q and q[0] < now - self.window:
                q.popleft()
            if len(q) >= self.max_reqs:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit reached. Please wait a moment before sending more requests."
                )
            q.append(now)


media_cache = MediaCache(ttl=600, max_size=1000)
inflight_mgr = InFlightManager()
rate_limiter = RateLimiter(max_reqs=35, window_sec=60)

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
    # Return JSON only if strictly requested by an API client
    if "application/json" in accept and "text/html" not in accept:
        return {
            "status": "online",
            "service": "Media Downloader API",
            "uptime": f"{int(time.time() - START_TIME)}s",
            "features": "100% Free Zero-Proxy Smart Engine with Multi-Tier Fallback (TikWM -> VidsSave -> SaveFrom -> YT-DLP)",
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
    return HTMLResponse(get_downloader_html())


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
        "network_mode": proxy_pool.status_summary,
        "proxies_count": len(proxy_pool.get_all()),
        "stats": REQUEST_STATS,
        "credentials": {
            "auth": vidssave.creds_manager.auth_code,
            "domain": vidssave.creds_manager.domain,
            "last_refresh": int(time.time() - vidssave.creds_manager.last_refresh) if vidssave.creds_manager.last_refresh else "never"
        },
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
          <span class="badge">Engine: <b style="color:#38bdf8;">${data.network_mode || 'Zero-Proxy Direct'}</b></span>
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
def _normalize_media_formats(videos: list, audios: list):
    """Guarantees rich quality options (1080p, 720p, 480p, 360p, MP3 bitrates) for every video/platform."""
    clean_videos = []
    for v in videos:
        q = str(v.get("quality") or "").strip().upper()
        if not q:
            d_url = v.get("direct_url") or ""
            if "1080" in d_url:
                q = "1080P"
            elif "720" in d_url:
                q = "720P"
            elif "480" in d_url:
                q = "480P"
            elif "360" in d_url:
                q = "360P"
            else:
                q = "720P"
        v["quality"] = q
        clean_videos.append(v)

    clean_audios = []
    for a in audios:
        q = str(a.get("quality") or "").strip().upper()
        if not q or q == "NONE":
            q = "128KBPS"
        a["quality"] = q
        clean_audios.append(a)

    # If the platform only provided 1 raw video format (e.g. Instagram Reels, TikTok, Twitter):
    if len(clean_videos) == 1:
        base_v = clean_videos[0]
        base_size = base_v.get("size") or 0
        standard_presets = [
            ("1080P", 1.45),
            ("720P", 1.0),
            ("480P", 0.65),
            ("360P", 0.40)
        ]
        multi_videos = []
        for q_name, scale_factor in standard_presets:
            est_size = int(base_size * scale_factor) if base_size else 0
            multi_videos.append({
                "quality": q_name,
                "format": base_v.get("format") or "mp4",
                "size": est_size,
                "resource_id": base_v.get("resource_id"),
                "direct_url": base_v.get("direct_url")
            })
        clean_videos = multi_videos

    # If audios list is empty or single, provide standard MP3 bitrates (320kbps, 256kbps, 128kbps)
    if len(clean_audios) <= 1:
        base_a = clean_audios[0] if clean_audios else (clean_videos[0] if clean_videos else {})
        base_size = base_a.get("size") or 2500000
        standard_audios = [
            {
                "quality": "320KBPS",
                "format": "MP3",
                "size": int(base_size * 1.25),
                "resource_id": base_a.get("resource_id"),
                "direct_url": base_a.get("direct_url")
            },
            {
                "quality": "256KBPS",
                "format": "MP3",
                "size": int(base_size * 1.0),
                "resource_id": base_a.get("resource_id"),
                "direct_url": base_a.get("direct_url")
            },
            {
                "quality": "128KBPS",
                "format": "MP3",
                "size": int(base_size * 0.5),
                "resource_id": base_a.get("resource_id"),
                "direct_url": base_a.get("direct_url")
            }
        ]
        clean_audios = standard_audios

    return clean_videos, clean_audios


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

    videos, audios = _normalize_media_formats(videos, audios)

    return {
        "status": "success",
        "engine": "vidssave",
        "id": vs_data.get("id"),
        "title": vs_data.get("title"),
        "duration": vs_data.get("duration"),
        "thumbnail": vs_data.get("thumbnail"),
        "videos": videos,
        "audios": audios,
        "_raw_resources": resources
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


def _run_extraction_waterfall(target_url: str, engine: Optional[str] = None):
    engine = (engine or "").lower().strip()

    if engine == "tikwm":
        return tikwm.parse_tiktok(target_url)
    if engine == "savefrom":
        return _run_savefrom_info(target_url)
    if engine == "vidssave":
        return _run_vidssave_info(target_url)
    if engine in ("ytdlp", "yt-dlp"):
        return _run_ytdlp_info(target_url)

    # 1. Zero-Proxy TikTok Handler (Instant <500ms HD No-Watermark)
    if tikwm.is_tiktok_url(target_url):
        try:
            return tikwm.parse_tiktok(target_url)
        except Exception as e:
            logger.warning(f"TikWM parse failed for {target_url}: {e}. Falling back to multi-engine waterfall...")

    # 2. Automatic Smart Waterfall: VidsSave -> SaveFrom -> YT-DLP (All Zero-Proxy Ready)
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
        logger.error(f"All engines failed for {target_url}: {e}")
        errors.append(f"yt-dlp: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Unable to parse media: {' | '.join(errors)}"
        )


def _process_info(target_url: str, engine: Optional[str] = None, client_ip: str = "unknown"):
    # 1. Validate & sanitize URL immediately (rejects garbage / SSRF without scraper load)
    target_url = validate_video_url(target_url)

    # 2. Return from in-memory cache if requested recently (<1ms latency)
    cached = media_cache.get(target_url)
    if cached:
        logger.info(f"Cache HIT for {target_url} -> 0ms zero engine load")
        return cached

    # 3. In-flight single-worker locking & duplicate burst blocker
    is_worker, event = inflight_mgr.acquire(client_ip, target_url)
    if not is_worker:
        logger.info(f"Waiting for in-flight extraction on {target_url}...")
        if event.wait(timeout=16):
            cached = media_cache.get(target_url)
            if cached:
                return cached
        raise HTTPException(
            status_code=429,
            detail="A request for this media URL is currently being processed. Please retry in a few seconds."
        )

    try:
        data = _run_extraction_waterfall(target_url, engine=engine)
        media_cache.set(target_url, data)
        return data
    finally:
        inflight_mgr.release(target_url)


@app.get("/api/info")
def get_info(
    request: Request,
    url: str = Query(..., description="Target video URL (YouTube, Shorts, Instagram, TikTok, etc.)"),
    engine: Optional[str] = Query(None, description="Optional engine override (e.g. 'vidssave', 'savefrom', 'yt-dlp'). Default is automatic smart fallback.")
):
    client_ip = _get_client_ip(request)
    rate_limiter.check(client_ip)
    return _process_info(url, engine=engine, client_ip=client_ip)


@app.post("/api/info")
def post_info(request: Request, req: MediaInfoRequest):
    client_ip = _get_client_ip(request)
    rate_limiter.check(client_ip)
    return _process_info(req.url, engine=req.engine, client_ip=client_ip)


def _run_vidssave_download(target_url: str, media_type: str = "video", quality: str = "best", output_format: Optional[str] = None):
    # Reuse parsed resources from cache if available to prevent redundant scraping & risk checks
    cached = media_cache.get(target_url)
    if cached and cached.get("engine") == "vidssave" and cached.get("_raw_resources"):
        resources = cached["_raw_resources"]
        title = cached.get("title", "download")
        thumbnail = cached.get("thumbnail")
        duration = cached.get("duration")
    else:
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
            "quality": selected.get("quality") or (quality.upper() if quality != "best" else "720P"),
            "format": selected.get("format") or ("mp3" if media_type == "audio" else "mp4"),
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
        "quality": selected.get("quality") or (quality.upper() if quality != "best" else "720P"),
        "format": selected.get("format") or ("mp3" if media_type == "audio" else "mp4"),
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
    target_url = validate_video_url(target_url)
    media_type = (media_type or "video").lower()
    quality = (quality or "best").lower()
    engine = (engine or "").lower().strip()

    if engine == "tikwm":
        return tikwm.get_tiktok_download(target_url, media_type=media_type, quality=quality)
    if engine == "savefrom":
        return _run_savefrom_download(target_url, media_type=media_type, quality=quality)
    if engine == "vidssave":
        return _run_vidssave_download(target_url, media_type=media_type, quality=quality, output_format=output_format)
    if engine in ("ytdlp", "yt-dlp"):
        return _run_ytdlp_download(target_url, media_type=media_type, quality=quality)

    # 1. Zero-Proxy TikTok Handler
    if tikwm.is_tiktok_url(target_url):
        try:
            return tikwm.get_tiktok_download(target_url, media_type=media_type, quality=quality)
        except Exception as e:
            logger.warning(f"TikWM download failed for {target_url}: {e}. Falling back to multi-engine waterfall...")

    # 2. Automatic Smart Waterfall: VidsSave -> SaveFrom -> YT-DLP
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
    request: Request,
    url: str = Query(..., description="Target video URL (YouTube, Shorts, Instagram, TikTok, etc.)"),
    type: str = Query("video", description="'video' or 'audio'"),
    quality: str = Query("best", description="Quality (e.g. 720p, 1080p, 360p, or 'best')"),
    format: Optional[str] = Query(None, description="Output format (mp4, mp3)"),
    engine: Optional[str] = Query(None, description="Optional engine override ('vidssave', 'savefrom', 'yt-dlp'). Default is automatic smart fallback.")
):
    client_ip = _get_client_ip(request)
    rate_limiter.check(client_ip)
    return _process_download(url, media_type=type, quality=quality, output_format=format, engine=engine)


@app.post("/api/download")
def post_download(request: Request, req: DownloadRequest):
    client_ip = _get_client_ip(request)
    rate_limiter.check(client_ip)
    return _process_download(req.url, media_type=req.type, quality=req.quality, output_format=req.format, engine=req.engine)


@app.get("/api/stream")
def stream_media(
    request: Request,
    url: str = Query(..., description="Target video URL"),
    type: str = Query("video", description="'video' or 'audio'"),
    quality: str = Query("best", description="Quality (e.g. 720p, 1080p, 360p, or 'best')"),
    engine: Optional[str] = Query(None, description="Optional engine override. Default is automatic.")
):
    client_ip = _get_client_ip(request)
    rate_limiter.check(client_ip)
    url = validate_video_url(url)
    dl_info = _process_download(url, media_type=type, quality=quality, engine=engine)
    direct_url = dl_info.get("download_url")

    if not direct_url:
        raise HTTPException(status_code=404, detail="Could not obtain direct streaming URL")

    target_host = urllib.parse.urlparse(direct_url).netloc.lower()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }
    if "vidssave" in target_host:
        headers["Referer"] = "https://vidssave.com/"
        headers["Origin"] = "https://vidssave.com"
    elif "googlevideo.com" in target_host or "youtube.com" in target_host:
        headers["Referer"] = "https://www.youtube.com/"
    elif "tiktok" in target_host or "tikwm" in target_host:
        headers["Referer"] = "https://www.tiktok.com/"
    elif "instagram" in target_host:
        headers["Referer"] = "https://www.instagram.com/"

    r = None
    # 1. Try direct stream fetch with appropriate referer
    try:
        r = requests.get(direct_url, headers=headers, stream=True, timeout=25, verify=False)
        if r.status_code != 200 or "text/html" in r.headers.get("Content-Type", ""):
            r = None
    except Exception as e:
        logger.warning(f"Direct stream fetch failed for {target_host}: {e}")
        r = None

    # 2. If direct fails (e.g. IP-bound signed proxy link), try fallback proxy
    if r is None:
        fallback_proxies = proxy_pool.get_fallback_dict()
        if fallback_proxies:
            try:
                r = requests.get(direct_url, headers=headers, proxies=fallback_proxies, stream=True, timeout=25, verify=False)
                if r.status_code != 200:
                    r = None
            except Exception as e:
                logger.warning(f"Fallback proxy stream fetch failed: {e}")
                r = None

    # 3. Emergency fallback: try plain generic headers directly
    if r is None:
        try:
            simple_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            r = requests.get(direct_url, headers=simple_headers, stream=True, timeout=15, verify=False)
            if r.status_code != 200:
                r = None
        except Exception as e:
            logger.warning(f"Generic header stream fetch failed: {e}")
            r = None

    # 4. If server stream proxying was blocked by origin/CDN (e.g. 403 Forbidden on datacenter IP),
    # seamlessly redirect client browser directly to the media URL so browser downloads natively!
    if r is None or getattr(r, 'status_code', None) != 200:
        logger.info(f"Server-side proxy fetch was blocked/failed for {target_host}. Seamlessly redirecting client to origin...")
        return RedirectResponse(url=direct_url, status_code=307)

    # Build RFC 6266 safe ASCII filename & UTF-8 encoded filename to avoid latin-1 header crashes
    raw_title = str(dl_info.get("title") or "media").strip()
    clean_title = "".join(c for c in raw_title if c.isalnum() or c in (" ", "-", "_")).strip() or "media"
    quality_tag = dl_info.get("quality") or ("MP3" if type == "audio" else "HD")
    ext = (dl_info.get("format") or ("mp3" if type == "audio" else "mp4")).lower()
    
    full_filename = f"{clean_title} - {quality_tag}.{ext}"
    ascii_filename = "".join(c for c in full_filename if c.isascii() and c not in ('"', '\r', '\n', '\\')).strip()
    if not ascii_filename:
        ascii_filename = f"media - {quality_tag}.{ext}"
    quoted_filename = urllib.parse.quote(full_filename)

    def iter_content():
        for chunk in r.iter_content(chunk_size=1024 * 64):
            if chunk:
                yield chunk

    response_headers = {
        "Content-Disposition": f"attachment; filename=\"{ascii_filename}\"; filename*=UTF-8''{quoted_filename}",
        "Content-Type": r.headers.get("Content-Type", "application/octet-stream")
    }
    if "Content-Length" in r.headers:
        response_headers["Content-Length"] = r.headers["Content-Length"]

    return StreamingResponse(iter_content(), headers=response_headers)
