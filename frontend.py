def get_downloader_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>⚡ AnyDownloader — Universal High-Speed Video & Audio Downloader</title>
  <meta name="description" content="Download videos and music from YouTube, Shorts, Instagram Reels, TikTok, Facebook, and Twitter in 1080p, 720p, MP4, and MP3.">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: #111827;
      --card-border: #1f293d;
      --accent: #38bdf8;
      --accent-glow: rgba(56, 189, 248, 0.35);
      --accent-hover: #0284c7;
      --text-main: #f8fafc;
      --text-sub: #94a3b8;
      --success: #10b981;
      --danger: #ef4444;
      --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text-main);
      font-family: var(--font);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }

    /* Ambient Glow background */
    .glow-bg {
      position: fixed;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 1000px;
      height: 450px;
      background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, rgba(99, 102, 241, 0.08) 50%, transparent 80%);
      z-index: 0;
      pointer-events: none;
    }

    /* Navbar */
    header {
      position: relative;
      z-index: 10;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 24px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      background: rgba(11, 15, 25, 0.7);
      backdrop-filter: blur(12px);
    }
    .logo {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 20px;
      font-weight: 800;
      color: #fff;
      text-decoration: none;
      letter-spacing: -0.5px;
    }
    .logo-badge {
      background: linear-gradient(135deg, #38bdf8, #6366f1);
      padding: 4px 8px;
      border-radius: 6px;
      font-size: 11px;
      color: #fff;
      font-weight: 700;
    }
    .nav-links {
      display: flex;
      gap: 12px;
      align-items: center;
    }
    .nav-link {
      color: var(--text-sub);
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 6px;
      transition: all 0.2s;
    }
    .nav-link:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.05);
    }
    .live-status {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      color: #34d399;
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.2);
      padding: 4px 10px;
      border-radius: 20px;
    }
    .status-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(0.85); }
    }

    /* Main Container */
    main {
      position: relative;
      z-index: 10;
      flex: 1;
      max-width: 860px;
      width: 100%;
      margin: 0 auto;
      padding: 40px 20px;
    }

    /* Hero Section */
    .hero {
      text-align: center;
      margin-bottom: 35px;
    }
    .hero h1 {
      font-size: 38px;
      font-weight: 900;
      line-height: 1.2;
      letter-spacing: -1px;
      margin-bottom: 12px;
      background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero p {
      color: var(--text-sub);
      font-size: 16px;
      max-width: 550px;
      margin: 0 auto;
    }

    /* Input Box Card */
    .input-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 8px;
      box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5), 0 0 20px var(--accent-glow);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .input-card:focus-within {
      border-color: var(--accent);
      box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.6), 0 0 35px var(--accent-glow);
    }
    .input-group {
      display: flex;
      align-items: center;
      gap: 10px;
      position: relative;
    }
    .input-icon {
      padding-left: 14px;
      color: #64748b;
      display: flex;
      align-items: center;
    }
    .url-input {
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      font-size: 16px;
      color: #fff;
      padding: 14px 6px;
      width: 100%;
    }
    .url-input::placeholder {
      color: #475569;
    }
    .btn-paste {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #cbd5e1;
      padding: 8px 12px;
      border-radius: 10px;
      font-size: 13px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s;
    }
    .btn-paste:hover {
      background: rgba(255, 255, 255, 0.15);
      color: #fff;
    }
    .btn-submit {
      background: linear-gradient(135deg, #38bdf8 0%, #2563eb 100%);
      color: #fff;
      border: none;
      padding: 14px 26px;
      font-size: 15px;
      font-weight: 700;
      border-radius: 12px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4);
      transition: all 0.2s;
      white-space: nowrap;
    }
    .btn-submit:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(56, 189, 248, 0.6);
      filter: brightness(1.1);
    }
    .btn-submit:active {
      transform: translateY(1px);
    }
    .btn-submit:disabled {
      opacity: 0.6;
      cursor: not-allowed;
      transform: none;
    }

    /* Platform Pills */
    .platforms {
      display: flex;
      justify-content: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 20px;
    }
    .platform-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.06);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 12px;
      color: var(--text-sub);
      transition: all 0.2s;
    }
    .platform-pill:hover {
      background: rgba(255, 255, 255, 0.07);
      color: #fff;
      border-color: rgba(255, 255, 255, 0.15);
    }

    /* Loading Spinner */
    .loading-container {
      display: none;
      text-align: center;
      padding: 40px 0;
    }
    .spinner {
      width: 48px;
      height: 48px;
      border: 4px solid rgba(56, 189, 248, 0.15);
      border-top-color: var(--accent);
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      margin: 0 auto 16px;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    .loading-text {
      font-size: 15px;
      color: #cbd5e1;
      font-weight: 600;
    }
    .loading-subtext {
      font-size: 12px;
      color: #64748b;
      margin-top: 4px;
    }

    /* Error Message Box */
    .error-box {
      display: none;
      background: rgba(239, 68, 68, 0.1);
      border: 1px solid rgba(239, 68, 68, 0.25);
      color: #fca5a5;
      padding: 16px 20px;
      border-radius: 12px;
      margin-top: 25px;
      font-size: 14px;
      display: flex;
      align-items: flex-start;
      gap: 12px;
    }

    /* Result Card */
    .result-card {
      display: none;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 24px;
      margin-top: 30px;
      box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.5);
      animation: fadeIn 0.4s ease-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(12px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .video-info-header {
      display: flex;
      gap: 20px;
      margin-bottom: 24px;
    }
    .thumb-wrap {
      position: relative;
      width: 220px;
      min-width: 220px;
      height: 130px;
      border-radius: 12px;
      overflow: hidden;
      background: #000;
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    }
    .thumb-wrap img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    .duration-badge {
      position: absolute;
      bottom: 8px;
      right: 8px;
      background: rgba(0, 0, 0, 0.8);
      color: #fff;
      font-size: 11px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      backdrop-filter: blur(4px);
    }
    .video-details {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .video-title {
      font-size: 17px;
      font-weight: 700;
      line-height: 1.4;
      color: #fff;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .video-meta {
      display: flex;
      gap: 12px;
      align-items: center;
      margin-top: 8px;
      font-size: 12px;
      color: #94a3b8;
    }
    .engine-tag {
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.25);
      color: #38bdf8;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 700;
      text-transform: uppercase;
      font-size: 10px;
    }

    /* Fast Action Row */
    .fast-actions {
      display: flex;
      gap: 12px;
      margin-top: 14px;
      flex-wrap: wrap;
    }
    .btn-quick-video {
      background: #10b981;
      color: #fff;
      border: none;
      padding: 10px 18px;
      font-size: 13px;
      font-weight: 700;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
      text-decoration: none;
    }
    .btn-quick-video:hover {
      background: #059669;
      transform: translateY(-1px);
    }
    .btn-quick-audio {
      background: #6366f1;
      color: #fff;
      border: none;
      padding: 10px 18px;
      font-size: 13px;
      font-weight: 700;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
      text-decoration: none;
    }
    .btn-quick-audio:hover {
      background: #4f46e5;
      transform: translateY(-1px);
    }

    /* Tabs */
    .tabs-header {
      display: flex;
      border-bottom: 1px solid var(--card-border);
      margin-top: 20px;
      margin-bottom: 16px;
      gap: 10px;
    }
    .tab-btn {
      background: transparent;
      border: none;
      outline: none;
      color: var(--text-sub);
      font-size: 14px;
      font-weight: 700;
      padding: 10px 16px;
      cursor: pointer;
      border-bottom: 2px solid transparent;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .tab-btn.active {
      color: var(--accent);
      border-bottom-color: var(--accent);
    }
    .tab-btn:hover:not(.active) {
      color: #fff;
    }

    /* Streams Table */
    .stream-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }
    .stream-table th {
      text-align: left;
      padding: 10px 12px;
      color: #64748b;
      font-weight: 600;
      border-bottom: 1px solid var(--card-border);
    }
    .stream-table td {
      padding: 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.03);
      vertical-align: middle;
    }
    .stream-table tr:hover td {
      background: rgba(255, 255, 255, 0.02);
    }
    .quality-badge {
      display: inline-block;
      font-weight: 700;
      color: #fff;
      font-size: 13px;
    }
    .format-tag {
      color: #64748b;
      font-size: 11px;
      text-transform: uppercase;
      font-weight: 600;
      margin-left: 6px;
    }
    .has-audio-tag {
      font-size: 10px;
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      padding: 2px 6px;
      border-radius: 4px;
      margin-left: 6px;
    }
    .btn-download-sm {
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.25);
      color: #38bdf8;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s;
    }
    .btn-download-sm:hover {
      background: var(--accent);
      color: #0b0f19;
    }

    /* How to Use Section */
    .how-section {
      margin-top: 60px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      padding-top: 40px;
    }
    .how-title {
      text-align: center;
      font-size: 22px;
      font-weight: 800;
      margin-bottom: 30px;
    }
    .steps-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
    }
    .step-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 20px;
      text-align: center;
    }
    .step-num {
      width: 36px;
      height: 36px;
      line-height: 36px;
      border-radius: 50%;
      background: rgba(56, 189, 248, 0.1);
      color: var(--accent);
      font-weight: 800;
      margin: 0 auto 12px;
      font-size: 16px;
    }
    .step-card h3 {
      font-size: 15px;
      font-weight: 700;
      margin-bottom: 6px;
    }
    .step-card p {
      font-size: 13px;
      color: var(--text-sub);
      line-height: 1.4;
    }

    /* Footer */
    footer {
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      padding: 24px;
      text-align: center;
      font-size: 13px;
      color: #64748b;
      margin-top: auto;
    }

    /* Responsive */
    @media (max-width: 680px) {
      .hero h1 { font-size: 28px; }
      .video-info-header { flex-direction: column; }
      .thumb-wrap { width: 100%; height: 190px; }
      .steps-grid { grid-template-columns: 1fr; }
      .btn-submit span { display: none; }
      .btn-submit { padding: 14px 18px; }
    }
  </style>
