def get_downloader_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Downify — Save Any Video or Audio</title>
  <meta name="description" content="Paste any video link and download it instantly. YouTube, Shorts, TikTok, Instagram Reels, and Twitter supported. Free, fast, and no sign-up required.">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#x2193;</text></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&display=swap" rel="stylesheet">

  <style>
    /* =========================================================
       DESIGN TOKENS
       Palette: Pure neutral dark  +  Single white accent.
       No color explosions. Everything earned.
    ========================================================= */
    :root {
      --bg:           #0a0a0a;
      --bg-raised:    #111111;
      --bg-elevated:  #181818;
      --line:         rgba(255,255,255,0.08);
      --line-hover:   rgba(255,255,255,0.18);
      --text-hi:      #ffffff;
      --text-md:      #a1a1aa;
      --text-lo:      #52525b;
      --accent:       #ffffff;
      --accent-bg:    rgba(255,255,255,0.08);
      --danger:       #ef4444;
      --success:      #22c55e;
      --r-sm:         8px;
      --r-md:         14px;
      --r-lg:         20px;
      --r-pill:       999px;
      --font:         'Geist', system-ui, -apple-system, sans-serif;
      --ease-out:     cubic-bezier(0.16, 1, 0.3, 1);
    }

    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    html {
      font-family: var(--font);
      background: var(--bg);
      color: var(--text-md);
      min-height: 100%;
      -webkit-font-smoothing: antialiased;
    }

    body {
      min-height: 100dvh;
      overflow-x: hidden;
    }

    /* =========================================================
       HEADER
    ========================================================= */
    .site-header {
      position: sticky;
      top: 0;
      z-index: 50;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      height: 56px;
      background: rgba(10,10,10,0.80);
      backdrop-filter: blur(16px) saturate(1.4);
      -webkit-backdrop-filter: blur(16px) saturate(1.4);
      border-bottom: 1px solid var(--line);
    }

    .logo {
      display: flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      color: var(--text-hi);
    }

    .logo-mark {
      width: 30px;
      height: 30px;
      background: var(--text-hi);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .logo-mark svg {
      color: #0a0a0a;
    }

    .logo-name {
      font-size: 16px;
      font-weight: 600;
      letter-spacing: -0.3px;
      color: var(--text-hi);
    }

    .header-nav {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .nav-item {
      color: var(--text-md);
      text-decoration: none;
      font-size: 13px;
      font-weight: 500;
      padding: 6px 12px;
      border-radius: var(--r-sm);
      transition: color 0.15s, background 0.15s;
    }
    .nav-item:hover {
      color: var(--text-hi);
      background: var(--accent-bg);
    }

    /* =========================================================
       PAGE CONTAINER
    ========================================================= */
    .page {
      display: flex;
      flex-direction: column;
      min-height: calc(100dvh - 56px);
    }

    /* =========================================================
       HERO SECTION
    ========================================================= */
    .hero {
      padding: 72px 24px 48px;
      text-align: center;
      max-width: 680px;
      margin: 0 auto;
      width: 100%;
    }

    .hero-eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 500;
      color: var(--text-lo);
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-bottom: 20px;
    }
    .eyebrow-dot {
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: var(--success);
    }

    .hero-title {
      font-size: clamp(30px, 6vw, 52px);
      font-weight: 700;
      letter-spacing: -1.5px;
      line-height: 1.1;
      color: var(--text-hi);
      margin-bottom: 14px;
    }

    .hero-sub {
      font-size: 15px;
      color: var(--text-md);
      line-height: 1.65;
      max-width: 440px;
      margin: 0 auto 36px;
    }

    /* =========================================================
       DOWNLOAD BOX  —  The whole product lives here
    ========================================================= */
    .download-box {
      background: var(--bg-raised);
      border: 1px solid var(--line);
      border-radius: var(--r-lg);
      overflow: hidden;
      transition: border-color 0.2s;
    }
    .download-box:focus-within {
      border-color: var(--line-hover);
    }

    /* URL Input Bar */
    .input-bar {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 10px 10px 16px;
    }

    .input-bar-icon {
      color: var(--text-lo);
      flex-shrink: 0;
      display: flex;
    }

    .url-input {
      flex: 1;
      min-width: 0;
      background: transparent;
      border: none;
      outline: none;
      color: var(--text-hi);
      font-family: var(--font);
      font-size: 15px;
      caret-color: var(--text-hi);
    }
    .url-input::placeholder {
      color: var(--text-lo);
    }

    .btn-clear-input {
      background: none;
      border: none;
      color: var(--text-lo);
      cursor: pointer;
      display: none;
      align-items: center;
      padding: 4px;
      border-radius: 50%;
      transition: color 0.15s;
      flex-shrink: 0;
    }
    .btn-clear-input:hover { color: var(--text-md); }

    .btn-paste {
      background: var(--bg-elevated);
      border: 1px solid var(--line);
      color: var(--text-md);
      font-family: var(--font);
      font-size: 13px;
      font-weight: 500;
      padding: 7px 12px;
      border-radius: var(--r-sm);
      cursor: pointer;
      white-space: nowrap;
      flex-shrink: 0;
      transition: color 0.15s, border-color 0.15s, background 0.15s;
    }
    .btn-paste:hover {
      color: var(--text-hi);
      border-color: var(--line-hover);
    }

    /* Full-width Download button at base of box */
    .btn-download-main {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 14px 20px;
      background: var(--text-hi);
      color: #0a0a0a;
      font-family: var(--font);
      font-size: 15px;
      font-weight: 600;
      border: none;
      border-top: 1px solid var(--line);
      cursor: pointer;
      letter-spacing: -0.2px;
      transition: background 0.15s, transform 0.15s var(--ease-out);
    }
    .btn-download-main:hover {
      background: #e4e4e7;
    }
    .btn-download-main:active {
      transform: scale(0.99);
    }
    .btn-download-main:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }

    /* Platform Chips */
    .platforms-row {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
      padding: 12px 16px;
      border-top: 1px solid var(--line);
    }

    .platforms-label {
      font-size: 11px;
      color: var(--text-lo);
      font-weight: 500;
      white-space: nowrap;
    }

    .platform-chip {
      font-size: 11px;
      font-weight: 500;
      color: var(--text-lo);
      background: transparent;
      border: 1px solid var(--line);
      padding: 3px 9px;
      border-radius: var(--r-pill);
      cursor: default;
    }

    /* =========================================================
       LOADING STATE
    ========================================================= */
    .loading-panel {
      display: none;
      flex-direction: column;
      align-items: center;
      gap: 14px;
      padding: 48px 24px;
      text-align: center;
    }

    .spinner-wrap {
      position: relative;
      width: 44px;
      height: 44px;
    }
    .spinner-ring {
      position: absolute;
      inset: 0;
      border-radius: 50%;
      border: 2px solid var(--line);
      border-top-color: var(--text-hi);
      animation: spin 0.9s linear infinite;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    .loading-title {
      font-size: 15px;
      font-weight: 600;
      color: var(--text-hi);
    }
    .loading-sub {
      font-size: 13px;
      color: var(--text-lo);
      min-height: 20px;
    }

    /* =========================================================
       ERROR STATE
    ========================================================= */
    .error-panel {
      display: none;
      align-items: flex-start;
      gap: 12px;
      max-width: 600px;
      margin: 24px auto 0;
      padding: 14px 18px;
      background: rgba(239,68,68,0.08);
      border: 1px solid rgba(239,68,68,0.25);
      border-radius: var(--r-md);
      font-size: 13px;
      color: #fca5a5;
      text-align: left;
    }
    .error-icon { flex-shrink: 0; color: var(--danger); }

    /* =========================================================
       RESULTS SECTION
    ========================================================= */
    .results-section {
      display: none;
      max-width: 760px;
      margin: 32px auto 0;
      padding: 0 24px;
      width: 100%;
      animation: fade-up 0.4s var(--ease-out);
    }
    @keyframes fade-up {
      from { opacity: 0; transform: translateY(20px); }
      to   { opacity: 1; transform: translateY(0); }
    }

    /* Media preview card */
    .media-card {
      background: var(--bg-raised);
      border: 1px solid var(--line);
      border-radius: var(--r-lg);
      overflow: hidden;
      margin-bottom: 20px;
    }

    .media-card-inner {
      display: flex;
      gap: 18px;
      padding: 18px;
    }

    .thumbnail-box {
      position: relative;
      width: 220px;
      min-width: 220px;
      aspect-ratio: 16/9;
      border-radius: var(--r-sm);
      overflow: hidden;
      background: var(--bg-elevated);
      flex-shrink: 0;
    }
    .thumbnail-box img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    .thumb-dur {
      position: absolute;
      bottom: 6px;
      right: 6px;
      background: rgba(0,0,0,0.75);
      color: #fff;
      font-size: 11px;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 4px;
    }

    .media-info {
      flex: 1;
      min-width: 0;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
    }

    .media-title {
      font-size: 16px;
      font-weight: 600;
      color: var(--text-hi);
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .media-quick-row {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .btn-quick {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-family: var(--font);
      font-size: 13px;
      font-weight: 600;
      padding: 9px 14px;
      border-radius: var(--r-sm);
      cursor: pointer;
      border: 1px solid var(--line);
      transition: all 0.15s;
    }
    .btn-quick.primary {
      background: var(--text-hi);
      color: #0a0a0a;
      border-color: transparent;
    }
    .btn-quick.primary:hover { background: #e4e4e7; }
    .btn-quick.secondary {
      background: transparent;
      color: var(--text-md);
    }
    .btn-quick.secondary:hover {
      border-color: var(--line-hover);
      color: var(--text-hi);
    }
    .btn-quick:active { transform: scale(0.97); }

    /* Format tabs */
    .tabs-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--line);
      margin-bottom: 16px;
      padding-bottom: 1px;
      flex-wrap: wrap;
      gap: 8px;
    }

    .tab-group {
      display: flex;
      gap: 2px;
    }

    .tab-btn {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-family: var(--font);
      font-size: 13px;
      font-weight: 500;
      color: var(--text-lo);
      background: none;
      border: none;
      padding: 10px 14px;
      border-bottom: 2px solid transparent;
      cursor: pointer;
      transition: color 0.15s;
      margin-bottom: -1px;
      white-space: nowrap;
    }
    .tab-btn:hover { color: var(--text-md); }
    .tab-btn.active {
      color: var(--text-hi);
      border-bottom-color: var(--text-hi);
    }

    .tab-hint {
      font-size: 12px;
      color: var(--text-lo);
      white-space: nowrap;
    }

    /* Format grid */
    .formats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
      gap: 10px;
      margin-bottom: 80px;
    }

    .format-card {
      background: var(--bg-raised);
      border: 1px solid var(--line);
      border-radius: var(--r-md);
      padding: 16px;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 14px;
      transition: border-color 0.15s, background 0.15s;
    }
    .format-card:hover {
      border-color: var(--line-hover);
      background: var(--bg-elevated);
    }
    .format-card.selected {
      border-color: rgba(255,255,255,0.4);
      background: var(--bg-elevated);
    }

    .fc-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }

    .fc-quality {
      font-size: 22px;
      font-weight: 700;
      color: var(--text-hi);
      letter-spacing: -0.5px;
      line-height: 1;
    }
    .fc-quality-sub {
      font-size: 11px;
      font-weight: 500;
      color: var(--text-lo);
      margin-top: 2px;
    }

    .fc-badge {
      font-size: 10px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: var(--r-pill);
      border: 1px solid var(--line);
      color: var(--text-lo);
      white-space: nowrap;
    }
    .fc-badge.best {
      border-color: rgba(255,255,255,0.25);
      color: var(--text-hi);
    }

    .fc-specs {
      display: flex;
      flex-direction: column;
      gap: 5px;
      font-size: 12px;
      color: var(--text-lo);
      border-top: 1px solid var(--line);
      padding-top: 10px;
    }
    .fc-spec-row {
      display: flex;
      justify-content: space-between;
    }
    .fc-spec-row span:last-child {
      color: var(--text-md);
      font-weight: 500;
    }

    .btn-dl-card {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 7px;
      font-family: var(--font);
      font-size: 13px;
      font-weight: 600;
      padding: 9px;
      border-radius: var(--r-sm);
      border: 1px solid var(--line);
      background: transparent;
      color: var(--text-md);
      cursor: pointer;
      transition: all 0.15s;
    }
    .format-card:hover .btn-dl-card,
    .format-card.selected .btn-dl-card {
      background: var(--text-hi);
      color: #0a0a0a;
      border-color: transparent;
    }
    .btn-dl-card:active { transform: scale(0.98); }

    /* =========================================================
       STICKY BOTTOM BAR  (shows only after extraction)
    ========================================================= */
    .sticky-bar {
      display: none;
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 40;
      background: rgba(10,10,10,0.90);
      backdrop-filter: blur(16px) saturate(1.4);
      -webkit-backdrop-filter: blur(16px) saturate(1.4);
      border-top: 1px solid var(--line);
      padding: 12px 20px;
      padding-bottom: max(12px, env(safe-area-inset-bottom));
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    .sticky-info {
      display: flex;
      flex-direction: column;
      gap: 2px;
      min-width: 0;
    }
    .sticky-sel {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-hi);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .sticky-sub {
      font-size: 12px;
      color: var(--text-lo);
    }

    .sticky-actions {
      display: flex;
      gap: 8px;
      flex-shrink: 0;
    }
    .sticky-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: var(--font);
      font-size: 13px;
      font-weight: 600;
      padding: 10px 16px;
      border-radius: var(--r-sm);
      cursor: pointer;
      border: 1px solid var(--line);
      transition: all 0.15s;
      white-space: nowrap;
    }
    .sticky-btn.primary {
      background: var(--text-hi);
      color: #0a0a0a;
      border-color: transparent;
    }
    .sticky-btn.primary:hover { background: #e4e4e7; }
    .sticky-btn.secondary {
      background: transparent;
      color: var(--text-md);
    }
    .sticky-btn.secondary:hover {
      color: var(--text-hi);
      border-color: var(--line-hover);
    }

    /* =========================================================
       TRUST FEATURES STRIP
    ========================================================= */
    .features-strip {
      border-top: 1px solid var(--line);
      margin-top: auto;
      padding: 36px 24px;
    }
    .features-inner {
      max-width: 760px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 32px;
    }
    .feature-item {}
    .feature-item-title {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-hi);
      margin-bottom: 6px;
    }
    .feature-item-desc {
      font-size: 13px;
      color: var(--text-lo);
      line-height: 1.55;
    }

    /* =========================================================
       FOOTER
    ========================================================= */
    footer {
      border-top: 1px solid var(--line);
      padding: 20px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }
    .footer-copy {
      font-size: 12px;
      color: var(--text-lo);
    }
    .footer-links {
      display: flex;
      gap: 16px;
    }
    .footer-links a {
      font-size: 12px;
      color: var(--text-lo);
      text-decoration: none;
      transition: color 0.15s;
    }
    .footer-links a:hover { color: var(--text-md); }

    /* =========================================================
       TOAST
    ========================================================= */
    .toast-stack {
      position: fixed;
      top: 70px;
      right: 20px;
      z-index: 100;
      display: flex;
      flex-direction: column;
      gap: 8px;
      pointer-events: none;
    }
    .toast {
      background: var(--bg-elevated);
      border: 1px solid var(--line-hover);
      color: var(--text-hi);
      font-size: 13px;
      font-weight: 500;
      padding: 10px 16px;
      border-radius: var(--r-md);
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
      animation: toast-in 0.3s var(--ease-out);
      transition: opacity 0.25s, transform 0.25s;
      max-width: 320px;
      pointer-events: auto;
    }
    @keyframes toast-in {
      from { opacity: 0; transform: translateY(-10px); }
      to   { opacity: 1; transform: translateY(0); }
    }

    /* =========================================================
       RESPONSIVE
    ========================================================= */
    @media (max-width: 640px) {
      .hero { padding: 44px 16px 32px; }
      .hero-title { letter-spacing: -1px; }

      .input-bar { flex-wrap: wrap; gap: 8px; }
      .btn-paste { order: 3; width: 100%; justify-content: center; }
      .btn-download-main { font-size: 14px; }

      .platforms-row { flex-wrap: nowrap; overflow-x: auto; padding: 10px 12px; scrollbar-width: none; }
      .platforms-row::-webkit-scrollbar { display: none; }
      .platform-chip { flex-shrink: 0; }

      .media-card-inner { flex-direction: column; gap: 14px; }
      .thumbnail-box { width: 100%; min-width: 0; }
      .media-title { font-size: 15px; }

      .btn-quick { font-size: 13px; }
      .media-quick-row { flex-direction: column; }
      .btn-quick { width: 100%; justify-content: center; }

      .formats-grid { grid-template-columns: 1fr; }

      .sticky-bar { flex-direction: column; align-items: stretch; gap: 10px; }
      .sticky-actions { flex-direction: column; }
      .sticky-btn { justify-content: center; }

      .features-inner { grid-template-columns: 1fr; gap: 20px; }

      .footer { flex-direction: column; align-items: flex-start; }
      .nav-item { display: none; }

      .toast-stack { right: 12px; left: 12px; }
      .toast { max-width: 100%; }
    }
  </style>
