# 🚀 VidsSave Media Downloader API Wrapper

Ek powerful aur fast **REST API Wrapper** jo `vidssave.com` ke backend ko use karke YouTube, Instagram, Facebook, TikTok, Twitter/X, Reddit aadi se direct Video aur Audio download karta hai.

---

## 📁 Project Structure

- [`main.py`](file:///sdcard/PROJECT/main.py): FastAPI Application endpoints (`/api/info`, `/api/download`, `/api/stream`, Swagger Docs).
- [`vidssave.py`](file:///sdcard/PROJECT/vidssave.py): Core reverse-engineered VidsSave client with AES-CBC decryption & SSE progress listener.
- [`ytdlp_engine.py`](file:///sdcard/PROJECT/ytdlp_engine.py): Automatic fallback engine (yt-dlp) agar vidssave kisi URL ko support na kare.
- [`requirements.txt`](file:///sdcard/PROJECT/requirements.txt): Python dependencies.
- [`run.sh`](file:///sdcard/PROJECT/run.sh): Server start script.

---

## ⚡ Server Start Kaise Kare

```bash
cd /sdcard/PROJECT
bash run.sh
```
Server start hone ke baad browser me open kare:
- **Interactive Swagger Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔌 API Endpoints & Usage

### 1. Media Info Endpoint (`/api/info`)
Video ka Title, Duration, Thumbnail, aur sabhi available Video (1080p, 720p, 480p, 360p) aur Audio (MP3) qualities check karne ke liye.

**GET Request:**
```http
GET /api/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/api/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

---

### 2. Direct Download Link Endpoint (`/api/download`)
Link pass kare aur direct high-speed downloadable URL prapt kare.

**Parameters:**
- `url` *(required)*: Video ka link.
- `type` *(optional)*: `"video"` ya `"audio"` (default: `"video"`).
- `quality` *(optional)*: `"best"`, `"1080p"`, `"720p"`, `"480p"`, `"360p"` aadi.
- `format` *(optional)*: `"mp4"`, `"mp3"`.

**GET Request Example (Audio / MP3):**
```bash
curl -X GET "http://localhost:8000/api/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&type=audio"
```

**Response Example:**
```json
{
  "status": "success",
  "engine": "vidssave",
  "title": "Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster)",
  "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hq720.jpg",
  "duration": 213,
  "type": "audio",
  "quality": "128KBPS",
  "format": "MP3",
  "filesize": 3416200,
  "download_url": "https://down-de.vidssave.com/tmp/recycle/..."
}
```

---

### 3. Direct Streaming Download Endpoint (`/api/stream`)
Agar aap chahte hain ki browser me click karte hi ya cURL se seedhe file download ho jaye bina alag link kholne ke:

```bash
curl -OJ "http://localhost:8000/api/stream?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&type=video&quality=720p"
```
