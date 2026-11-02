# 🚀 VidsSave Media Downloader API Wrapper & Live Logs

Ek powerful aur fast **REST API Wrapper** jo `vidssave.com` ke backend aur `yt-dlp` ko use karke YouTube, Instagram, Facebook, TikTok, Twitter/X, Reddit aadi se direct Video aur Audio download karta hai. Isme live logs aur system metrics dashboard bhi shamil hai.

---

## 📁 Project Structure

- [`main.py`](file:///sdcard/PROJECT/main.py): FastAPI Application endpoints (`/api/info`, `/api/download`, `/api/stream`, `/api/logs`, `/logs`, `/docs`).
- [`vidssave.py`](file:///sdcard/PROJECT/vidssave.py): Core reverse-engineered VidsSave client with dynamic auto-refreshing credentials & SSE resolver.
- [`ytdlp_engine.py`](file:///sdcard/PROJECT/ytdlp_engine.py): Smart fallback engine (yt-dlp with `android`, `ios`, `mweb` client spoofing).
- [`requirements.txt`](file:///sdcard/PROJECT/requirements.txt): Python dependencies.
- [`run.sh`](file:///sdcard/PROJECT/run.sh): Server launch script.

---

## ⚡ Server Start & Dashboards

```bash
cd /sdcard/PROJECT
bash run.sh
```

- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Live Logs Web Dashboard**: [http://localhost:8000/logs](http://localhost:8000/logs)
- **Logs API (JSON)**: [http://localhost:8000/api/logs](http://localhost:8000/api/logs)

---

## 🔌 API Endpoints & Usage

### 1. Live Logs API (`/api/logs` & `/logs`)
Server ke real-time requests, errors aur credentials status check karne ke liye:
- **Web UI**: Open `/logs` in your browser for real-time visual monitor.
- **JSON API**: `GET /api/logs?limit=50&level=INFO`

### 2. Media Info Endpoint (`/api/info`)
Video ka Title, Duration, Thumbnail, aur sabhi available Video (1080p, 720p, 480p, 360p) aur Audio (MP3) qualities check karne ke liye:
```http
GET /api/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### 3. Direct Download Link Endpoint (`/api/download`)
Link pass karein aur direct high-speed downloadable URL prapt karein:
- **Audio (MP3)**: `GET /api/download?url={VIDEO_URL}&type=audio`
- **Video (720p)**: `GET /api/download?url={VIDEO_URL}&type=video&quality=720p`

### 4. Direct Streaming Download Endpoint (`/api/stream`)
Seedhe browser ya cURL se file download shuru karwane ke liye:
```bash
curl -OJ "http://localhost:8000/api/stream?url={VIDEO_URL}&type=video&quality=720p"
```
