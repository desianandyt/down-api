def get_downloader_html() -> str:
    return r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <title>Downify — Save Any Video or Audio</title>
  <meta name="description" content="Paste any video link and download it instantly. YouTube, Shorts, TikTok, Instagram Reels, and Twitter supported. Free, fast, no sign-up required.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@500;600;700;800&family=Inter:wght@400;450;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700&display=swap" rel="stylesheet">

  <style>
    /* ============================================================
       DESIGN TOKENS & TYPOGRAPHY SYSTEM
       - Display / Headings: Geist (Bold, geometric, clean)
       - Body / Paragraphs:  Inter + Plus Jakarta Sans (World-class legibility)
       - Contrast: Calibrated WCAG AA compliant contrast for all body text
    ============================================================ */
    :root {
      --bg:          #09090b;
      --bg-raised:   #131316;
      --bg-elevated: #18181b;
      --bg-hover:    #27272a;
      --line:        rgba(255,255,255,0.08);
      --line-strong: rgba(255,255,255,0.15);
      --line-focus:  rgba(255,255,255,0.32);

      --text-hi:     #fafafa;
      --text-body:   #e4e4e7;       /* Crisp zinc-200, highly readable on OLED & LCD */
      --text-muted:  #a1a1aa;       /* Balanced zinc-400 */
      --text-subtle: #71717a;       /* Sharp zinc-500 */

      --success:     #4ade80;
      --danger:      #f87171;

      --r-xs:        6px;
      --r-sm:        10px;
      --r-md:        14px;
      --r-lg:        20px;
      --r-xl:        26px;
      --r-pill:      999px;

      --font-display: 'Geist', system-ui, -apple-system, sans-serif;
      --font-body:    'Inter', 'Plus Jakarta Sans', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono:    'Geist Mono', ui-monospace, monospace;

      --ease:        cubic-bezier(0.16, 1, 0.3, 1);
    }

    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    html {
      font-family: var(--font-body);
      background: var(--bg);
      color: var(--text-body);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      max-width: 100vw;
      overflow-x: hidden;
    }

    body {
      min-height: 100dvh;
      max-width: 100vw;
      overflow-x: hidden;
      position: relative;
      font-family: var(--font-body);
      color: var(--text-body);
      line-height: 1.6;
      /* Subtle CSS grain texture for depth */
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='0.025'/%3E%3C/svg%3E");
    }

    /* Paragraphs and typography rules */
    p {
      color: var(--text-body);
      line-height: 1.65;
    }

    /* ============================================================
       HEADER
    ============================================================ */
    .site-header {
      position: sticky;
      top: 0;
      z-index: 50;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      height: 56px;
      background: rgba(10,10,12,0.88);
      backdrop-filter: blur(20px) saturate(1.6);
      -webkit-backdrop-filter: blur(20px) saturate(1.6);
      border-bottom: 1px solid var(--line);
    }

    .logo {
      display: flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      user-select: none;
    }
    .logo-mark {
      width: 28px;
      height: 28px;
      background: var(--text-hi);
      border-radius: 7px;
      display: grid;
      place-items: center;
      flex-shrink: 0;
    }
    .logo-name {
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 700;
      letter-spacing: -0.4px;
      color: var(--text-hi);
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .live-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: var(--font-body);
      font-size: 11.5px;
      font-weight: 500;
      color: var(--text-muted);
    }
    .live-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--success);
      animation: blink 2.5s ease-in-out infinite;
    }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

    .nav-link {
      font-family: var(--font-body);
      font-size: 13px;
      font-weight: 500;
      color: var(--text-muted);
      text-decoration: none;
      padding: 5px 10px;
      border-radius: var(--r-xs);
      transition: color 0.15s;
    }
    .nav-link:hover { color: var(--text-hi); }

    /* ============================================================
       PAGE SHELL
    ============================================================ */
    .page {
      display: flex;
      flex-direction: column;
      min-height: calc(100dvh - 56px);
    }

    /* ============================================================
       HERO (Responsive 2-column on desktop >= 900px)
    ============================================================ */
    .hero-wrap {
      max-width: 1000px;
      margin: 0 auto;
      width: 100%;
      padding: 68px 32px 52px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 64px;
      align-items: start;
    }
    .hero-wrap > div {
      min-width: 0;
      max-width: 100%;
      width: 100%;
    }

    .hero-eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-family: var(--font-body);
      font-size: 11.5px;
      font-weight: 600;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 20px;
    }
    .eyebrow-dot {
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: var(--success);
      flex-shrink: 0;
    }
    .hero-title {
      font-family: var(--font-display);
      font-size: clamp(28px, 4vw, 44px);
      font-weight: 800;
      letter-spacing: -1.4px;
      line-height: 1.12;
      color: var(--text-hi);
      margin-bottom: 14px;
    }
    .hero-sub {
      font-family: var(--font-body);
      font-size: 15px;
      font-weight: 400;
      color: var(--text-body);
      line-height: 1.65;
      letter-spacing: -0.01em;
      margin-bottom: 28px;
      max-width: 480px;
    }

    .platform-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
    }
    .platform-btn {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-family: var(--font-body);
      font-size: 12px;
      font-weight: 500;
      color: var(--text-muted);
      background: var(--bg-raised);
      border: 1px solid var(--line);
      padding: 6px 12px;
      border-radius: var(--r-pill);
      cursor: pointer;
      transition: color 0.2s, border-color 0.2s, background 0.2s;
      user-select: none;
    }
    .platform-btn:hover {
      color: var(--text-hi);
      border-color: var(--line-strong);
      background: var(--bg-elevated);
    }
    .platform-btn .p-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      flex-shrink: 0;
    }

    /* ============================================================
       DOWNLOAD BOX
    ============================================================ */
    .download-box {
      width: 100%;
      max-width: 100%;
      min-width: 0;
      box-sizing: border-box;
      background: var(--bg-raised);
      border: 1px solid var(--line);
      border-radius: var(--r-xl);
      position: relative;
      overflow: hidden;
      transition: border-color 0.25s var(--ease), box-shadow 0.25s var(--ease);
    }
    .download-box:focus-within {
      border-color: var(--line-strong);
      box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.08);
    }

    .input-area {
      width: 100%;
      max-width: 100%;
      min-width: 0;
      box-sizing: border-box;
      padding: 16px 16px 10px;
    }

    .input-label {
      font-family: var(--font-body);
      font-size: 11.5px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 8px;
      display: block;
    }

    .input-row {
      display: flex;
      align-items: center;
      gap: 8px;
      width: 100%;
      max-width: 100%;
      min-width: 0;
      box-sizing: border-box;
      background: var(--bg);
      border: 1px solid var(--line);
      border-radius: var(--r-md);
      padding: 10px 10px 10px 14px;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    .input-row:focus-within {
      border-color: var(--line-focus);
      box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.12);
    }

    .url-input {
      width: 0;
      flex: 1 1 0;
      min-width: 0;
      max-width: 100%;
      box-sizing: border-box;
      background: transparent;
      border: none;
      outline: none;
      color: var(--text-hi);
      font-family: var(--font-body);
      font-size: 15px;
      caret-color: var(--text-hi);
    }
    .url-input::placeholder { color: var(--text-subtle); }

    .btn-inline {
      background: none;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      padding: 5px;
      border-radius: 6px;
      flex-shrink: 0;
      color: var(--text-muted);
      transition: color 0.15s, background 0.15s;
    }
    .btn-inline:hover { color: var(--text-hi); background: var(--bg-elevated); }

    /* Platform detection badge */
    .detected-badge {
      display: none;
      align-items: center;
      gap: 7px;
      font-family: var(--font-body);
      font-size: 11px;
      font-weight: 600;
      color: var(--text-muted);
      margin-top: 10px;
      padding: 0 2px;
    }
    .detected-badge.show { display: flex; }
    .detected-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }

    /* Submit button */
    .btn-submit {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
      padding: 14px;
      margin-top: 10px;
      background: var(--text-hi);
      color: #0d0d0d;
      font-family: var(--font-display);
      font-size: 14px;
      font-weight: 700;
      border: none;
      border-radius: var(--r-md);
      cursor: pointer;
      letter-spacing: -0.2px;
      transition: background 0.15s, transform 0.15s var(--ease), opacity 0.15s;
    }
    .btn-submit:hover  { background: #e4e4e7; }
    .btn-submit:active { transform: scale(0.985); }
    .btn-submit:disabled {
      opacity: 0.55;
      cursor: not-allowed;
      transform: none;
    }

    .input-footer {
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
      padding: 10px 16px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
      border-top: 1px solid var(--line);
    }
    .hint-text {
      font-family: var(--font-body);
      font-size: 12px;
      color: var(--text-subtle);
      max-width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .btn-try {
      font-family: var(--font-body);
      font-size: 11.5px;
      font-weight: 500;
      color: var(--text-muted);
      background: none;
      border: none;
      cursor: pointer;
      text-decoration: underline;
      text-underline-offset: 2px;
      text-decoration-color: var(--text-subtle);
      transition: color 0.15s;
      padding: 0;
    }
    .btn-try:hover { color: var(--text-hi); }

    /* ============================================================
       HISTORY PANEL
    ============================================================ */
    .history-panel {
      display: none;
      position: absolute;
      left: -1px;
      right: -1px;
      top: calc(100% + 4px);
      z-index: 60;
      background: var(--bg-raised);
      border: 1px solid var(--line-strong);
      border-radius: var(--r-lg);
      overflow: hidden;
      box-shadow: 0 16px 40px rgba(0,0,0,0.6);
      max-height: 200px;
      overflow-y: auto;
    }
    .history-panel.open { display: flex; flex-direction: column; }
    .history-title {
      font-family: var(--font-body);
      font-size: 10px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: var(--text-subtle);
      padding: 10px 14px 4px;
    }
    .history-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 14px;
      cursor: pointer;
      transition: background 0.15s;
      font-family: var(--font-body);
      font-size: 12.5px;
      color: var(--text-muted);
      border: none;
      background: none;
      text-align: left;
      width: 100%;
    }
    .history-item:hover { background: var(--bg-elevated); color: var(--text-hi); }
    .history-item svg { flex-shrink: 0; }
    .history-url {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      flex: 1;
      min-width: 0;
    }

    /* ============================================================
       LOADING SKELETON
    ============================================================ */
    .loading-wrap {
      display: none;
      padding: 16px 16px 20px;
      border-top: 1px solid var(--line);
    }
    @keyframes shimmer {
      0%   { background-position: -400px 0; }
      100% { background-position: 400px 0; }
    }
    .skel {
      border-radius: var(--r-xs);
      background: linear-gradient(90deg, var(--bg-elevated) 25%, var(--bg-hover) 50%, var(--bg-elevated) 75%);
      background-size: 800px 100%;
      animation: shimmer 1.4s ease-in-out infinite;
    }
    .skel-thumb { width: 100%; aspect-ratio: 16/9; border-radius: var(--r-sm); margin-bottom: 12px; }
    .skel-line  { height: 13px; margin-bottom: 8px; }
    .skel-line.w80 { width: 80%; }
    .skel-line.w50 { width: 50%; }
    .skel-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 16px; }
    .skel-card  { height: 90px; border-radius: var(--r-md); }

    .loading-step {
      font-family: var(--font-body);
      font-size: 12.5px;
      color: var(--text-muted);
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .step-spin {
      width: 13px; height: 13px;
      border-radius: 50%;
      border: 1.5px solid var(--line-strong);
      border-top-color: var(--text-hi);
      animation: spin 0.8s linear infinite;
      flex-shrink: 0;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    /* ============================================================
       ERROR PANEL
    ============================================================ */
    .error-panel {
      display: none;
      align-items: flex-start;
      gap: 10px;
      padding: 12px 14px;
      margin: 0 16px 16px;
      background: rgba(248,113,113,0.07);
      border: 1px solid rgba(248,113,113,0.22);
      border-radius: var(--r-sm);
      font-family: var(--font-body);
      font-size: 13px;
      color: #fca5a5;
    }
    .error-icon { flex-shrink: 0; color: var(--danger); margin-top: 1px; }
    .retry-link {
      margin-top: 5px;
      display: inline-block;
      font-family: var(--font-body);
      font-size: 11.5px;
      font-weight: 500;
      color: var(--text-muted);
      text-decoration: underline;
      text-underline-offset: 2px;
      cursor: pointer;
      background: none;
      border: none;
      padding: 0;
    }
    .retry-link:hover { color: var(--text-hi); }

    /* ============================================================
       RESULTS
    ============================================================ */
    .results-wrap {
      display: none;
      max-width: 1000px;
      margin: 0 auto 140px;
      padding: 0 32px;
      width: 100%;
      animation: fade-up 0.4s var(--ease) both;
    }
    @keyframes fade-up {
      from { opacity: 0; transform: translateY(16px); }
      to   { opacity: 1; transform: translateY(0); }
    }

    .media-row {
      display: flex;
      gap: 20px;
      align-items: flex-start;
      padding: 20px;
      background: var(--bg-raised);
      border: 1px solid var(--line);
      border-radius: var(--r-xl);
      margin-bottom: 24px;
    }

    .thumb-frame {
      position: relative;
      width: 220px;
      min-width: 220px;
      aspect-ratio: 16/9;
      border-radius: var(--r-sm);
      overflow: hidden;
      background: var(--bg-elevated);
      flex-shrink: 0;
    }
    .thumb-frame img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .thumb-dur {
      position: absolute;
      bottom: 6px;
      right: 6px;
      background: rgba(0,0,0,0.78);
      color: #fff;
      font-family: var(--font-body);
      font-size: 11px;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: 4px;
    }

    .media-details {
      flex: 1;
      min-width: 0;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .video-title {
      font-family: var(--font-display);
      font-size: 17px;
      font-weight: 700;
      color: var(--text-hi);
      line-height: 1.45;
      letter-spacing: -0.3px;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .quick-row { display: flex; gap: 8px; flex-wrap: wrap; }

    .btn-primary {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 600;
      padding: 9px 16px;
      background: var(--text-hi);
      color: #0d0d0d;
      border: none;
      border-radius: var(--r-sm);
      cursor: pointer;
      transition: background 0.15s, transform 0.15s var(--ease);
    }
    .btn-primary:hover  { background: #e4e4e7; }
    .btn-primary:active { transform: scale(0.97); }

    .btn-ghost {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 600;
      padding: 9px 16px;
      background: transparent;
      color: var(--text-muted);
      border: 1px solid var(--line);
      border-radius: var(--r-sm);
      cursor: pointer;
      transition: color 0.15s, border-color 0.15s, transform 0.15s var(--ease);
    }
    .btn-ghost:hover { color: var(--text-hi); border-color: var(--line-strong); }
    .btn-ghost:active { transform: scale(0.97); }

    /* ============================================================
       FORMAT TABS
    ============================================================ */
    .tabs-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--line);
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 8px;
    }
    .tab-grp { display: flex; }
    .tab {
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      background: none;
      border: none;
      border-bottom: 2px solid transparent;
      padding: 10px 16px;
      cursor: pointer;
      transition: color 0.15s;
      margin-bottom: -1px;
      display: flex;
      align-items: center;
      gap: 7px;
      white-space: nowrap;
    }
    .tab:hover { color: var(--text-hi); }
    .tab.active { color: var(--text-hi); border-bottom-color: var(--text-hi); }

    .tab-count {
      font-family: var(--font-body);
      font-size: 11px;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: var(--r-pill);
      background: var(--bg-elevated);
      color: var(--text-muted);
    }
    .tab.active .tab-count { background: var(--bg-hover); color: var(--text-hi); }
    .tab-hint {
      font-family: var(--font-body);
      font-size: 11.5px;
      color: var(--text-subtle);
    }

    /* ============================================================
       FORMAT CARDS
    ============================================================ */
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 10px;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
      min-width: 0;
    }

    .format-card {
      background: var(--bg-raised);
      border: 1px solid var(--line);
      border-radius: var(--r-lg);
      padding: 16px;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 12px;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
      min-width: 0;
      transition: border-color 0.2s, background 0.2s;
      animation: card-in 0.4s var(--ease) both;
      animation-delay: calc(var(--i, 0) * 50ms);
    }
    @keyframes card-in {
      from { opacity: 0; transform: translateY(10px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    .format-card:hover {
      border-color: var(--line-strong);
      background: var(--bg-elevated);
    }
    .format-card.selected {
      border-color: var(--line-focus);
      background: var(--bg-elevated);
    }

    .fc-top { display: flex; justify-content: space-between; align-items: flex-start; }

    .fc-num {
      font-family: var(--font-display);
      font-size: 32px;
      font-weight: 800;
      letter-spacing: -1px;
      color: var(--text-hi);
      line-height: 1;
    }
    .fc-unit { font-size: 14px; font-weight: 500; color: var(--text-muted); margin-left: 1px; }
    .fc-sub  {
      font-family: var(--font-body);
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 500;
      margin-top: 3px;
    }

    .fc-badge {
      font-family: var(--font-body);
      font-size: 10px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: var(--r-pill);
      border: 1px solid var(--line);
      color: var(--text-muted);
      white-space: nowrap;
      flex-shrink: 0;
    }
    .fc-badge.best {
      border-color: rgba(74,222,128,0.4);
      color: var(--success);
      background: rgba(74,222,128,0.07);
    }

    .fc-specs {
      font-family: var(--font-body);
      border-top: 1px solid var(--line);
      padding-top: 10px;
      display: flex;
      flex-direction: column;
      gap: 5px;
    }
    .fc-row {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: var(--text-muted);
    }
    .fc-row b {
      color: var(--text-body);
      font-weight: 600;
    }

    .btn-card-dl {
      width: 100%;
      max-width: 100%;
      min-width: 0;
      box-sizing: border-box;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 7px;
      font-family: var(--font-display);
      font-size: 12.5px;
      font-weight: 600;
      padding: 9px;
      border-radius: var(--r-sm);
      border: 1px solid var(--line);
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s var(--ease);
    }
    .format-card:hover .btn-card-dl,
    .format-card.selected .btn-card-dl {
      background: var(--text-hi);
      color: #0d0d0d;
      border-color: transparent;
    }
    .btn-card-dl:active { transform: scale(0.97); }

    /* ============================================================
       STICKY BOTTOM BAR
    ============================================================ */
    .sticky-bar {
      display: none;
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      margin: 0 auto;
      width: 100%;
      max-width: 1000px;
      z-index: 100;
      box-sizing: border-box;
      background: rgba(10,10,12,0.95);
      backdrop-filter: blur(20px) saturate(1.6);
      -webkit-backdrop-filter: blur(20px) saturate(1.6);
      border-top: 1px solid var(--line-strong);
      border-left: 1px solid var(--line);
      border-right: 1px solid var(--line);
      padding: 10px 20px;
      padding-bottom: max(10px, env(safe-area-inset-bottom));
      align-items: center;
      gap: 14px;
      transform: none;
      animation: bar-slide-up 0.35s var(--ease);
    }
    @keyframes bar-slide-up {
      from { transform: translateY(100%); }
      to   { transform: translateY(0); }
    }

    .sticky-thumb {
      width: 48px;
      height: 32px;
      border-radius: 5px;
      object-fit: cover;
      background: var(--bg-elevated);
      flex-shrink: 0;
      display: none;
    }
    .sticky-thumb.show { display: block; }

    .sticky-info { flex: 1; min-width: 0; }
    .sticky-title {
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 600;
      color: var(--text-hi);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .sticky-sub {
      font-family: var(--font-body);
      font-size: 11.5px;
      color: var(--text-muted);
      margin-top: 2px;
    }

    .sticky-btns { display: flex; gap: 8px; flex-shrink: 0; }

    .sticky-btn-p {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 600;
      padding: 9px 16px;
      background: var(--text-hi);
      color: #0d0d0d;
      border: none;
      border-radius: var(--r-sm);
      cursor: pointer;
      white-space: nowrap;
      transition: background 0.15s, transform 0.15s var(--ease);
    }
    .sticky-btn-p:hover  { background: #e4e4e7; }
    .sticky-btn-p:active { transform: scale(0.97); }

    .sticky-btn-s {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 600;
      padding: 9px 14px;
      background: transparent;
      color: var(--text-muted);
      border: 1px solid var(--line-strong);
      border-radius: var(--r-sm);
      cursor: pointer;
      white-space: nowrap;
      transition: color 0.15s, border-color 0.15s, transform 0.15s;
    }
    .sticky-btn-s:hover { color: var(--text-hi); border-color: var(--line-focus); }
    .sticky-btn-s:active { transform: scale(0.97); }

    /* ============================================================
       FEATURES & FOOTER
    ============================================================ */
    .features-wrap {
      border-top: 1px solid var(--line);
      padding: 48px 32px;
      margin-top: auto;
    }
    .features-inner {
      max-width: 1000px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 40px;
    }
    .feat-title {
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 700;
      color: var(--text-hi);
      letter-spacing: -0.2px;
      margin-bottom: 6px;
    }
    .feat-desc  {
      font-family: var(--font-body);
      font-size: 13.5px;
      font-weight: 400;
      color: var(--text-muted);
      line-height: 1.65;
      letter-spacing: -0.01em;
    }

    footer {
      border-top: 1px solid var(--line);
      padding: 18px 32px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }
    .footer-left {
      font-family: var(--font-body);
      font-size: 12px;
      color: var(--text-subtle);
    }
    .footer-links { display: flex; gap: 16px; }
    .footer-links a {
      font-family: var(--font-body);
      font-size: 12px;
      color: var(--text-subtle);
      text-decoration: none;
      transition: color 0.15s;
    }
    .footer-links a:hover { color: var(--text-muted); }

    /* ============================================================
       TOAST
    ============================================================ */
    .toast-stack {
      position: fixed;
      top: 68px;
      right: 20px;
      z-index: 100;
      display: flex;
      flex-direction: column;
      gap: 8px;
      pointer-events: none;
      max-width: 320px;
    }
    .toast {
      background: var(--bg-elevated);
      border: 1px solid var(--line-strong);
      color: var(--text-hi);
      font-family: var(--font-body);
      font-size: 13px;
      font-weight: 500;
      padding: 10px 14px;
      border-radius: var(--r-md);
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.6);
      animation: toast-in 0.3s var(--ease);
      transition: opacity 0.25s, transform 0.25s;
      pointer-events: auto;
      word-break: break-word;
    }
    @keyframes toast-in {
      from { opacity: 0; transform: translateX(12px); }
      to   { opacity: 1; transform: translateX(0); }
    }

    /* ============================================================
       RESPONSIVE — breakpoint at 860px (Mobile & Tablet)
    ============================================================ */
    @media (max-width: 860px) {
      .hero-wrap {
        grid-template-columns: 1fr;
        gap: 20px;
        padding: 24px 16px 20px;
      }
      .hero-eyebrow {
        margin-bottom: 8px;
        font-size: 11px;
      }
      .hero-title {
        font-size: clamp(24px, 7vw, 32px);
        margin-bottom: 8px;
        line-height: 1.15;
      }
      .hero-sub {
        max-width: 100%;
        font-size: 14px;
        line-height: 1.5;
        margin-bottom: 14px;
      }

      .platform-grid {
        flex-wrap: nowrap;
        overflow-x: auto;
        padding-bottom: 4px;
        margin-bottom: 4px;
        scrollbar-width: none;
        -webkit-overflow-scrolling: touch;
      }
      .platform-grid::-webkit-scrollbar { display: none; }
      .platform-btn { flex-shrink: 0; }

      .nav-link { display: none; }
      .live-pill { display: none; }

      .url-input { font-size: 16px; } /* Prevents iOS Safari auto-zoom on input tap */
      .results-wrap { padding: 0 16px 140px; }

      .media-row {
        flex-direction: column;
        gap: 12px;
        padding: 14px;
        border-radius: var(--r-lg);
      }
      .thumb-frame {
        width: 100%;
        min-width: 0;
      }
      .video-title {
        font-size: 15px;
        line-height: 1.4;
      }

      .quick-row {
        flex-direction: column;
        width: 100%;
        gap: 8px;
      }
      .btn-primary, .btn-ghost {
        width: 100%;
        justify-content: center;
        padding: 11px 16px;
        font-size: 13.5px;
      }

      .cards-grid {
        grid-template-columns: 1fr;
        gap: 10px;
      }
      .format-card {
        padding: 14px;
      }
      .fc-num {
        font-size: 26px;
      }
      .btn-card-dl {
        width: 100%;
        padding: 11px;
        font-size: 13px;
      }

      .sticky-bar {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        max-width: 100vw !important;
        border-left: none !important;
        border-right: none !important;
        padding: 8px 12px !important;
        padding-bottom: max(10px, env(safe-area-inset-bottom)) !important;
        gap: 8px !important;
        flex-direction: column !important;
        align-items: stretch !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
      }
      .sticky-thumb {
        display: none !important;
      }
      .sticky-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        min-width: 0;
        box-sizing: border-box;
      }
      .sticky-title {
        font-size: 12.5px;
        max-width: 65%;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .sticky-sub {
        font-size: 11px;
        margin-top: 0;
        white-space: nowrap;
      }
      .sticky-btns {
        width: 100% !important;
        display: flex !important;
        gap: 8px !important;
        box-sizing: border-box !important;
      }
      .sticky-btn-p, .sticky-btn-s {
        flex: 1 1 0 !important;
        min-width: 0 !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        justify-content: center !important;
        padding: 10px 8px !important;
        font-size: 13px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
      }

      .features-inner {
        grid-template-columns: 1fr;
        gap: 20px;
      }
      .features-wrap {
        padding: 32px 16px;
      }
      footer {
        padding: 16px;
      }

      .toast-stack {
        right: 12px;
        left: 12px;
        max-width: 100%;
      }
    }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
      }
    }
  </style>
</head>
<body>

  <!-- Hidden <a> tag for downloads -->
  <a id="dlAnchor" style="display:none;" aria-hidden="true"></a>

  <header class="site-header">
    <a href="/" class="logo">
      <div class="logo-mark">
        <svg width="14" height="14" fill="none" stroke="#0a0a0c" stroke-width="2.5" viewBox="0 0 24 24">
          <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
        </svg>
      </div>
      <span class="logo-name">Downify</span>
    </a>
    <div class="header-right">
      <div class="live-pill">
        <span class="live-dot"></span>
        <span>Online</span>
      </div>
      <a href="/docs" target="_blank" class="nav-link">API</a>
    </div>
  </header>

  <div class="page">

    <div class="hero-wrap">

      <!-- Left column: Headline + platform pills -->
      <div>
        <div class="hero-eyebrow">
          <span class="eyebrow-dot"></span>
          Free &amp; always online
        </div>
        <h1 class="hero-title">
          Save any video<br>in seconds.
        </h1>
        <p class="hero-sub">
          Paste a link from YouTube, TikTok, Instagram, or Twitter. Pick your quality. It downloads straight to your device — no apps, no sign-up.
        </p>
        <div class="platform-grid">
          <button class="platform-btn" type="button" onclick="tryUrl('https://youtube.com/shorts/nUgWZ37u9fY')">
            <span class="p-dot" style="background:#ff2020;"></span> YouTube
          </button>
          <button class="platform-btn" type="button" onclick="tryUrl('https://youtube.com/shorts/nUgWZ37u9fY')">
            <span class="p-dot" style="background:#ff4444;"></span> Shorts
          </button>
          <button class="platform-btn" type="button" onclick="tryUrl('https://www.tiktok.com/@tiktok/video/7106594312292453675')">
            <span class="p-dot" style="background:#69c9d0;"></span> TikTok
          </button>
          <button class="platform-btn" type="button" onclick="focusWithPlatform('Instagram')">
            <span class="p-dot" style="background:#e1306c;"></span> Instagram
          </button>
          <button class="platform-btn" type="button" onclick="focusWithPlatform('Twitter / X')">
            <span class="p-dot" style="background:#888;"></span> Twitter / X
          </button>
        </div>
      </div>

      <!-- Right column: Download box -->
      <div style="position:relative; width:100%; max-width:100%; min-width:0;">

        <div class="download-box" id="downloadBox">
          <form class="input-area" onsubmit="event.preventDefault(); run(); return false;">
            <label class="input-label" for="urlInput">Video link</label>
            <div class="input-row">
              <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" style="color:var(--text-subtle);flex-shrink:0;">
                <path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
              </svg>
              <input
                type="text"
                id="urlInput"
                class="url-input"
                placeholder="Paste a YouTube, TikTok, or Instagram link"
                autocomplete="off"
                autocorrect="off"
                autocapitalize="none"
                spellcheck="false"
                oninput="onType(this.value)"
                onfocus="onFocusInput()"
                onblur="onBlurInput()"
              >
              <button type="button" id="btnClear" class="btn-inline" onclick="clearInput()" style="display:none;" aria-label="Clear">
                <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path d="M18 6L6 18M6 6l12 12"/>
                </svg>
              </button>
              <button type="button" class="btn-inline" onclick="pasteLink()" aria-label="Paste" title="Paste from clipboard">
                <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                </svg>
              </button>
            </div>

            <!-- Auto-detected platform badge -->
            <div class="detected-badge" id="detectedBadge">
              <span class="detected-dot" id="detectedDot"></span>
              <span id="detectedName"></span>
            </div>

            <!-- CTA button -->
            <button type="button" id="btnSubmit" class="btn-submit" onclick="run()">
              <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
                <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
              </svg>
              <span>Download</span>
            </button>
          </form>

          <div class="input-footer">
            <span class="hint-text">YouTube, Shorts, TikTok, Instagram, Twitter</span>
            <button class="btn-try" type="button" onclick="tryUrl('https://youtube.com/shorts/nUgWZ37u9fY')">Try an example</button>
          </div>

          <!-- Error panel -->
          <div class="error-panel" id="errorPanel">
            <div class="error-icon">
              <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/>
              </svg>
            </div>
            <div>
              <div id="errorText">Something went wrong. Please check the link and try again.</div>
              <button class="retry-link" type="button" onclick="run()">Try again</button>
            </div>
          </div>

          <!-- Skeleton loading panel -->
          <div class="loading-wrap" id="loadingWrap">
            <div class="loading-step">
              <div class="step-spin"></div>
              <span id="stepText">Checking link &amp; cache…</span>
            </div>
            <div class="skel skel-thumb"></div>
            <div class="skel skel-line w80"></div>
            <div class="skel skel-line w50"></div>
            <div class="skel-cards">
              <div class="skel skel-card"></div>
              <div class="skel skel-card"></div>
            </div>
          </div>
        </div>

        <!-- History dropdown -->
        <div class="history-panel" id="historyPanel">
          <div class="history-title">Recent Searches</div>
        </div>

      </div>
    </div>

    <!-- Results -->
    <div class="results-wrap" id="resultsWrap">

      <div class="media-row">
        <div class="thumb-frame">
          <img id="thumbImg" src="" alt="thumbnail" onerror="this.onerror=null;this.src='data:image/svg+xml,<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'320\\' height=\\'180\\' fill=\\'%231d1d22\\'><rect width=\\'320\\' height=\\'180\\'/></svg>'">
          <div class="thumb-dur" id="thumbDur"></div>
        </div>
        <div class="media-details">
          <h2 class="video-title" id="videoTitle">Video</h2>
          <div class="quick-row">
            <button class="btn-primary" id="btnBestVideo" type="button" onclick="dlBest()">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
                <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
              </svg>
              Save best quality
            </button>
            <button class="btn-ghost" type="button" onclick="dlMp3()">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
                <path d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"/>
              </svg>
              Save as MP3
            </button>
          </div>
        </div>
      </div>

      <div class="tabs-bar">
        <div class="tab-grp">
          <button class="tab active" id="tabV" type="button" onclick="setTab('video')">
            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
            </svg>
            Video
            <span class="tab-count" id="cntV">0</span>
          </button>
          <button class="tab" id="tabA" type="button" onclick="setTab('audio')">
            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M9 19V6l12-3v13"/>
            </svg>
            Audio
            <span class="tab-count" id="cntA">0</span>
          </button>
        </div>
        <span class="tab-hint">Click any format to download</span>
      </div>

      <div class="cards-grid" id="videoGrid"></div>
      <div class="cards-grid" id="audioGrid" style="display:none;"></div>

    </div>

    <!-- Features -->
    <div class="features-wrap" id="featuresWrap">
      <div class="features-inner">
        <div>
          <div class="feat-title">No account needed</div>
          <div class="feat-desc">Paste a link, choose a quality, and your file starts downloading. Nothing else required.</div>
        </div>
        <div>
          <div class="feat-title">Every quality, every format</div>
          <div class="feat-desc">Pick from HD 1080p, 720p, and lower resolutions — or save just the audio as an MP3.</div>
        </div>
        <div>
          <div class="feat-title">Works on any device</div>
          <div class="feat-desc">iPhone, Android, laptop, or desktop — same clean experience across every screen.</div>
        </div>
      </div>
    </div>

    <footer>
      <span class="footer-left">Downify &mdash; 2025</span>
      <div class="footer-links">
        <a href="/docs" target="_blank">API docs</a>
        <a href="/logs" target="_blank">Service status</a>
      </div>
    </footer>

  </div>

  <!-- Sticky bar -->
  <div class="sticky-bar" id="stickyBar">
    <img class="sticky-thumb" id="stickyThumb" src="" alt="">
    <div class="sticky-info">
      <div class="sticky-title" id="stickyTitle">Best quality selected</div>
      <div class="sticky-sub"  id="stickySub">Ready to download</div>
    </div>
    <div class="sticky-btns">
      <button class="sticky-btn-p" type="button" onclick="dlSelected()">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
          <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
        </svg>
        Download
      </button>
      <button class="sticky-btn-s" type="button" onclick="dlMp3()">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
          <path d="M9 19V6l12-3v13"/>
        </svg>
        MP3
      </button>
    </div>
  </div>

  <div class="toast-stack" id="toastStack"></div>

  <script>
    /* ============================================================
       STATE & VALIDATION CONTROLLERS
    ============================================================ */
    let currentUrl       = "";
    let selectedQuality  = null;
    let selectedType     = "video";
    let bestVideoUrl     = "";
    let bestAudioUrl     = "";
    let isExtracting     = false;
    let lastRenderedUrl  = "";
    let lastRenderedTime = 0;

    const HISTORY_KEY = "downify_history";
    const MAX_HIST    = 5;

    /* ============================================================
       HISTORY
    ============================================================ */
    function getHistory() {
      try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]"); } catch { return []; }
    }
    function pushHistory(url) {
      let h = getHistory().filter(u => u !== url);
      h.unshift(url);
      if (h.length > MAX_HIST) h = h.slice(0, MAX_HIST);
      try { localStorage.setItem(HISTORY_KEY, JSON.stringify(h)); } catch {}
    }
    function renderHistory() {
      const h = getHistory();
      const panel = document.getElementById('historyPanel');
      panel.querySelectorAll('.history-item').forEach(el => el.remove());
      if (!h.length) { panel.classList.remove('open'); return; }

      h.forEach(url => {
        const btn = document.createElement('button');
        btn.className = 'history-item';
        btn.type = 'button';
        btn.innerHTML = `
          <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <polyline points="12 8 12 12 14 14"/><circle cx="12" cy="12" r="10"/>
          </svg>
          <span class="history-url">${esc(url)}</span>
        `;
        btn.onmousedown = (e) => {
          e.preventDefault();
          document.getElementById('urlInput').value = url;
          onType(url);
          panel.classList.remove('open');
          run();
        };
        panel.appendChild(btn);
      });
      panel.classList.add('open');
    }

    /* ============================================================
       PLATFORM DETECTION
    ============================================================ */
    const PLATFORMS = [
      { match: v => v.includes('youtube.com/shorts'), name: 'YouTube Shorts', color: '#ff4444' },
      { match: v => v.includes('youtube.com') || v.includes('youtu.be'), name: 'YouTube', color: '#ff2020' },
      { match: v => v.includes('tiktok.com'), name: 'TikTok', color: '#69c9d0' },
      { match: v => v.includes('instagram.com'), name: 'Instagram', color: '#e1306c' },
      { match: v => v.includes('twitter.com') || v.includes('x.com'), name: 'Twitter / X', color: '#a0a0a0' },
      { match: v => v.includes('facebook.com') || v.includes('fb.watch'), name: 'Facebook', color: '#1877f2' },
    ];

    function detectPlatform(url) {
      const lc = url.toLowerCase();
      for (const p of PLATFORMS) { if (p.match(lc)) return p; }
      return null;
    }

    /* ============================================================
       INPUT HANDLERS
    ============================================================ */
    function onType(val) {
      document.getElementById('btnClear').style.display = val ? 'flex' : 'none';

      const badge = document.getElementById('detectedBadge');
      const p = detectPlatform(val);
      if (p && (val.startsWith('http') || val.includes('.'))) {
        document.getElementById('detectedDot').style.background = p.color;
        document.getElementById('detectedName').textContent = p.name + ' detected';
        badge.classList.add('show');
      } else {
        badge.classList.remove('show');
      }
    }

    function clearInput() {
      const inp = document.getElementById('urlInput');
      inp.value = '';
      onType('');
      document.getElementById('historyPanel').classList.remove('open');
      inp.focus();
    }

    function onFocusInput() {
      const val = document.getElementById('urlInput').value;
      if (!val) renderHistory();
    }

    function onBlurInput() {
      setTimeout(() => {
        document.getElementById('historyPanel').classList.remove('open');
      }, 240);
    }

    async function pasteLink() {
      try {
        const text = await navigator.clipboard.readText();
        if (text && text.trim()) {
          document.getElementById('urlInput').value = text.trim();
          onType(text.trim());
          toast("Link pasted from clipboard");
          run();
        }
      } catch {
        document.getElementById('urlInput').focus();
      }
    }

    function tryUrl(url) {
      document.getElementById('urlInput').value = url;
      onType(url);
      run();
    }

    function focusWithPlatform(platformName) {
      const inp = document.getElementById('urlInput');
      inp.focus();
      toast("Paste your " + platformName + " link to download");
    }

    function onFormSubmit(e) {
      e.preventDefault();
      run();
    }

    function showInlineError(msg) {
      document.getElementById('errorText').textContent = msg;
      document.getElementById('errorPanel').style.display = 'flex';
      document.getElementById('errorPanel').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    /* ============================================================
       TABS
    ============================================================ */
    function setTab(mode) {
      document.getElementById('videoGrid').style.display = mode === 'video' ? 'grid' : 'none';
      document.getElementById('audioGrid').style.display = mode === 'audio' ? 'grid' : 'none';
      document.getElementById('tabV').classList.toggle('active', mode === 'video');
      document.getElementById('tabA').classList.toggle('active', mode === 'audio');
    }

    /* ============================================================
       CLIENT-SIDE BACKGROUND FALLBACK ENGINE
       (Bypasses server blocks/proxies by extracting on user device)
    ============================================================ */
    function extractYouTubeId(url) {
      if (!url) return null;
      const m = url.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|shorts\/|live\/|watch\?.+&v=))([\w-]{11})/i);
      return m ? m[1] : null;
    }

    function fmtDur(seconds) {
      if (!seconds || isNaN(seconds)) return '';
      const s = parseInt(seconds, 10);
      const m = Math.floor(s / 60);
      const remS = s % 60;
      if (m < 60) {
        return `${m}:${remS < 10 ? '0' : ''}${remS}`;
      }
      const h = Math.floor(m / 60);
      const remM = m % 60;
      return `${h}:${remM < 10 ? '0' : ''}${remM}:${remS < 10 ? '0' : ''}${remS}`;
    }

    async function clientSideFallback(rawUrl) {
      const lc = rawUrl.toLowerCase();

      // --- 1. TIKTOK CLIENT EXTRACTION ---
      if (lc.includes('tiktok.com')) {
        const resp = await fetch('https://www.tikwm.com/api/?url=' + encodeURIComponent(rawUrl), {
          headers: { 'Accept': 'application/json' }
        });
        if (!resp.ok) throw new Error('TikTok network service response: ' + resp.status);
        const res = await resp.json();
        if (res.code !== 0 || !res.data) {
          throw new Error(res.msg || 'TikTok link could not be parsed.');
        }
        const d = res.data;
        const videos = [];
        if (d.hdplay) {
          videos.push({ quality: '1080p HD', format: 'mp4', size: d.hd_size || null, direct_url: d.hdplay });
        }
        if (d.play) {
          videos.push({ quality: '720p (No Watermark)', format: 'mp4', size: d.size || null, direct_url: d.play });
        }
        if (d.wmplay) {
          videos.push({ quality: '720p (Watermarked)', format: 'mp4', size: d.wm_size || null, direct_url: d.wmplay });
        }
        const audios = [];
        if (d.music) {
          audios.push({ quality: '320kbps', format: 'mp3', size: null, direct_url: d.music });
        }

        return {
          status: 'success',
          title: d.title || 'TikTok Video',
          thumbnail: d.cover || d.origin_cover || '',
          duration: fmtDur(d.duration),
          platform: 'tiktok',
          videos: videos,
          audios: audios
        };
      }

      // --- 2. YOUTUBE CLIENT EXTRACTION ---
      const ytId = extractYouTubeId(rawUrl);
      if (ytId) {
        const instances = [
          'https://yt.chocolatemoo53.com',
          'https://invidious.jing.rocks',
          'https://invidious.privacydev.net'
        ];

        let invData = null;
        let lastErr = null;

        for (const inst of instances) {
          try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 6000);
            const resp = await fetch(`${inst}/api/v1/videos/${ytId}`, {
              signal: controller.signal,
              headers: { 'Accept': 'application/json' }
            });
            clearTimeout(timeoutId);
            if (resp.ok) {
              invData = await resp.json();
              if (invData && invData.title) break;
            }
          } catch (e) {
            lastErr = e;
          }
        }

        if (!invData) {
          throw new Error('YouTube direct streams unavailable. ' + (lastErr ? lastErr.message : ''));
        }

        const videos = [];
        const seenV = new Set();

        if (Array.isArray(invData.formatStreams)) {
          invData.formatStreams.forEach(f => {
            const q = f.qualityLabel || f.resolution || '720p';
            if (f.url && !seenV.has(q)) {
              seenV.add(q);
              videos.push({
                quality: q,
                format: f.container || 'mp4',
                size: f.size || null,
                direct_url: f.url
              });
            }
          });
        }

        if (Array.isArray(invData.adaptiveFormats)) {
          invData.adaptiveFormats.forEach(f => {
            if ((f.type || '').includes('video/mp4') || (f.type || '').includes('video/webm')) {
              const q = f.qualityLabel || f.resolution;
              if (q && f.url && !seenV.has(q)) {
                seenV.add(q);
                videos.push({
                  quality: q,
                  format: f.container || 'mp4',
                  size: f.clen ? parseInt(f.clen, 10) : null,
                  direct_url: f.url
                });
              }
            }
          });
        }

        videos.sort((a, b) => {
          const numA = parseInt(String(a.quality).replace(/[^0-9]/g, '')) || 0;
          const numB = parseInt(String(b.quality).replace(/[^0-9]/g, '')) || 0;
          return numB - numA;
        });

        const audios = [];
        const seenA = new Set();
        if (Array.isArray(invData.adaptiveFormats)) {
          invData.adaptiveFormats.forEach(f => {
            if ((f.type || '').includes('audio/')) {
              const kbps = Math.round((f.bitrate || 128000) / 1000);
              const qKey = `${kbps}kbps`;
              if (f.url && !seenA.has(qKey)) {
                seenA.add(qKey);
                audios.push({
                  quality: qKey,
                  format: f.container === 'm4a' ? 'm4a' : 'mp3',
                  size: f.clen ? parseInt(f.clen, 10) : null,
                  direct_url: f.url
                });
              }
            }
          });
        }

        audios.sort((a, b) => {
          const numA = parseInt(String(a.quality).replace(/[^0-9]/g, '')) || 0;
          const numB = parseInt(String(b.quality).replace(/[^0-9]/g, '')) || 0;
          return numB - numA;
        });

        let thumb = `https://i.ytimg.com/vi/${ytId}/hqdefault.jpg`;
        if (Array.isArray(invData.videoThumbnails) && invData.videoThumbnails.length) {
          thumb = invData.videoThumbnails[invData.videoThumbnails.length - 1].url || thumb;
        }

        return {
          status: 'success',
          title: invData.title || 'YouTube Video',
          thumbnail: thumb,
          duration: fmtDur(invData.lengthSeconds),
          platform: 'youtube',
          videos: videos,
          audios: audios
        };
      }

      throw new Error('Platform not supported for direct device extraction.');
    }

    /* ============================================================
       MAIN EXTRACTION (With Client Fallback & Duplicate Block)
    ============================================================ */
    async function run() {
      let rawUrl = document.getElementById('urlInput').value.trim();
      if (!rawUrl) { document.getElementById('urlInput').focus(); return; }

      // Auto-prepend https:// if omitted
      if (!rawUrl.startsWith('http://') && !rawUrl.startsWith('https://')) {
        rawUrl = "https://" + rawUrl;
        document.getElementById('urlInput').value = rawUrl;
      }

      // 1. Client-Side Validation
      try {
        const parsed = new URL(rawUrl);
        if (!parsed.hostname || !parsed.hostname.includes('.')) {
          showInlineError("Please enter a valid video link with a domain name (e.g. YouTube, TikTok, Instagram).");
          return;
        }
      } catch (err) {
        showInlineError("Invalid URL. Please enter a valid web link.");
        return;
      }

      // 2. Prevent Duplicate Burst while in-flight
      if (isExtracting) {
        toast("Extraction already in progress. Please wait…");
        return;
      }

      // 3. Prevent Duplicate Request if same video is already loaded below
      const now = Date.now();
      if (lastRenderedUrl === rawUrl && (now - lastRenderedTime < 300000) && document.getElementById('resultsWrap').style.display !== 'none') {
        toast("Video already loaded below");
        document.getElementById('resultsWrap').scrollIntoView({ behavior: 'smooth', block: 'start' });
        return;
      }

      isExtracting = true;
      currentUrl = rawUrl;
      pushHistory(rawUrl);
      document.getElementById('historyPanel').classList.remove('open');

      const loadW   = document.getElementById('loadingWrap');
      const errP    = document.getElementById('errorPanel');
      const resW    = document.getElementById('resultsWrap');
      const bar     = document.getElementById('stickyBar');
      const btn     = document.getElementById('btnSubmit');
      const stepTx  = document.getElementById('stepText');

      errP.style.display  = 'none';
      resW.style.display  = 'none';
      bar.style.display   = 'none';
      loadW.style.display = 'block';
      btn.disabled        = true;
      btn.innerHTML       = '<span class="step-spin" style="width:14px;height:14px;border-width:2px;display:inline-block;vertical-align:middle;margin-right:6px;"></span> Extracting…';

      const steps = ["Checking link & cache…", "Resolving video streams…", "Almost ready…"];
      let si = 0;
      stepTx.textContent = steps[0];
      const stTimer = setInterval(() => { si = (si+1) % steps.length; stepTx.textContent = steps[si]; }, 1800);

      try {
        let data = null;

        try {
          const res  = await fetch('/api/info?url=' + encodeURIComponent(rawUrl));
          const json = await res.json().catch(() => null);

          if (res.ok && json && json.status === 'success') {
            data = json;
          } else {
            throw new Error((json && (json.detail || json.message)) || 'Server extraction unavailable');
          }
        } catch (serverErr) {
          console.warn('Server extraction failed, initiating direct client fallback:', serverErr.message);
          stepTx.textContent = "Connecting via direct device network…";
          data = await clientSideFallback(rawUrl);
        }

        clearInterval(stTimer);
        if (!data || data.status !== 'success') {
          throw new Error('Could not parse video streams.');
        }

        lastRenderedUrl = rawUrl;
        lastRenderedTime = Date.now();
        loadW.style.display = 'none';
        render(data, rawUrl);

      } catch (err) {
        clearInterval(stTimer);
        loadW.style.display = 'none';
        showInlineError(err.message || 'Something went wrong. Please check the link and try again.');
      } finally {
        isExtracting = false;
        btn.disabled = false;
        btn.innerHTML = `
          <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
            <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
          </svg>
          <span>Download</span>
        `;
      }
    }

    /* ============================================================
       RENDER RESULTS
    ============================================================ */
    function render(data, url) {
      const thumbSrc = data.thumbnail || '';
      document.getElementById('thumbImg').src = thumbSrc;
      document.getElementById('thumbDur').textContent = data.duration || '';
      document.getElementById('videoTitle').textContent = data.title || 'Video';

      const videos = data.videos || [];
      const audios = data.audios || [];

      document.getElementById('cntV').textContent = videos.length;
      document.getElementById('cntA').textContent = audios.length;

      bestVideoUrl = videos.length
        ? (videos[0].direct_url || `/api/stream?url=${encodeURIComponent(url)}&type=video&quality=${encodeURIComponent(videos[0].quality || 'best')}`)
        : '';
      bestAudioUrl = audios.length
        ? (audios[0].direct_url || `/api/stream?url=${encodeURIComponent(url)}&type=audio&quality=${encodeURIComponent(audios[0].quality || 'best')}`)
        : '';

      buildGrid(document.getElementById('videoGrid'), videos, 'video', url);
      buildGrid(document.getElementById('audioGrid'), audios, 'audio', url);
      setTab('video');

      document.getElementById('resultsWrap').style.display = 'block';
      document.getElementById('stickyBar').style.display   = 'flex';

      const st = document.getElementById('stickyThumb');
      if (thumbSrc) { st.src = thumbSrc; st.classList.add('show'); }

      document.getElementById('resultsWrap').scrollIntoView({ behavior: 'smooth', block: 'start' });
      toast("Download links ready");
    }

    function buildGrid(grid, items, type, url) {
      grid.innerHTML = '';
      items.forEach((item, i) => {
        const streamUrl = item.direct_url ? item.direct_url : `/api/stream?url=${encodeURIComponent(url)}&type=${type}&quality=${encodeURIComponent(item.quality || 'best')}`;
        const isBest    = i === 0;

        const rawQ  = String(item.quality || (type === 'audio' ? '320kbps' : 'HD'));
        let   qNum, qUnit, qSub;

        if (type === 'video') {
          qNum  = rawQ.replace(/[^0-9]/g, '') || rawQ;
          qUnit = /^[0-9]+$/.test(qNum) ? 'p' : '';
          qSub  = 'Video quality';
        } else {
          const kbpsMatch = rawQ.match(/([0-9]+)[ ]*kbps/i);
          if (kbpsMatch) {
            qNum  = kbpsMatch[1];
            qUnit = 'kbps';
          } else {
            qNum  = rawQ.replace(/[^0-9]/g, '') || rawQ;
            qUnit = '';
          }
          qSub = 'Audio track';
        }

        const fmt  = (item.format || (type === 'audio' ? 'mp3' : 'mp4')).toUpperCase();
        const size = fmtSize(item.size);

        const card = document.createElement('div');
        card.className = `format-card${isBest ? ' selected' : ''}`;
        card.style.setProperty('--i', i);
        card.onclick = () => pick(item, type, card);

        const dlLabel = type === 'audio'
          ? `Save ${qNum}${qUnit} MP3`
          : `Save ${qNum}${qUnit}`;

        card.innerHTML = `
          <div class="fc-top">
            <div>
              <div class="fc-num">${esc(qNum)}<span class="fc-unit">${qUnit}</span></div>
              <div class="fc-sub">${qSub}</div>
            </div>
            <span class="fc-badge${isBest ? ' best' : ''}">${isBest ? 'Best' : fmt}</span>
          </div>
          <div class="fc-specs">
            <div class="fc-row"><span>Format</span><b>${esc(fmt)}</b></div>
            ${size ? `<div class="fc-row"><span>Approx. size</span><b>${size}</b></div>` : ''}
            <div class="fc-row">
              <span>${type === 'audio' ? 'Codec' : 'Audio'}</span>
              <b>${type === 'audio' ? 'MP3' : 'Included'}</b>
            </div>
          </div>
          <button type="button" class="btn-card-dl">
            <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
              <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
            </svg>
            ${esc(dlLabel)}
          </button>
        `;

        const btnDl = card.querySelector('.btn-card-dl');
        if (btnDl) {
          btnDl.onclick = (e) => {
            e.stopPropagation();
            go(streamUrl);
          };
        }

        grid.appendChild(card);
        if (isBest) pick(item, type, card);
      });
    }

    /* ============================================================
       SELECTION & DOWNLOAD
    ============================================================ */
    function pick(item, type, el) {
      document.querySelectorAll('.format-card').forEach(c => c.classList.remove('selected'));
      el.classList.add('selected');
      selectedQuality = item;
      selectedType    = type;

      const rawQ = String(item.quality || (type === 'video' ? 'Best quality' : 'Best audio'));
      const fmt  = (item.format || (type === 'video' ? 'MP4' : 'MP3')).toUpperCase();
      const size = fmtSize(item.size);
      document.getElementById('stickyTitle').textContent = `${rawQ} ${fmt} selected`;
      document.getElementById('stickySub').textContent   = size ? `~${size}` : 'Ready to save';
    }

    function dlSelected() {
      if (!currentUrl || !selectedQuality) return;
      if (selectedQuality.direct_url) {
        go(selectedQuality.direct_url);
        return;
      }
      const q    = selectedQuality.quality || 'best';
      const type = selectedType || 'video';
      go(`/api/stream?url=${encodeURIComponent(currentUrl)}&type=${type}&quality=${encodeURIComponent(q)}`);
    }

    function dlBest() {
      if (!bestVideoUrl) {
        if (currentUrl) go(`/api/stream?url=${encodeURIComponent(currentUrl)}&type=video&quality=best`);
        return;
      }
      go(bestVideoUrl);
    }

    function dlMp3() {
      if (!bestAudioUrl) {
        if (currentUrl) {
          go(`/api/stream?url=${encodeURIComponent(currentUrl)}&type=audio&quality=best`);
          return;
        }
        toast("Audio track not available");
        return;
      }
      go(bestAudioUrl);
    }

    function go(url) {
      if (!url) return;
      toast("Download starting…");
      const a = document.createElement('a');
      a.href = url;
      a.setAttribute('download', '');
      a.setAttribute('target', '_blank');
      a.setAttribute('rel', 'noopener noreferrer');
      a.style.display = 'none';
      document.body.appendChild(a);
      a.click();
      setTimeout(() => a.remove(), 1200);
    }

    /* ============================================================
       HELPERS & EVENT LISTENERS
    ============================================================ */
    function fmtSize(bytes) {
      if (!bytes || isNaN(bytes) || bytes === 0) return '';
      const k = 1024, u = ['B','KB','MB','GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return (bytes / Math.pow(k, i)).toFixed(1) + ' ' + u[i];
    }

    function esc(s) {
      return String(s)
        .replace(/&/g,'&amp;').replace(/</g,'&lt;')
        .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    }

    function toast(msg) {
      const stack = document.getElementById('toastStack');
      const el = document.createElement('div');
      el.className = 'toast';
      el.innerHTML = `
        <svg width="14" height="14" fill="none" stroke="#4ade80" stroke-width="2.2" viewBox="0 0 24 24">
          <path d="M5 13l4 4L19 7"/>
        </svg>
        <span>${esc(msg)}</span>
      `;
      stack.appendChild(el);
      setTimeout(() => {
        el.style.opacity = '0';
        el.style.transform = 'translateX(10px)';
        setTimeout(() => el.remove(), 260);
      }, 3000);
    }

    // Keyboard & Outside Click Listeners
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        document.getElementById('historyPanel').classList.remove('open');
      }
    });

    document.addEventListener('click', (e) => {
      const panel = document.getElementById('historyPanel');
      const box = document.getElementById('downloadBox');
      if (panel && box && panel.classList.contains('open') && !box.contains(e.target) && !panel.contains(e.target)) {
        panel.classList.remove('open');
      }
    });
  </script>
</body>
</html>"""