</head>
<body>
  <div class="glow-bg"></div>

  <!-- Header -->
  <header>
    <a href="/" class="logo">
      <span>⚡ AnyDownloader</span>
      <span class="logo-badge">PRO v1.2</span>
    </a>
    <div class="nav-links">
      <div class="live-status">
        <span class="status-dot"></span>
        <span>Online</span>
      </div>
      <a href="/logs" class="nav-link" target="_blank">Live Logs</a>
      <a href="/docs" class="nav-link" target="_blank">Swagger API</a>
    </div>
  </header>

  <!-- Main Content -->
  <main>
    <div class="hero">
      <h1>Download Video & Audio In Seconds</h1>
      <p>High-speed direct downloader for YouTube, Shorts, Instagram Reels, TikTok, Twitter/X, and Facebook.</p>
    </div>

    <!-- Input Card -->
    <div class="input-card">
      <form id="downloadForm" onsubmit="handleFetch(event)">
        <div class="input-group">
          <div class="input-icon">
            <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path></svg>
          </div>
          <input 
            type="url" 
            id="urlInput" 
            class="url-input" 
            placeholder="Paste YouTube, Reels, TikTok, or video link here..." 
            required 
            autocomplete="off"
          />
          <button type="button" class="btn-paste" onclick="pasteClipboard()">
            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
            Paste
          </button>
          <button type="submit" id="submitBtn" class="btn-submit">
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
            <span>Download</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Supported Platform Badges -->
    <div class="platforms">
      <span class="platform-pill">🔴 YouTube & Shorts</span>
      <span class="platform-pill">🟣 Instagram Reels</span>
      <span class="platform-pill">⚫ TikTok</span>
      <span class="platform-pill">🔵 Facebook</span>
      <span class="platform-pill">⚪ Twitter / X</span>
    </div>

    <!-- Loading State -->
    <div id="loadingBox" class="loading-container">
      <div class="spinner"></div>
      <div class="loading-text">Resolving Media Streams...</div>
      <div class="loading-subtext">Checking VidsSave, SaveFrom, and fallback engines with proxy protection</div>
    </div>

    <!-- Error Box -->
    <div id="errorBox" class="error-box" style="display: none;">
      <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
      <div id="errorMsg">Could not parse link. Please check the URL.</div>
    </div>

    <!-- Result Card -->
    <div id="resultCard" class="result-card">
      <div class="video-info-header">
        <div class="thumb-wrap">
          <img id="resThumb" src="" alt="Thumbnail" />
          <span id="resDuration" class="duration-badge">0:00</span>
        </div>
        <div class="video-details">
          <div>
            <div id="resTitle" class="video-title">Video Title</div>
            <div class="video-meta">
              <span id="resEngine" class="engine-tag">Engine: Auto</span>
              <span id="resStreamsCount">0 Available Streams</span>
            </div>
          </div>
          <div class="fast-actions">
            <a id="btnFastVideo" href="#" class="btn-quick-video" target="_blank">
              ⚡ Download Best Video (MP4)
            </a>
            <a id="btnFastAudio" href="#" class="btn-quick-audio" target="_blank">
              🎵 Download Audio (MP3)
            </a>
          </div>
        </div>
      </div>

      <!-- Tabs Header -->
      <div class="tabs-header">
        <button class="tab-btn active" onclick="switchTab('video')">📹 Video Streams</button>
        <button class="tab-btn" onclick="switchTab('audio')">🎵 Audio Streams</button>
      </div>

      <!-- Video Streams List -->
      <div id="videoTab">
        <table class="stream-table">
          <thead>
            <tr>
              <th>Resolution</th>
              <th>Format</th>
              <th>File Size</th>
              <th style="text-align: right;">Action</th>
            </tr>
          </thead>
          <tbody id="videoStreamsBody"></tbody>
        </table>
      </div>

      <!-- Audio Streams List -->
      <div id="audioTab" style="display: none;">
        <table class="stream-table">
          <thead>
            <tr>
              <th>Bitrate</th>
              <th>Format</th>
              <th>File Size</th>
              <th style="text-align: right;">Action</th>
            </tr>
          </thead>
          <tbody id="audioStreamsBody"></tbody>
        </table>
      </div>
    </div>

    <!-- How It Works Section -->
    <div class="how-section">
      <h2 class="how-title">How To Use AnyDownloader</h2>
      <div class="steps-grid">
        <div class="step-card">
          <div class="step-num">1</div>
          <h3>Copy Media Link</h3>
          <p>Copy the video URL from YouTube, Instagram Reels, TikTok, or Twitter.</p>
        </div>
        <div class="step-card">
          <div class="step-num">2</div>
          <h3>Paste in Box</h3>
          <p>Click the "Paste" button or paste the link directly into the search bar above.</p>
        </div>
        <div class="step-card">
          <div class="step-num">3</div>
          <h3>Download File</h3>
          <p>Select your desired resolution (1080p, 720p, 360p) or MP3 to save instantly!</p>
        </div>
      </div>
    </div>
  </main>

  <!-- Footer -->
  <footer>
    <p>Powered by ⚡ Down-API Engine Waterfall (VidsSave + SaveFrom REA + YT-DLP) | 10 Residential Proxies Active</p>
  </footer>

  <script>
    async function pasteClipboard() {
      try {
        const text = await navigator.clipboard.readText();
        if (text) {
          document.getElementById('urlInput').value = text.trim();
          handleFetch();
        }
      } catch (err) {
        document.getElementById('urlInput').focus();
      }
    }

    function switchTab(tab) {
      const vTab = document.getElementById('videoTab');
      const aTab = document.getElementById('audioTab');
      const btns = document.querySelectorAll('.tab-btn');

      if (tab === 'video') {
        vTab.style.display = 'block';
        aTab.style.display = 'none';
        btns[0].classList.add('active');
        btns[1].classList.remove('active');
      } else {
        vTab.style.display = 'none';
        aTab.style.display = 'block';
        btns[1].classList.add('active');
        btns[0].classList.remove('active');
      }
    }

    function formatBytes(bytes) {
      if (!bytes || bytes === 0) return 'Variable / Stream';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return (bytes / Math.pow(k, i)).toFixed(1) + ' ' + sizes[i];
    }

    async function handleFetch(e) {
      if (e) e.preventDefault();
      const url = document.getElementById('urlInput').value.trim();
      if (!url) return;

      const loadingBox = document.getElementById('loadingBox');
      const errorBox = document.getElementById('errorBox');
      const resultCard = document.getElementById('resultCard');
      const submitBtn = document.getElementById('submitBtn');

      loadingBox.style.display = 'block';
      errorBox.style.display = 'none';
      resultCard.style.display = 'none';
      submitBtn.disabled = true;

      try {
        const res = await fetch(`/api/info?url=${encodeURIComponent(url)}`);
        const data = await res.json();

        if (!res.ok || data.status !== 'success') {
          throw new Error(data.detail || data.message || 'Unable to fetch video details.');
        }

        // Fill Metadata
        document.getElementById('resTitle').textContent = data.title || 'Video Title';
        document.getElementById('resThumb').src = data.thumbnail || 'https://via.placeholder.com/320x180?text=No+Thumbnail';
        document.getElementById('resDuration').textContent = data.duration || 'Video';
        document.getElementById('resEngine').textContent = `Engine: ${data.engine || 'Auto'}`;

        const vList = data.videos || [];
        const aList = data.audios || [];
        document.getElementById('resStreamsCount').textContent = `${vList.length + aList.length} Qualities Available`;

        // Direct Quick 1-Click buttons
        const fastVideoUrl = `/api/download?url=${encodeURIComponent(url)}&type=video&quality=best`;
        const fastAudioUrl = `/api/download?url=${encodeURIComponent(url)}&type=audio`;
        
        document.getElementById('btnFastVideo').onclick = () => { triggerDownload(fastVideoUrl); return false; };
        document.getElementById('btnFastAudio').onclick = () => { triggerDownload(fastAudioUrl); return false; };

        // Populate Video Streams
        const vBody = document.getElementById('videoStreamsBody');
        vBody.innerHTML = '';
        if (vList.length === 0) {
          vBody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#64748b;">No video streams detected</td></tr>';
        } else {
          vList.forEach(v => {
            const row = document.createElement('tr');
            const dlLink = v.download_url || `/api/download?url=${encodeURIComponent(url)}&type=video&quality=${encodeURIComponent(v.quality)}`;
            row.innerHTML = `
              <td>
                <span class="quality-badge">${escapeHtml(v.quality || 'Video')}</span>
                ${v.has_audio ? '<span class="has-audio-tag">🔊 With Sound</span>' : ''}
              </td>
              <td><span class="format-tag">${escapeHtml(v.format || 'mp4')}</span></td>
              <td style="color:#94a3b8;">${formatBytes(v.size)}</td>
              <td style="text-align: right;">
                <button class="btn-download-sm" onclick="triggerDownload('${dlLink}')">
                  📥 Download
                </button>
              </td>
            `;
            vBody.appendChild(row);
          });
        }

        // Populate Audio Streams
        const aBody = document.getElementById('audioStreamsBody');
        aBody.innerHTML = '';
        if (aList.length === 0) {
          aBody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#64748b;">No audio streams detected</td></tr>';
        } else {
          aList.forEach(a => {
            const row = document.createElement('tr');
            const dlLink = a.download_url || `/api/download?url=${encodeURIComponent(url)}&type=audio`;
            row.innerHTML = `
              <td><span class="quality-badge">${escapeHtml(a.quality || 'Audio')}</span></td>
              <td><span class="format-tag">${escapeHtml(a.format || 'mp3')}</span></td>
              <td style="color:#94a3b8;">${formatBytes(a.size)}</td>
              <td style="text-align: right;">
                <button class="btn-download-sm" onclick="triggerDownload('${dlLink}')">
                  🎵 Download MP3
                </button>
              </td>
            `;
            aBody.appendChild(row);
          });
        }

        resultCard.style.display = 'block';
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } catch (err) {
        document.getElementById('errorMsg').textContent = err.message || 'Error occurred while fetching media.';
        errorBox.style.display = 'flex';
      } finally {
        loadingBox.style.display = 'none';
        submitBtn.disabled = false;
      }
    }

    async function triggerDownload(url) {
      // If it is already a direct CDN link (e.g. googlevideo or cdn)
      if (url.startsWith('http') && !url.includes('/api/download')) {
        window.open(url, '_blank');
        return;
      }
      
      // If it is an API download endpoint, resolve it first
      try {
        const btn = event?.currentTarget;
        const originalText = btn ? btn.innerHTML : null;
        if (btn) btn.innerHTML = '⏳ Preparing...';

        const res = await fetch(url);
        const data = await res.json();
        if (data && data.download_url) {
          window.open(data.download_url, '_blank');
        } else {
          alert('Could not resolve direct link: ' + JSON.stringify(data));
        }
        if (btn && originalText) btn.innerHTML = originalText;
      } catch (e) {
        window.open(url, '_blank');
      }
    }

    function escapeHtml(str) {
      return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
  </script>
</body>
</html>"""
