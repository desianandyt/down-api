def get_downloader_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Downify — Save Any Video or Audio</title>
  <meta name="description" content="Paste any video link and download it instantly. YouTube, Shorts, TikTok, Instagram Reels, and Twitter supported. Free, fast, no sign-up required.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
    /* ============================================================
       DESIGN TOKENS — dark neutral + single white accent
       Improvements over v1:
       - Subtle CSS grain texture for depth (no WebGL overhead)
       - Warmer dark base (#0d0d0d) instead of cold pure black
       - Tighter, more refined type scale
       - Better spacing rhythm (8px grid strictly)
    ============================================================ */
    :root {
      --bg:          #0d0d0d;
      --bg-raised:   #161616;
      --bg-elevated: #1f1f1f;
      --bg-hover:    #242424;
      --line:        rgba(255,255,255,0.07);
      --line-strong: rgba(255,255,255,0.14);
      --line-focus:  rgba(255,255,255,0.28);
      --text-hi:     #f4f4f5;
      --text-md:     #a1a1aa;
      --text-lo:     #52525b;
      --text-xlo:    #3f3f46;
      --success:     #4ade80;
      --danger:      #f87171;
      --r-xs:        6px;
      --r-sm:        10px;
      --r-md:        14px;
      --r-lg:        20px;
      --r-xl:        26px;
      --r-pill:      999px;
      --font:        'Geist', system-ui, -apple-system, sans-serif;
      --ease:        cubic-bezier(0.16, 1, 0.3, 1);
      --ease-fast:   cubic-bezier(0.4, 0, 0.2, 1);
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
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    body {
      min-height: 100dvh;
      overflow-x: hidden;
      /* Subtle grain texture for premium depth — pure CSS, zero JS */
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
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
      background: rgba(13,13,13,0.85);
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

    /* Live indicator — small green dot + text */
    .live-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 500;
      color: var(--text-lo);
    }
    .live-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--success);
      animation: blink 2.5s ease-in-out infinite;
    }
    @keyframes blink {
      0%, 100% { opacity: 1; }
      50%       { opacity: 0.3; }
    }

    .nav-link {
      font-size: 13px;
      font-weight: 500;
      color: var(--text-lo);
      text-decoration: none;
      padding: 5px 10px;
      border-radius: var(--r-xs);
      transition: color 0.15s;
    }
    .nav-link:hover { color: var(--text-md); }

    /* ============================================================
       PAGE SHELL
    ============================================================ */
    .page {
      display: flex;
      flex-direction: column;
      min-height: calc(100dvh - 56px);
    }

    /* ============================================================
       HERO — left-aligned on desktop (Design Variance: 7)
    ============================================================ */
    .hero-wrap {
      max-width: 1000px;
      margin: 0 auto;
      width: 100%;
      padding: 72px 32px 56px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 64px;
      align-items: start;
    }

    .hero-left {}

    .hero-eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.6px;
      text-transform: uppercase;
      color: var(--text-lo);
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
      font-size: clamp(28px, 4vw, 44px);
      font-weight: 800;
      letter-spacing: -1.5px;
      line-height: 1.1;
      color: var(--text-hi);
      margin-bottom: 14px;
    }

    .hero-sub {
      font-size: 15px;
      color: var(--text-lo);
      line-height: 1.65;
      margin-bottom: 28px;
      max-width: 38ch;
    }

    /* Platform grid — improved with platform colors as 1px border on hover */
    .platform-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
    }

    .platform-btn {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-size: 12px;
      font-weight: 500;
      color: var(--text-lo);
      background: var(--bg-raised);
      border: 1px solid var(--line);
      padding: 6px 12px;
      border-radius: var(--r-pill);
      cursor: pointer;
      transition: color 0.2s, border-color 0.2s, background 0.2s;
      user-select: none;
    }
    .platform-btn:hover {
      color: var(--text-md);
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
       DOWNLOAD BOX — right column on desktop
    ============================================================ */
    .hero-right {}

    .download-box {
      background: var(--bg-raised);
      border: 1px solid var(--line);
      border-radius: var(--r-xl);
      overflow: hidden;
      transition: border-color 0.25s var(--ease);
    }
    .download-box:focus-within {
      border-color: var(--line-strong);
    }

    /* Cycling animated placeholder */
    .input-area {
      padding: 16px 16px 10px;
    }

    .input-label {
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-xlo);
      margin-bottom: 8px;
      display: block;
    }

    .input-row {
      display: flex;
      align-items: center;
      gap: 8px;
      background: var(--bg);
      border: 1px solid var(--line);
      border-radius: var(--r-md);
      padding: 10px 10px 10px 14px;
      transition: border-color 0.2s;
    }
    .input-row:focus-within {
      border-color: var(--line-focus);
    }

    .url-input {
      flex: 1;
      min-width: 0;
      background: transparent;
      border: none;
      outline: none;
      color: var(--text-hi);
      font-family: var(--font);
      font-size: 14px;
      caret-color: var(--text-hi);
    }
    .url-input::placeholder { color: var(--text-xlo); }

    .btn-inline {
      background: none;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      padding: 4px;
      border-radius: 6px;
      flex-shrink: 0;
      color: var(--text-lo);
      transition: color 0.15s, background 0.15s;
    }
    .btn-inline:hover { color: var(--text-md); background: var(--bg-elevated); }

    /* Detected platform badge (shown when URL is pasted) */
    .detected-platform {
      display: none;
      align-items: center;
      gap: 7px;
      font-size: 11px;
      font-weight: 600;
      color: var(--text-lo);
      margin-top: 10px;
      padding: 0 2px;
    }
    .detected-platform.show { display: flex; }
    .detected-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
    }

    /* Submit button */
    .btn-submit {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      padding: 14px;
      margin-top: 10px;
      background: var(--text-hi);
      color: #0d0d0d;
      font-family: var(--font);
      font-size: 14px;
      font-weight: 700;
      border: none;
      border-radius: var(--r-md);
      cursor: pointer;
      letter-spacing: -0.2px;
      transition: background 0.15s, transform 0.15s var(--ease);
    }
    .btn-submit:hover  { background: #e4e4e7; }
    .btn-submit:active { transform: scale(0.985); }
    .btn-submit:disabled {
      opacity: 0.45;
      cursor: not-allowed;
      transform: none;
    }

    .input-footer {
      padding: 10px 16px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
    }

    .hint-text {
      font-size: 11px;
      color: var(--text-xlo);
    }

    .btn-try-example {
      font-size: 11px;
      font-weight: 500;
      color: var(--text-lo);
      background: none;
      border: none;
      cursor: pointer;
      padding: 0;
      text-decoration: underline;
      text-underline-offset: 2px;
      text-decoration-color: var(--text-xlo);
      transition: color 0.15s;
    }
    .btn-try-example:hover { color: var(--text-md); }

    /* ============================================================
       LOADING STATE — skeleton-aware, no spinner alone
    ============================================================ */
    .loading-wrap {
      display: none;
      padding: 20px 16px;
    }

    /* Skeleton shimmer */
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
    .skel-line  { height: 14px; margin-bottom: 8px; }
    .skel-line.w80 { width: 80%; }
    .skel-line.w50 { width: 50%; }
    .skel-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 16px; }
    .skel-card  { height: 100px; border-radius: var(--r-md); }

    .loading-step {
      font-size: 12px;
      color: var(--text-lo);
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .loading-step-spinner {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      border: 1.5px solid var(--line-strong);
      border-top-color: var(--text-md);
      animation: spin 0.8s linear infinite;
      flex-shrink: 0;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    /* ============================================================
       ERROR
    ============================================================ */
    .error-box {
      display: none;
      align-items: flex-start;
      gap: 10px;
      padding: 12px 14px;
      margin: 0 16px 16px;
      background: rgba(248,113,113,0.07);
      border: 1px solid rgba(248,113,113,0.2);
      border-radius: var(--r-sm);
      font-size: 13px;
      color: #fca5a5;
    }
    .error-box-icon { flex-shrink: 0; color: var(--danger); margin-top: 1px; }

    /* ============================================================
       RESULTS — below the hero on mobile, full-width
    ============================================================ */
    .results-wrap {
      display: none;
      max-width: 1000px;
      margin: 0 auto 100px;
      padding: 0 32px;
      width: 100%;
    }

    /* Media preview: thumbnail left, details right */
    .media-row {
      display: flex;
      gap: 20px;
      align-items: flex-start;
      padding: 20px;
      background: var(--bg-raised);
      border: 1px solid var(--line);
      border-radius: var(--r-xl);
      margin-bottom: 24px;
      animation: fade-up 0.4s var(--ease) both;
    }
    @keyframes fade-up {
      from { opacity: 0; transform: translateY(16px); }
      to   { opacity: 1; transform: translateY(0); }
    }

    .thumb-frame {
      position: relative;
      width: 200px;
      min-width: 200px;
      aspect-ratio: 16/9;
      border-radius: var(--r-sm);
      overflow: hidden;
      background: var(--bg-elevated);
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
      gap: 12px;
    }

    .video-title {
      font-size: 16px;
      font-weight: 700;
      color: var(--text-hi);
      line-height: 1.4;
      letter-spacing: -0.3px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .quick-dl-row {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .btn-dl-primary {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-family: var(--font);
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
    .btn-dl-primary:hover  { background: #e4e4e7; }
    .btn-dl-primary:active { transform: scale(0.97); }

    .btn-dl-ghost {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-family: var(--font);
      font-size: 13px;
      font-weight: 600;
      padding: 9px 16px;
      background: transparent;
      color: var(--text-md);
      border: 1px solid var(--line);
      border-radius: var(--r-sm);
      cursor: pointer;
      transition: color 0.15s, border-color 0.15s, transform 0.15s var(--ease);
    }
    .btn-dl-ghost:hover {
      color: var(--text-hi);
      border-color: var(--line-strong);
    }
    .btn-dl-ghost:active { transform: scale(0.97); }

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

    .tab-group {
      display: flex;
    }

    .tab {
      font-family: var(--font);
      font-size: 13px;
      font-weight: 500;
      color: var(--text-lo);
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
    }
    .tab:hover  { color: var(--text-md); }
    .tab.active {
      color: var(--text-hi);
      border-bottom-color: var(--text-hi);
    }

    .tab-count {
      font-size: 11px;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: var(--r-pill);
      background: var(--bg-elevated);
      color: var(--text-lo);
    }
    .tab.active .tab-count {
      background: var(--bg-hover);
      color: var(--text-md);
    }

    .tab-hint {
      font-size: 11px;
      color: var(--text-xlo);
    }

    /* ============================================================
       FORMAT CARDS — improved typography hierarchy
    ============================================================ */
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 10px;
    }

    /* Stagger animation via CSS custom property */
    .format-card {
      background: var(--bg-raised);
      border: 1px solid var(--line);
      border-radius: var(--r-lg);
      padding: 16px;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: border-color 0.2s, background 0.2s;
      animation: card-in 0.4s var(--ease) both;
      animation-delay: calc(var(--i, 0) * 60ms);
    }
    @keyframes card-in {
      from { opacity: 0; transform: translateY(12px); }
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

    /* Quality number is the hero — large and readable */
    .fc-quality-row {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }

    .fc-q-number {
      font-size: 32px;
      font-weight: 800;
      letter-spacing: -1px;
      color: var(--text-hi);
      line-height: 1;
    }
    .fc-q-unit {
      font-size: 14px;
      font-weight: 500;
      color: var(--text-lo);
      margin-left: 2px;
    }
    .fc-q-label {
      font-size: 11px;
      color: var(--text-lo);
      margin-top: 3px;
      font-weight: 500;
    }

    .fc-badge {
      font-size: 10px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: var(--r-pill);
      border: 1px solid var(--line);
      color: var(--text-lo);
      white-space: nowrap;
      flex-shrink: 0;
    }
    .fc-badge.best {
      border-color: rgba(74,222,128,0.4);
      color: var(--success);
      background: rgba(74,222,128,0.07);
    }

    /* Specs */
    .fc-specs {
      border-top: 1px solid var(--line);
      padding-top: 10px;
      display: flex;
      flex-direction: column;
      gap: 5px;
    }
    .fc-spec {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: var(--text-lo);
    }
    .fc-spec b {
      color: var(--text-md);
      font-weight: 500;
    }

    /* Download btn in card */
    .btn-fc-dl {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 7px;
      font-family: var(--font);
      font-size: 12px;
      font-weight: 600;
      padding: 9px;
      border-radius: var(--r-sm);
      border: 1px solid var(--line);
      background: transparent;
      color: var(--text-lo);
      cursor: pointer;
      transition: all 0.2s var(--ease);
    }
    .format-card:hover .btn-fc-dl,
    .format-card.selected .btn-fc-dl {
      background: var(--text-hi);
      color: #0d0d0d;
      border-color: transparent;
    }
    .btn-fc-dl:active { transform: scale(0.97); }

    /* ============================================================
       STICKY BOTTOM BAR — improved with mini thumbnail
    ============================================================ */
    .sticky-bar {
      display: none;
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 40;
      background: rgba(13,13,13,0.92);
      backdrop-filter: blur(20px) saturate(1.6);
      -webkit-backdrop-filter: blur(20px) saturate(1.6);
      border-top: 1px solid var(--line-strong);
      padding: 10px 20px;
      padding-bottom: max(10px, env(safe-area-inset-bottom));
      align-items: center;
      gap: 14px;
      animation: bar-up 0.35s var(--ease);
    }
    @keyframes bar-up {
      from { transform: translateY(100%); }
      to   { transform: translateY(0); }
    }

    /* Mini thumbnail in sticky bar */
    .sticky-thumb {
      width: 48px;
      height: 32px;
      border-radius: 5px;
      object-fit: cover;
      background: var(--bg-elevated);
      flex-shrink: 0;
      display: none;
    }
    .sticky-thumb.loaded { display: block; }

    .sticky-info {
      flex: 1;
      min-width: 0;
    }
    .sticky-title {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-hi);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .sticky-sub {
      font-size: 11px;
      color: var(--text-lo);
      margin-top: 2px;
    }

    .sticky-btns {
      display: flex;
      gap: 8px;
      flex-shrink: 0;
    }

    .sticky-btn-p {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: var(--font);
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
      font-family: var(--font);
      font-size: 13px;
      font-weight: 600;
      padding: 9px 14px;
      background: transparent;
      color: var(--text-md);
      border: 1px solid var(--line-strong);
      border-radius: var(--r-sm);
      cursor: pointer;
      white-space: nowrap;
      transition: color 0.15s, border-color 0.15s, transform 0.15s;
    }
    .sticky-btn-s:hover {
      color: var(--text-hi);
      border-color: var(--line-focus);
    }
    .sticky-btn-s:active { transform: scale(0.97); }

    /* ============================================================
       FEATURES STRIP — improved layout
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

    .feat {}
    .feat-title {
      font-size: 14px;
      font-weight: 700;
      color: var(--text-hi);
      letter-spacing: -0.2px;
      margin-bottom: 6px;
    }
    .feat-desc {
      font-size: 13px;
      color: var(--text-lo);
      line-height: 1.6;
    }

    /* ============================================================
       FOOTER
    ============================================================ */
    footer {
      border-top: 1px solid var(--line);
      padding: 18px 32px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }
    .footer-left { font-size: 12px; color: var(--text-xlo); }
    .footer-links { display: flex; gap: 16px; }
    .footer-links a {
      font-size: 12px;
      color: var(--text-xlo);
      text-decoration: none;
      transition: color 0.15s;
    }
    .footer-links a:hover { color: var(--text-lo); }

    /* ============================================================
       TOAST — improved with type variants
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
       HISTORY DROPDOWN — recent links
    ============================================================ */
    .history-panel {
      display: none;
      flex-direction: column;
      border-top: 1px solid var(--line);
      max-height: 160px;
      overflow-y: auto;
    }
    .history-panel.open { display: flex; }
    .history-title {
      font-size: 10px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-xlo);
      padding: 8px 14px 4px;
    }
    .history-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 7px 14px;
      cursor: pointer;
      transition: background 0.15s;
      font-size: 12px;
      color: var(--text-lo);
      border: none;
      background: none;
      text-align: left;
      font-family: var(--font);
    }
    .history-item:hover {
      background: var(--bg-elevated);
      color: var(--text-md);
    }
    .history-item svg { flex-shrink: 0; }

    /* ============================================================
       RESPONSIVE MOBILE (<= 640px)
    ============================================================ */
    @media (max-width: 768px) {
      /* Hero becomes single column */
      .hero-wrap {
        grid-template-columns: 1fr;
        gap: 32px;
        padding: 36px 16px 32px;
      }
      .hero-title { font-size: clamp(26px, 8vw, 36px); }
      .hero-sub   { font-size: 14px; max-width: 100%; }

      /* Platform grid scrolls horizontally */
      .platform-grid {
        flex-wrap: nowrap;
        overflow-x: auto;
        padding-bottom: 4px;
        scrollbar-width: none;
        -webkit-overflow-scrolling: touch;
      }
      .platform-grid::-webkit-scrollbar { display: none; }
      .platform-btn { flex-shrink: 0; }

      /* Results */
      .results-wrap { padding: 0 16px; }
      .media-row {
        flex-direction: column;
        gap: 14px;
        padding: 16px;
      }
      .thumb-frame { width: 100%; min-width: 0; }
      .video-title { font-size: 15px; }
      .quick-dl-row { flex-direction: column; }
      .btn-dl-primary, .btn-dl-ghost {
        width: 100%;
        justify-content: center;
      }

      /* Format cards */
      .cards-grid { grid-template-columns: 1fr; }
      .fc-q-number { font-size: 26px; }

      /* Sticky bar */
      .sticky-bar {
        flex-wrap: wrap;
        gap: 10px;
        padding: 10px 14px;
        padding-bottom: max(10px, env(safe-area-inset-bottom));
      }
      .sticky-thumb { display: none !important; }
      .sticky-btns {
        width: 100%;
      }
      .sticky-btn-p, .sticky-btn-s {
        flex: 1;
        justify-content: center;
      }

      /* Features */
      .features-inner { grid-template-columns: 1fr; gap: 24px; }
      .features-wrap  { padding: 32px 16px; }

      footer { padding: 16px; }
      .toast-stack { right: 12px; left: 12px; max-width: 100%; }

      .nav-link { display: none; }
      .live-pill { display: none; }
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

  <!-- Header -->
  <header class="site-header">
    <a href="/" class="logo">
      <div class="logo-mark">
        <svg width="14" height="14" fill="none" stroke="#0d0d0d" stroke-width="2.5" viewBox="0 0 24 24">
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

    <!-- Hero -->
    <div class="hero-wrap">

      <!-- Left: Headline + platforms -->
      <div class="hero-left">
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
          <button class="platform-btn" onclick="tryUrl('https://youtube.com/shorts/nUgWZ37u9fY')">
            <span class="p-dot" style="background:#ff0000;"></span> YouTube
          </button>
          <button class="platform-btn" onclick="tryUrl('https://youtube.com/shorts/nUgWZ37u9fY')">
            <span class="p-dot" style="background:#ff4444;"></span> Shorts
          </button>
          <button class="platform-btn">
            <span class="p-dot" style="background:#69c9d0;"></span> TikTok
          </button>
          <button class="platform-btn">
            <span class="p-dot" style="background:#e1306c;"></span> Instagram
          </button>
          <button class="platform-btn">
            <span class="p-dot" style="background:#888;"></span> Twitter / X
          </button>
        </div>
      </div>

      <!-- Right: Input box -->
      <div class="hero-right">
        <div class="download-box" id="downloadBox">
          <div class="input-area">
            <span class="input-label">Video link</span>
            <div class="input-row">
              <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" style="color:var(--text-xlo);flex-shrink:0;">
                <path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
              </svg>
              <input
                type="url"
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
              <button type="button" class="btn-inline" onclick="pasteLink()" aria-label="Paste from clipboard" title="Paste">
                <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                </svg>
              </button>
            </div>

            <!-- Auto-detected platform badge -->
            <div class="detected-platform" id="detectedPlatform">
              <span class="detected-dot" id="detectedDot"></span>
              <span id="detectedName"></span>
            </div>

            <!-- Main CTA -->
            <button class="btn-submit" id="btnSubmit" onclick="run()">
              <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
                <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
              </svg>
              Get Download Links
            </button>
          </div>

          <!-- History dropdown -->
          <div class="history-panel" id="historyPanel">
            <div class="history-title">Recent</div>
          </div>

          <div class="input-footer">
            <span class="hint-text">YouTube, Shorts, TikTok, Instagram, Twitter</span>
            <button class="btn-try-example" onclick="tryUrl('https://youtube.com/shorts/nUgWZ37u9fY')">Try an example</button>
          </div>

          <!-- Loading skeleton (inside box) -->
          <div class="loading-wrap" id="loadingWrap">
            <div class="loading-step">
              <div class="loading-step-spinner"></div>
              <span id="loadingStepText">Fetching video info…</span>
            </div>
            <div class="skel skel-thumb"></div>
            <div class="skel skel-line w80"></div>
            <div class="skel skel-line w50"></div>
            <div class="skel-cards">
              <div class="skel skel-card"></div>
              <div class="skel skel-card"></div>
            </div>
          </div>

          <!-- Error (inside box) -->
          <div class="error-box" id="errorBox">
            <div class="error-box-icon">
              <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/>
              </svg>
            </div>
            <div id="errorText">Something went wrong. Please check the link and try again.</div>
          </div>

        </div><!-- /download-box -->
      </div><!-- /hero-right -->
    </div><!-- /hero-wrap -->

    <!-- Results section -->
    <div class="results-wrap" id="resultsWrap">

      <!-- Media info row -->
      <div class="media-row">
        <div class="thumb-frame">
          <img id="thumbImg" src="" alt="thumbnail">
          <div class="thumb-dur" id="thumbDur"></div>
        </div>
        <div class="media-details">
          <h2 class="video-title" id="videoTitle">Video</h2>
          <div class="quick-dl-row">
            <button class="btn-dl-primary" onclick="dlBest()">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
                <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
              </svg>
              Save best quality
            </button>
            <button class="btn-dl-ghost" onclick="dlMp3()">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
                <path d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"/>
              </svg>
              Save as MP3
            </button>
          </div>
        </div>
      </div>

      <!-- Format tabs -->
      <div class="tabs-bar">
        <div class="tab-group">
          <button class="tab active" id="tabV" onclick="setTab('video')">
            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
            </svg>
            Video
            <span class="tab-count" id="cntV">0</span>
          </button>
          <button class="tab" id="tabA" onclick="setTab('audio')">
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

    </div><!-- /results-wrap -->

    <!-- Features strip -->
    <div class="features-wrap" id="featuresWrap">
      <div class="features-inner">
        <div class="feat">
          <div class="feat-title">No account needed</div>
          <div class="feat-desc">Paste a link, choose a quality, and your file starts downloading. Nothing else required.</div>
        </div>
        <div class="feat">
          <div class="feat-title">Every quality, every format</div>
          <div class="feat-desc">Pick from HD 1080p, 720p, and lower resolutions — or save just the audio as an MP3.</div>
        </div>
        <div class="feat">
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

  </div><!-- /page -->

  <!-- Sticky bar -->
  <div class="sticky-bar" id="stickyBar">
    <img class="sticky-thumb" id="stickyThumb" src="" alt="">
    <div class="sticky-info">
      <div class="sticky-title" id="stickyTitle">Best quality selected</div>
      <div class="sticky-sub"  id="stickySub">Ready to download</div>
    </div>
    <div class="sticky-btns">
      <button class="sticky-btn-p" onclick="dlSelected()">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
          <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
        </svg>
        Download
      </button>
      <button class="sticky-btn-s" onclick="dlMp3()">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
          <path d="M9 19V6l12-3v13"/>
        </svg>
        MP3
      </button>
    </div>
  </div>

  <!-- Toast stack -->
  <div class="toast-stack" id="toastStack"></div>

  <script>
    /* ============================================================
       STATE
    ============================================================ */
    let currentUrl  = "";
    let selectedQuality = null;
    let selectedType    = "video";
    let thumbSrc    = "";

    const HISTORY_KEY = "downify_history";
    const MAX_HISTORY = 5;

    /* ============================================================
       HISTORY (localStorage)
    ============================================================ */
    function getHistory() {
      try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]"); } catch { return []; }
    }
    function pushHistory(url) {
      let h = getHistory().filter(u => u !== url);
      h.unshift(url);
      if (h.length > MAX_HISTORY) h = h.slice(0, MAX_HISTORY);
      try { localStorage.setItem(HISTORY_KEY, JSON.stringify(h)); } catch {}
    }
    function renderHistory() {
      const h = getHistory();
      const panel = document.getElementById('historyPanel');
      if (!h.length) { panel.classList.remove('open'); return; }

      // Clear old items (keep title)
      const items = panel.querySelectorAll('.history-item');
      items.forEach(el => el.remove());

      h.forEach(url => {
        const btn = document.createElement('button');
        btn.className = 'history-item';
        btn.innerHTML = `
          <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <polyline points="12 8 12 12 14 14"/><circle cx="12" cy="12" r="10"/>
          </svg>
          <span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${esc(url)}</span>
        `;
        btn.onclick = () => { fillInput(url); onType(url); panel.classList.remove('open'); run(); };
        panel.appendChild(btn);
      });
    }

    /* ============================================================
       PLATFORM DETECTION
    ============================================================ */
    const PLATFORMS = [
      { match: v => v.includes('youtube.com') || v.includes('youtu.be'), name: 'YouTube', color: '#ff2020' },
      { match: v => v.includes('youtube.com/shorts'), name: 'YouTube Shorts', color: '#ff2020' },
      { match: v => v.includes('tiktok.com'), name: 'TikTok', color: '#69c9d0' },
      { match: v => v.includes('instagram.com'), name: 'Instagram', color: '#e1306c' },
      { match: v => v.includes('twitter.com') || v.includes('x.com'), name: 'Twitter / X', color: '#888' },
      { match: v => v.includes('facebook.com') || v.includes('fb.com'), name: 'Facebook', color: '#1877f2' },
    ];

    function detectPlatform(url) {
      const lc = url.toLowerCase();
      // Shorts before YouTube so it matches first
      if (lc.includes('youtube.com/shorts')) return PLATFORMS[1];
      for (const p of PLATFORMS) {
        if (p.match(lc)) return p;
      }
      return null;
    }

    /* ============================================================
       INPUT HANDLERS
    ============================================================ */
    function fillInput(url) {
      document.getElementById('urlInput').value = url;
    }

    function onType(val) {
      document.getElementById('btnClear').style.display = val ? 'flex' : 'none';

      const p = detectPlatform(val);
      const dp = document.getElementById('detectedPlatform');
      if (p && val.startsWith('http')) {
        document.getElementById('detectedDot').style.background = p.color;
        document.getElementById('detectedName').textContent = p.name + ' detected';
        dp.classList.add('show');
      } else {
        dp.classList.remove('show');
      }
    }

    function clearInput() {
      fillInput('');
      onType('');
      document.getElementById('detectedPlatform').classList.remove('show');
      document.getElementById('btnClear').style.display = 'none';
      document.getElementById('urlInput').focus();
    }

    function onFocusInput() {
      const h = getHistory();
      if (h.length && !document.getElementById('urlInput').value) {
        renderHistory();
        document.getElementById('historyPanel').classList.add('open');
      }
    }
    function onBlurInput() {
      setTimeout(() => document.getElementById('historyPanel').classList.remove('open'), 160);
    }

    async function pasteLink() {
      try {
        const text = await navigator.clipboard.readText();
        if (text && text.trim()) {
          fillInput(text.trim());
          onType(text.trim());
          toast("Link pasted");
          run();
        }
      } catch {
        document.getElementById('urlInput').focus();
      }
    }

    function tryUrl(url) {
      fillInput(url);
      onType(url);
      run();
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
       MAIN EXTRACTION
    ============================================================ */
    async function run() {
      const url = document.getElementById('urlInput').value.trim();
      if (!url) { document.getElementById('urlInput').focus(); return; }

      currentUrl = url;
      pushHistory(url);

      const loadW  = document.getElementById('loadingWrap');
      const errBox = document.getElementById('errorBox');
      const resW   = document.getElementById('resultsWrap');
      const bar    = document.getElementById('stickyBar');
      const btn    = document.getElementById('btnSubmit');
      const featW  = document.getElementById('featuresWrap');
      const stepTx = document.getElementById('loadingStepText');

      // Reset
      errBox.style.display  = 'none';
      resW.style.display    = 'none';
      bar.style.display     = 'none';
      loadW.style.display   = 'block';
      btn.disabled          = true;

      const steps = ["Fetching video info…", "Reading available qualities…", "Almost ready…"];
      let si = 0;
      stepTx.textContent = steps[0];
      const stepTimer = setInterval(() => { si = (si + 1) % steps.length; stepTx.textContent = steps[si]; }, 1800);

      try {
        const res  = await fetch(`/api/info?url=${encodeURIComponent(url)}`);
        const data = await res.json();
        clearInterval(stepTimer);

        if (!res.ok || data.status !== 'success') {
          throw new Error(data.detail || data.message || 'Could not read this video link.');
        }

        loadW.style.display = 'none';
        featW.style.display = 'none';
        render(data, url);

      } catch (err) {
        clearInterval(stepTimer);
        loadW.style.display = 'none';
        document.getElementById('errorText').textContent =
          err.message || 'Something went wrong. Please check the link and try again.';
        errBox.style.display = 'flex';
      } finally {
        btn.disabled = false;
      }
    }

    /* ============================================================
       RENDER RESULTS
    ============================================================ */
    function render(data, url) {
      thumbSrc = data.thumbnail || '';
      document.getElementById('thumbImg').src    = thumbSrc;
      document.getElementById('thumbDur').textContent = data.duration || '';
      document.getElementById('videoTitle').textContent = data.title || 'Video';

      const videos = data.videos || [];
      const audios = data.audios || [];

      document.getElementById('cntV').textContent = videos.length;
      document.getElementById('cntA').textContent = audios.length;

      buildGrid(document.getElementById('videoGrid'), videos, 'video', url);
      buildGrid(document.getElementById('audioGrid'), audios, 'audio', url);

      setTab('video');

      document.getElementById('resultsWrap').style.display = 'block';
      document.getElementById('stickyBar').style.display   = 'flex';

      // Sticky thumbnail
      const st = document.getElementById('stickyThumb');
      if (thumbSrc) { st.src = thumbSrc; st.classList.add('loaded'); }

      document.getElementById('resultsWrap').scrollIntoView({ behavior: 'smooth', block: 'start' });
      toast("Download links ready");
    }

    function buildGrid(grid, items, type, url) {
      grid.innerHTML = '';
      items.forEach((item, i) => {
        const streamUrl = `/api/stream?url=${encodeURIComponent(url)}&type=${type}&quality=${encodeURIComponent(item.quality || 'best')}`;
        const isBest    = i === 0;

        const q    = String(item.quality || (type === 'audio' ? 'MP3' : 'HD'));
        const qNum = q.replace(/[^0-9kK]/g, '') || q;
        const qUnit = /[0-9]/.test(qNum) && type === 'video' ? 'p' : '';
        const fmt  = (item.format || (type === 'audio' ? 'mp3' : 'mp4')).toUpperCase();
        const size = fmtSize(item.size);

        const card = document.createElement('div');
        card.className = `format-card${isBest ? ' selected' : ''}`;
        card.style.setProperty('--i', i);
        card.onclick = () => pick(item, type, card);

        card.innerHTML = `
          <div class="fc-quality-row">
            <div>
              <div class="fc-q-number">${esc(qNum)}<span class="fc-q-unit">${qUnit}</span></div>
              <div class="fc-q-label">${type === 'audio' ? 'Audio track' : 'Video quality'}</div>
            </div>
            <span class="fc-badge${isBest ? ' best' : ''}">${isBest ? 'Best' : fmt}</span>
          </div>
          <div class="fc-specs">
            <div class="fc-spec"><span>Format</span><b>${esc(fmt)}</b></div>
            ${size ? `<div class="fc-spec"><span>Approx. size</span><b>${size}</b></div>` : ''}
            <div class="fc-spec"><span>${type === 'audio' ? 'Codec' : 'Audio'}</span><b>${type === 'audio' ? 'MP3' : 'Included'}</b></div>
          </div>
          <button class="btn-fc-dl" onclick="event.stopPropagation(); go('${streamUrl}')">
            <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
              <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
            </svg>
            Save ${esc(q)}${qUnit}${type === 'audio' ? ' MP3' : ''}
          </button>
        `;
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

      const q    = item.quality || (type === 'video' ? 'Best quality' : 'Best audio');
      const fmt  = (item.format || (type === 'video' ? 'MP4' : 'MP3')).toUpperCase();
      const size = fmtSize(item.size);
      document.getElementById('stickyTitle').textContent = `${q} ${fmt} selected`;
      document.getElementById('stickySub').textContent   = size ? `~${size}` : 'Ready to save';
    }

    function dlSelected() {
      if (!currentUrl) return;
      const q    = selectedQuality?.quality || 'best';
      const type = selectedType || 'video';
      go(`/api/stream?url=${encodeURIComponent(currentUrl)}&type=${type}&quality=${encodeURIComponent(q)}`);
    }

    function dlBest() {
      if (!currentUrl) return;
      go(`/api/stream?url=${encodeURIComponent(currentUrl)}&type=video&quality=best`);
    }

    function dlMp3() {
      if (!currentUrl) return;
      go(`/api/stream?url=${encodeURIComponent(currentUrl)}&type=audio&quality=best`);
    }

    function go(url) {
      toast("Download starting…");
      window.location.href = url;
    }

    /* ============================================================
       HELPERS
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

    /* Enter key on input */
    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('urlInput').addEventListener('keydown', e => {
        if (e.key === 'Enter') { e.preventDefault(); run(); }
      });
    });
  </script>
</body>
</html>"""