</head>
<body>

  <!-- Header -->
  <header class="site-header">
    <a href="/" class="logo">
      <div class="logo-mark">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
          <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
        </svg>
      </div>
      <span class="logo-name">Downify</span>
    </a>
    <nav class="header-nav">
      <a href="/docs" target="_blank" class="nav-item">API</a>
    </nav>
  </header>

  <div class="page">

    <!-- Hero -->
    <section class="hero">
      <div class="hero-eyebrow">
        <span class="eyebrow-dot"></span>
        Free &amp; always available
      </div>

      <h1 class="hero-title">Save any video<br>in seconds.</h1>

      <p class="hero-sub">
        Paste a link from YouTube, TikTok, Instagram, or Twitter. Pick your quality. Download.
      </p>

      <!-- Download Box -->
      <div class="download-box" id="downloadBox">
        <div class="input-bar">
          <div class="input-bar-icon">
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
            </svg>
          </div>
          <form id="mainForm" onsubmit="onSubmit(event)" style="display:contents;">
            <input
              type="url"
              id="urlInput"
              class="url-input"
              placeholder="Paste a video link here..."
              autocomplete="off"
              required
              oninput="onInputChange(this.value)"
            >
            <button type="button" id="btnClear" class="btn-clear-input" onclick="clearUrl()" aria-label="Clear">
              <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path d="M18 6L6 18M6 6l12 12"/>
              </svg>
            </button>
          </form>
          <button type="button" class="btn-paste" onclick="paste()">Paste</button>
        </div>

        <!-- Full-width submit (tied to form above) -->
        <button type="submit" id="btnSubmit" class="btn-download-main" onclick="onSubmit()">
          <svg width="17" height="17" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
            <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
          </svg>
          Get Download Links
        </button>

        <div class="platforms-row">
          <span class="platforms-label">Supports</span>
          <span class="platform-chip">YouTube</span>
          <span class="platform-chip">Shorts</span>
          <span class="platform-chip">TikTok</span>
          <span class="platform-chip">Instagram</span>
          <span class="platform-chip">Twitter / X</span>
        </div>
      </div>

      <!-- Loading -->
      <div class="loading-panel" id="loadingPanel" style="display:none; flex-direction:column;">
        <div class="spinner-wrap">
          <div class="spinner-ring"></div>
        </div>
        <div class="loading-title">Finding your video...</div>
        <div class="loading-sub" id="loadingMsg">Just a moment</div>
      </div>

      <!-- Error -->
      <div class="error-panel" id="errorPanel">
        <div class="error-icon">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/>
          </svg>
        </div>
        <div id="errorMsg">Something went wrong. Please check the link and try again.</div>
      </div>
    </section>

    <!-- Results -->
    <section class="results-section" id="resultsSection">

      <!-- Media preview -->
      <div class="media-card">
        <div class="media-card-inner">
          <div class="thumbnail-box">
            <img id="thumbImg" src="" alt="Video thumbnail">
            <div class="thumb-dur" id="thumbDur"></div>
          </div>
          <div class="media-info">
            <h2 class="media-title" id="mediaTitle">Video Title</h2>
            <div class="media-quick-row">
              <button class="btn-quick primary" onclick="downloadSelected()">
                <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
                  <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                </svg>
                Save Video (Best)
              </button>
              <button class="btn-quick secondary" onclick="downloadMp3()">
                <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
                  <path d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"/>
                </svg>
                Save as MP3
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Format tabs -->
      <div class="tabs-row">
        <div class="tab-group">
          <button class="tab-btn active" id="tabVideo" onclick="setTab('video')">
            <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
            </svg>
            <span id="lblVideo">Video</span>
          </button>
          <button class="tab-btn" id="tabAudio" onclick="setTab('audio')">
            <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M9 19V6l12-3v13"/>
            </svg>
            <span id="lblAudio">Audio (MP3)</span>
          </button>
        </div>
        <span class="tab-hint">Click any format to download</span>
      </div>

      <!-- Format grids -->
      <div class="formats-grid" id="videoGrid"></div>
      <div class="formats-grid" id="audioGrid" style="display:none;"></div>

    </section>

    <!-- Features strip -->
    <div class="features-strip" id="featuresStrip">
      <div class="features-inner">
        <div class="feature-item">
          <div class="feature-item-title">No sign-up needed</div>
          <div class="feature-item-desc">Paste a link and download. No account, no email, no waiting.</div>
        </div>
        <div class="feature-item">
          <div class="feature-item-title">Multiple quality options</div>
          <div class="feature-item-desc">Pick from 1080p, 720p, and more — or just grab the best available.</div>
        </div>
        <div class="feature-item">
          <div class="feature-item-title">Video &amp; audio</div>
          <div class="feature-item-desc">Download full video or extract just the audio as an MP3 file.</div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer>
      <span class="footer-copy">Downify — 2025</span>
      <div class="footer-links">
        <a href="/docs" target="_blank">API</a>
        <a href="/logs" target="_blank">Status</a>
      </div>
    </footer>

  </div>

  <!-- Sticky action bar (shown after extraction) -->
  <div class="sticky-bar" id="stickyBar">
    <div class="sticky-info">
      <span class="sticky-sel" id="stickySelTitle">Best quality selected</span>
      <span class="sticky-sub" id="stickySelSub">Tap to download</span>
    </div>
    <div class="sticky-actions">
      <button class="sticky-btn primary" onclick="downloadSelected()">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
          <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
        </svg>
        Download Video
      </button>
      <button class="sticky-btn secondary" onclick="downloadMp3()">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
          <path d="M9 19V6l12-3v13"/>
        </svg>
        Download MP3
      </button>
    </div>
  </div>

  <!-- Toast stack -->
  <div class="toast-stack" id="toastStack"></div>

  <script>
    /* =====================================================
       STATE
    ===================================================== */
    let currentUrl = "";
    let selectedItem = null;
    let selectedType = "video";

    /* =====================================================
       INPUT HELPERS
    ===================================================== */
    function onInputChange(val) {
      document.getElementById('btnClear').style.display = val ? 'flex' : 'none';
    }

    function clearUrl() {
      const inp = document.getElementById('urlInput');
      inp.value = '';
      onInputChange('');
      inp.focus();
    }

    async function paste() {
      try {
        const text = await navigator.clipboard.readText();
        if (text && text.trim()) {
          const inp = document.getElementById('urlInput');
          inp.value = text.trim();
          onInputChange(inp.value);
          toast("Link pasted");
          onSubmit();
        }
      } catch {
        document.getElementById('urlInput').focus();
      }
    }

    /* =====================================================
       TOAST
    ===================================================== */
    function toast(msg) {
      const stack = document.getElementById('toastStack');
      const el = document.createElement('div');
      el.className = 'toast';
      el.innerHTML = `
        <svg width="15" height="15" fill="none" stroke="#22c55e" stroke-width="2.2" viewBox="0 0 24 24">
          <path d="M5 13l4 4L19 7"/>
        </svg>
        <span>${esc(msg)}</span>
      `;
      stack.appendChild(el);
      setTimeout(() => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(-8px)';
        setTimeout(() => el.remove(), 260);
      }, 3000);
    }

    /* =====================================================
       TABS
    ===================================================== */
    function setTab(mode) {
      const vG = document.getElementById('videoGrid');
      const aG = document.getElementById('audioGrid');
      document.getElementById('tabVideo').classList.toggle('active', mode === 'video');
      document.getElementById('tabAudio').classList.toggle('active', mode === 'audio');
      vG.style.display = mode === 'video' ? 'grid' : 'none';
      aG.style.display = mode === 'audio' ? 'grid' : 'none';
    }

    /* =====================================================
       FORMAT HELPERS
    ===================================================== */
    function fmtSize(bytes) {
      if (!bytes || isNaN(bytes) || bytes === 0) return '';
      const k = 1024;
      const u = ['B','KB','MB','GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return (bytes / Math.pow(k, i)).toFixed(1) + ' ' + u[i];
    }

    function fmtQuality(q) {
      return String(q || 'HD').replace(/p$/i, '').trim();
    }

    /* =====================================================
       MAIN EXTRACTION
    ===================================================== */
    async function onSubmit(e) {
      if (e && e.preventDefault) e.preventDefault();
      const url = document.getElementById('urlInput').value.trim();
      if (!url) return;

      currentUrl = url;

      const loading = document.getElementById('loadingPanel');
      const error   = document.getElementById('errorPanel');
      const results = document.getElementById('resultsSection');
      const bar     = document.getElementById('stickyBar');
      const submit  = document.getElementById('btnSubmit');
      const features = document.getElementById('featuresStrip');
      const msgEl   = document.getElementById('loadingMsg');

      // Show loading state
      loading.style.display = 'flex';
      error.style.display   = 'none';
      results.style.display = 'none';
      bar.style.display     = 'none';
      submit.disabled       = true;

      const msgs = ["Just a moment", "Fetching video info…", "Almost there…"];
      let mi = 0;
      const msgTimer = setInterval(() => {
        mi = (mi + 1) % msgs.length;
        msgEl.textContent = msgs[mi];
      }, 2000);

      try {
        const res  = await fetch(`/api/info?url=${encodeURIComponent(url)}`);
        const data = await res.json();

        if (!res.ok || data.status !== 'success') {
          throw new Error(data.detail || data.message || 'Could not read this link.');
        }

        clearInterval(msgTimer);
        renderResults(data, url);
        features.style.display = 'none';
        loading.style.display  = 'none';

      } catch (err) {
        clearInterval(msgTimer);
        loading.style.display = 'none';
        document.getElementById('errorMsg').textContent =
          err.message || 'Something went wrong. Please check the link and try again.';
        error.style.display = 'flex';
      } finally {
        submit.disabled = false;
      }
    }

    /* =====================================================
       RENDER RESULTS
    ===================================================== */
    function renderResults(data, url) {
      // Thumbnail & title
      document.getElementById('thumbImg').src = data.thumbnail || '';
      document.getElementById('thumbDur').textContent = data.duration || '';
      document.getElementById('mediaTitle').textContent = data.title || 'Video';

      const videos = data.videos || [];
      const audios = data.audios || [];
      document.getElementById('lblVideo').textContent = `Video (${videos.length})`;
      document.getElementById('lblAudio').textContent = `Audio / MP3 (${audios.length})`;

      // Build video grid
      const vG = document.getElementById('videoGrid');
      vG.innerHTML = '';
      videos.forEach((v, i) => {
        const streamUrl = `/api/stream?url=${encodeURIComponent(url)}&type=video&quality=${encodeURIComponent(v.quality)}`;
        const q = fmtQuality(v.quality);
        const qFull = String(v.quality || 'HD').toUpperCase();
        const isBest = i === 0;
        const size = fmtSize(v.size);

        const card = document.createElement('div');
        card.className = `format-card${isBest ? ' selected' : ''}`;
        card.onclick = () => pick(v, 'video', card);
        card.innerHTML = `
          <div class="fc-top">
            <div>
              <div class="fc-quality">${esc(q)}<span style="font-size:14px;color:var(--text-lo);font-weight:400;">p</span></div>
              <div class="fc-quality-sub">${esc((v.format || 'MP4').toUpperCase())} Video</div>
            </div>
            <span class="fc-badge${isBest ? ' best' : ''}">${isBest ? 'Best' : qFull}</span>
          </div>
          <div class="fc-specs">
            <div class="fc-spec-row">
              <span>Format</span><span>${esc((v.format || 'MP4').toUpperCase())}</span>
            </div>
            ${size ? `<div class="fc-spec-row"><span>Size</span><span>${size}</span></div>` : ''}
            <div class="fc-spec-row">
              <span>Sound</span><span>Included</span>
            </div>
          </div>
          <button class="btn-dl-card" onclick="event.stopPropagation(); go('${streamUrl}')">
            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
              <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
            </svg>
            Save ${esc(q)}p
          </button>
        `;
        vG.appendChild(card);
        if (isBest) pick(v, 'video', card);
      });

      // Build audio grid
      const aG = document.getElementById('audioGrid');
      aG.innerHTML = '';
      audios.forEach((a, i) => {
        const streamUrl = `/api/stream?url=${encodeURIComponent(url)}&type=audio&quality=${encodeURIComponent(a.quality || 'best')}`;
        const isBest = i === 0;
        const size = fmtSize(a.size);

        const card = document.createElement('div');
        card.className = `format-card${isBest ? ' selected' : ''}`;
        card.onclick = () => pick(a, 'audio', card);
        card.innerHTML = `
          <div class="fc-top">
            <div>
              <div class="fc-quality" style="font-size:18px;">${esc(a.quality || 'MP3')}</div>
              <div class="fc-quality-sub">MP3 Audio</div>
            </div>
            <span class="fc-badge${isBest ? ' best' : ''}">${isBest ? 'Best' : 'Audio'}</span>
          </div>
          <div class="fc-specs">
            <div class="fc-spec-row"><span>Format</span><span>MP3</span></div>
            ${size ? `<div class="fc-spec-row"><span>Size</span><span>${size}</span></div>` : ''}
          </div>
          <button class="btn-dl-card" onclick="event.stopPropagation(); go('${streamUrl}')">
            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
              <path d="M9 19V6l12-3v13"/>
            </svg>
            Save MP3
          </button>
        `;
        aG.appendChild(card);
      });

      document.getElementById('resultsSection').style.display = 'block';
      document.getElementById('stickyBar').style.display      = 'flex';
      document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
      toast("Download links ready");
    }

    /* =====================================================
       SELECTION & DOWNLOAD
    ===================================================== */
    function pick(item, type, el) {
      document.querySelectorAll('.format-card').forEach(c => c.classList.remove('selected'));
      el.classList.add('selected');
      selectedItem = item;
      selectedType = type;

      const q = item.quality || (type === 'video' ? 'Best quality' : 'Best MP3');
      const f = (item.format || (type === 'video' ? 'MP4' : 'MP3')).toUpperCase();
      const size = fmtSize(item.size);
      document.getElementById('stickySelTitle').textContent = `${q} ${f} selected`;
      document.getElementById('stickySelSub').textContent   = size ? `${size} estimated` : 'Ready to save';
    }

    function downloadSelected() {
      if (!currentUrl) return;
      const q    = selectedItem?.quality || 'best';
      const type = selectedType || 'video';
      go(`/api/stream?url=${encodeURIComponent(currentUrl)}&type=${type}&quality=${encodeURIComponent(q)}`);
    }

    function downloadMp3() {
      if (!currentUrl) return;
      go(`/api/stream?url=${encodeURIComponent(currentUrl)}&type=audio&quality=best`);
    }

    function go(url) {
      toast("Download starting…");
      window.location.href = url;
    }

    function esc(s) {
      return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    }
  </script>
</body>
</html>"""
