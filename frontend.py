def get_downloader_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>VORTEX // Next-Gen Media Downloader & Stream Engine</title>
  <meta name="description" content="Ultra-fast, studio-grade universal video and audio downloader for YouTube, Shorts, Instagram Reels, TikTok, and Twitter.">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">
  <style>
    :root {
      --bg-base: #06090f;
      --bg-surface: #0e1422;
      --bg-card: rgba(17, 24, 39, 0.7);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-focus: rgba(6, 182, 212, 0.6);
      
      --cyan-neon: #06b6d4;
      --cyan-glow: rgba(6, 182, 212, 0.35);
      --emerald-neon: #10b981;
      --indigo-neon: #6366f1;
      --violet-neon: #8b5cf6;
      
      --text-title: #ffffff;
      --text-body: #cbd5e1;
      --text-muted: #64748b;
      
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 22px;
      --font-stack: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-base);
      color: var(--text-body);
      font-family: var(--font-stack);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      position: relative;
    }

    /* Ambient Spatial Lights */
    .ambient-mesh {
      position: fixed;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 1200px;
      height: 600px;
      background: radial-gradient(circle at 50% 20%, rgba(6, 182, 212, 0.16) 0%, rgba(99, 102, 241, 0.1) 40%, transparent 75%);
      z-index: 0;
      pointer-events: none;
    }
    .grid-lines {
      position: fixed;
      inset: 0;
      background-image: 
        linear-gradient(to right, rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255,255,255,0.02) 1px, transparent 1px);
      background-size: 40px 40px;
      z-index: 0;
      pointer-events: none;
    }

    /* Top Navigation Bar */
    header {
      position: relative;
      z-index: 20;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 18px 28px;
      background: rgba(6, 9, 15, 0.75);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border-subtle);
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
    }
    .brand-icon {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: linear-gradient(135deg, #06b6d4, #6366f1);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 20px rgba(6, 182, 212, 0.5);
    }
    .brand-title {
      font-size: 19px;
      font-weight: 800;
      color: #fff;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .brand-badge {
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      padding: 3px 7px;
      border-radius: 4px;
      background: rgba(6, 182, 212, 0.15);
      border: 1px solid rgba(6, 182, 212, 0.3);
      color: var(--cyan-neon);
      letter-spacing: 0.5px;
    }
    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-size: 12px;
      font-weight: 600;
      color: #34d399;
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.25);
      padding: 5px 12px;
      border-radius: 20px;
    }
    .pulse-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.8); }
    }
    .nav-btn {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 8px;
      transition: all 0.2s;
    }
    .nav-btn:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.05);
    }

    /* Main Container */
    main {
      position: relative;
      z-index: 10;
      flex: 1;
      max-width: 900px;
      width: 100%;
      margin: 0 auto;
      padding: 50px 20px 80px;
    }

    /* Hero Header */
    .hero-box {
      text-align: center;
      margin-bottom: 35px;
    }
    .hero-tagline {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      color: var(--cyan-neon);
      background: rgba(6, 182, 212, 0.08);
      border: 1px solid rgba(6, 182, 212, 0.2);
      padding: 4px 14px;
      border-radius: 30px;
      margin-bottom: 16px;
    }
    .hero-box h1 {
      font-size: 44px;
      font-weight: 900;
      line-height: 1.15;
      letter-spacing: -1.2px;
      color: #fff;
      margin-bottom: 12px;
    }
    .hero-box h1 span {
      background: linear-gradient(135deg, #06b6d4 0%, #a855f7 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero-box p {
      color: var(--text-muted);
      font-size: 16px;
      max-width: 580px;
      margin: 0 auto;
      line-height: 1.5;
    }

    /* Premium Search Bar */
    .search-wrapper {
      position: relative;
      background: rgba(17, 24, 39, 0.8);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      padding: 10px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 25px rgba(6, 182, 212, 0.15);
      backdrop-filter: blur(20px);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .search-wrapper:focus-within {
      border-color: var(--cyan-neon);
      box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.8), 0 0 35px var(--cyan-glow);
    }
    .search-row {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .url-icon {
      padding-left: 12px;
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
      padding: 12px 6px;
      font-family: inherit;
    }
    .url-input::placeholder {
      color: #475569;
    }
    .btn-icon-action {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      color: #94a3b8;
      padding: 8px 14px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-icon-action:hover {
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
    }
    .btn-main-fetch {
      background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #6366f1 100%);
      color: #fff;
      border: none;
      padding: 14px 30px;
      font-size: 15px;
      font-weight: 800;
      border-radius: 14px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 20px rgba(6, 182, 212, 0.4);
      transition: all 0.25s;
      white-space: nowrap;
    }
    .btn-main-fetch:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(6, 182, 212, 0.6);
      filter: brightness(1.1);
    }
    .btn-main-fetch:active {
      transform: translateY(1px);
    }
    .btn-main-fetch:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }

    /* Platform Pills Bar */
    .platform-row {
      display: flex;
      justify-content: center;
      gap: 10px;
      margin-top: 20px;
      flex-wrap: wrap;
    }
    .platform-tag {
      font-size: 12px;
      color: #64748b;
      padding: 5px 12px;
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid rgba(255, 255, 255, 0.05);
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .platform-tag:hover {
      color: var(--text-body);
      border-color: rgba(255, 255, 255, 0.15);
      background: rgba(255, 255, 255, 0.05);
    }

    /* Loading State */
    .loader-box {
      display: none;
      text-align: center;
      padding: 45px 0;
    }
    .loader-ring {
      width: 52px;
      height: 52px;
      border: 4px solid rgba(6, 182, 212, 0.1);
      border-top-color: var(--cyan-neon);
      border-right-color: var(--indigo-neon);
      border-radius: 50%;
      animation: spin 0.85s linear infinite;
      margin: 0 auto 18px;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    .loader-title {
      font-size: 16px;
      font-weight: 700;
      color: #fff;
    }
    .loader-subtitle {
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 5px;
    }

    /* Error Alert */
    .alert-error {
      display: none;
      background: rgba(239, 68, 68, 0.08);
      border: 1px solid rgba(239, 68, 68, 0.25);
      color: #fca5a5;
      padding: 16px 20px;
      border-radius: 14px;
      margin-top: 25px;
      font-size: 14px;
      align-items: center;
      gap: 12px;
    }

    /* Main Result Hub */
    .result-hub {
      display: none;
      margin-top: 35px;
      animation: hubFade 0.35s ease-out;
    }
    @keyframes hubFade {
      from { opacity: 0; transform: translateY(16px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Media Overview Card */
    .media-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      padding: 24px;
      box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6);
      margin-bottom: 25px;
    }
    .media-header {
      display: flex;
      gap: 22px;
    }
    .preview-box {
      position: relative;
      width: 250px;
      min-width: 250px;
      height: 145px;
      border-radius: 14px;
      overflow: hidden;
      background: #000;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    }
    .preview-box img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s;
    }
    .preview-box:hover img {
      transform: scale(1.03);
    }
    .duration-pill {
      position: absolute;
      bottom: 8px;
      right: 8px;
      background: rgba(0, 0, 0, 0.85);
      color: #fff;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
      backdrop-filter: blur(4px);
    }
    .media-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .media-title {
      font-size: 18px;
      font-weight: 800;
      color: #fff;
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .media-badges {
      display: flex;
      gap: 10px;
      margin-top: 10px;
      flex-wrap: wrap;
    }
    .badge-item {
      font-size: 11px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-muted);
      border: 1px solid var(--border-subtle);
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }
    .badge-engine {
      background: rgba(6, 182, 212, 0.1);
      border-color: rgba(6, 182, 212, 0.3);
      color: var(--cyan-neon);
      text-transform: uppercase;
    }

    /* Quality Selector in Search Bar */
    .quality-select-input {
      background: rgba(14, 20, 34, 0.9);
      border: 1px solid var(--border-subtle);
      color: var(--cyan-neon);
      font-size: 13px;
      font-weight: 700;
      padding: 11px 14px;
      border-radius: 12px;
      cursor: pointer;
      outline: none;
      transition: all 0.2s;
    }
    .quality-select-input:hover, .quality-select-input:focus {
      border-color: var(--cyan-neon);
      background: rgba(17, 24, 39, 1);
      box-shadow: 0 0 15px var(--cyan-glow);
    }
    .quality-select-input option {
      background: #0b0f19;
      color: #fff;
    }

    /* Quality Action Station */
    .quality-station {
      margin-top: 16px;
      padding: 14px 18px;
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
    }
    .qs-title-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }
    .qs-title {
      font-size: 12px;
      font-weight: 800;
      color: var(--cyan-neon);
      letter-spacing: 0.8px;
    }
    .qs-hint {
      font-size: 11px;
      color: var(--text-muted);
    }
    .qs-pills {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }
    .pill-btn {
      background: rgba(17, 24, 39, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 10px;
      padding: 8px 14px;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      color: #fff;
      font-size: 13px;
      font-weight: 700;
      transition: all 0.2s;
    }
    .pill-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }
    .pill-1080:hover {
      border-color: var(--cyan-neon);
      box-shadow: 0 4px 18px var(--cyan-glow);
    }
    .pill-720:hover {
      border-color: var(--emerald-neon);
      box-shadow: 0 4px 18px rgba(16, 185, 129, 0.35);
    }
    .pill-480:hover, .pill-360:hover {
      border-color: var(--violet-neon);
      box-shadow: 0 4px 18px rgba(139, 92, 246, 0.35);
    }
    .pill-audio:hover {
      border-color: var(--indigo-neon);
      box-shadow: 0 4px 18px rgba(99, 102, 241, 0.35);
    }
    .pill-badge {
      font-size: 10px;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 4px;
      text-transform: uppercase;
    }
    .pill-badge.fhd {
      background: rgba(6, 182, 212, 0.2);
      color: var(--cyan-neon);
      border: 1px solid rgba(6, 182, 212, 0.4);
    }
    .pill-badge.hd {
      background: rgba(16, 185, 129, 0.2);
      color: var(--emerald-neon);
      border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .pill-badge.sd {
      background: rgba(139, 92, 246, 0.2);
      color: var(--violet-neon);
      border: 1px solid rgba(139, 92, 246, 0.4);
    }
    .pill-badge.audio {
      background: rgba(99, 102, 241, 0.2);
      color: #a5b4fc;
      border: 1px solid rgba(99, 102, 241, 0.4);
    }

    /* Segmented Filter Control */
    .filter-switcher {
      display: flex;
      background: rgba(17, 24, 39, 0.9);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 4px;
      gap: 6px;
      margin-bottom: 20px;
    }
    .filter-btn {
      flex: 1;
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 13px;
      font-weight: 700;
      padding: 10px 16px;
      border-radius: 10px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s;
    }
    .filter-btn.active {
      background: rgba(6, 182, 212, 0.15);
      color: #fff;
      border: 1px solid rgba(6, 182, 212, 0.3);
      box-shadow: 0 2px 10px rgba(6, 182, 212, 0.2);
    }
    .filter-btn:hover:not(.active) {
      color: #fff;
      background: rgba(255, 255, 255, 0.03);
    }

    /* Quality Selection Grid */
    .quality-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 15px;
    }
    .quality-card {
      background: rgba(14, 20, 34, 0.6);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      cursor: pointer;
      position: relative;
      overflow: hidden;
    }
    .quality-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 3px;
      background: transparent;
      transition: background 0.2s;
    }
    .quality-card:hover {
      border-color: rgba(6, 182, 212, 0.4);
      background: rgba(17, 24, 39, 0.95);
      transform: translateY(-2px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .quality-card.selected {
      border-color: var(--cyan-neon);
      background: rgba(6, 182, 212, 0.05);
      box-shadow: 0 0 20px rgba(6, 182, 212, 0.2);
    }
    .quality-card.selected::before {
      background: linear-gradient(90deg, var(--cyan-neon), var(--indigo-neon));
    }
    .q-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }
    .q-res {
      font-size: 20px;
      font-weight: 900;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .q-tag {
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      padding: 2px 7px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.08);
      color: #cbd5e1;
    }
    .q-tag.fhd {
      background: rgba(168, 85, 247, 0.2);
      color: #c084fc;
      border: 1px solid rgba(168, 85, 247, 0.3);
    }
    .q-tag.hd {
      background: rgba(6, 182, 212, 0.2);
      color: var(--cyan-neon);
      border: 1px solid rgba(6, 182, 212, 0.3);
    }
    .q-tag.audio {
      background: rgba(99, 102, 241, 0.2);
      color: #818cf8;
      border: 1px solid rgba(99, 102, 241, 0.3);
    }
    .q-details {
      display: flex;
      gap: 12px;
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 16px;
    }
    .q-details span b {
      color: var(--text-body);
    }
    .btn-download-card {
      width: 100%;
      background: rgba(6, 182, 212, 0.12);
      border: 1px solid rgba(6, 182, 212, 0.3);
      color: var(--cyan-neon);
      padding: 10px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-download-card:hover {
      background: var(--cyan-neon);
      color: #06090f;
      box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4);
    }

    /* Floating Download Trigger */
    .sticky-download-bar {
      position: sticky;
      bottom: 20px;
      margin-top: 25px;
      background: rgba(14, 20, 34, 0.95);
      border: 1px solid var(--cyan-neon);
      border-radius: 18px;
      padding: 14px 22px;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.8), 0 0 30px rgba(6, 182, 212, 0.3);
      backdrop-filter: blur(20px);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 15px;
      z-index: 50;
    }
    .sticky-info {
      display: flex;
      flex-direction: column;
    }
    .sticky-quality-label {
      font-size: 16px;
      font-weight: 800;
      color: #fff;
    }
    .sticky-subtext {
      font-size: 12px;
      color: var(--text-muted);
    }
    .btn-sticky-trigger {
      background: linear-gradient(135deg, #06b6d4, #3b82f6);
      color: #fff;
      border: none;
      padding: 12px 28px;
      font-size: 14px;
      font-weight: 800;
      border-radius: 12px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
      box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4);
    }
    .btn-sticky-trigger:hover {
      filter: brightness(1.15);
      transform: translateY(-1px);
    }

    /* Modal Player */
    .player-modal {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(10px);
      z-index: 100;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .player-window {
      background: #111827;
      border: 1px solid var(--border-subtle);
      border-radius: 18px;
      max-width: 700px;
      width: 100%;
      overflow: hidden;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9);
    }
    .player-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 14px 20px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      color: #fff;
      font-weight: 700;
      font-size: 14px;
    }
    .btn-close-modal {
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 20px;
    }
    .btn-close-modal:hover { color: #fff; }
    .video-container {
      width: 100%;
      background: #000;
      max-height: 400px;
    }
    .video-container video, .video-container audio {
      width: 100%;
      display: block;
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

    /* Responsive Queries */
    @media (max-width: 720px) {
      .hero-box h1 { font-size: 32px; }
      .media-header { flex-direction: column; }
      .preview-box { width: 100%; height: 200px; }
      .sticky-download-bar { flex-direction: column; align-items: stretch; }
      .btn-sticky-trigger { justify-content: center; }
      .btn-main-fetch span { display: none; }
      .btn-main-fetch { padding: 14px 18px; }
    }
  </style>
</head>
<body>
  <div class="ambient-mesh"></div>
  <div class="grid-lines"></div>

  <!-- Header -->
  <header>
    <a href="/" class="brand">
      <div class="brand-icon">
        <svg width="20" height="20" fill="none" stroke="#fff" stroke-width="2.5" viewBox="0 0 24 24"><path d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
      </div>
      <div class="brand-title">
        <span>VORTEX</span>
        <span class="brand-badge">STUDIO CORE</span>
      </div>
    </a>
    <div class="nav-actions">
      <div class="status-badge">
        <span class="pulse-dot"></span>
        <span>10 Proxies Active</span>
      </div>
      <a href="/logs" class="nav-btn" target="_blank">Engine Logs</a>
      <a href="/docs" class="nav-btn" target="_blank">API Docs</a>
    </div>
  </header>

  <!-- Main App -->
  <main>
    <div class="hero-box">
      <div class="hero-tagline">⚡ Universal High-Definition Media Engine</div>
      <h1>Extract Any Media in <span>Studio Quality</span></h1>
      <p>Direct lossless MP4 Video & MP3 Audio downloads from YouTube, Shorts, Instagram Reels, TikTok, and Twitter/X.</p>
    </div>

    <!-- Search Input Box -->
    <div class="search-wrapper">
      <form id="fetchForm" onsubmit="handleExtract(event)">
        <div class="search-row">
          <div class="url-icon">
            <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path></svg>
          </div>
          <input 
            type="url" 
            id="urlField" 
            class="url-input" 
            placeholder="Paste YouTube, Shorts, Reels, or TikTok URL..." 
            required 
            autocomplete="off"
          />
          <button type="button" class="btn-icon-action" onclick="quickPaste()">
            <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
            Paste
          </button>
          <select id="targetQuality" class="quality-select-input" title="Choose Preferred Quality">
            <option value="best" selected>⚡ Auto (Best)</option>
            <option value="1080P">💎 1080p FHD</option>
            <option value="720P">✨ 720p HD</option>
            <option value="480P">📺 480p SD</option>
            <option value="360P">📱 360p</option>
            <option value="320KBPS">🎵 320k MP3</option>
          </select>
          <button type="submit" id="extractBtn" class="btn-main-fetch">
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
            <span>Analyze Link</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Supported Platforms -->
    <div class="platform-row">
      <span class="platform-tag">🔴 YouTube & Shorts</span>
      <span class="platform-tag">🟣 Instagram Reels</span>
      <span class="platform-tag">⚫ TikTok</span>
      <span class="platform-tag">🔵 Facebook</span>
      <span class="platform-tag">⚪ Twitter / X</span>
    </div>

    <!-- Loading State -->
    <div id="loaderBox" class="loader-box">
      <div class="loader-ring"></div>
      <div class="loader-title">Decrypting Media Pipeline...</div>
      <div class="loader-subtitle">Querying VidsSave + SaveFrom signature + YT-DLP fallback engines</div>
    </div>

    <!-- Error Alert -->
    <div id="errorAlert" class="alert-error">
      <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
      <span id="errorMessage">Invalid link or media stream unavailable.</span>
    </div>

    <!-- Result Hub -->
    <div id="resultHub" class="result-hub">
      <!-- Media Header Card -->
      <div class="media-card">
        <div class="media-header">
          <div class="preview-box">
            <img id="cardThumb" src="" alt="Thumbnail" />
            <span id="cardDuration" class="duration-pill">0:00</span>
          </div>
          <div class="media-content">
            <div>
              <h2 id="cardTitle" class="media-title">Video Title</h2>
              <div class="media-badges">
                <span id="cardEngine" class="badge-item badge-engine">ENGINE: SMART AUTO</span>
                <span id="cardTotalStreams" class="badge-item">Multi-Quality Options</span>
                <span class="badge-item">⚡ 0-Second Ad-Free</span>
              </div>
            </div>
            <div class="quality-station">
              <div class="qs-title-row">
                <span class="qs-title">🎯 INSTANT QUALITY DOWNLOADS:</span>
                <span class="qs-hint">Direct 1-Click Stream</span>
              </div>
              <div class="qs-pills" id="qualityPillsContainer">
                <button type="button" class="pill-btn pill-1080" onclick="triggerQualityDownload('1080P', 'video')">
                  <span class="pill-badge fhd">1080P</span>
                  <span class="pill-label">Full HD MP4</span>
                </button>
                <button type="button" class="pill-btn pill-720" onclick="triggerQualityDownload('720P', 'video')">
                  <span class="pill-badge hd">720P</span>
                  <span class="pill-label">HD MP4</span>
                </button>
                <button type="button" class="pill-btn pill-480" onclick="triggerQualityDownload('480P', 'video')">
                  <span class="pill-badge sd">480P</span>
                  <span class="pill-label">Standard MP4</span>
                </button>
                <button type="button" class="pill-btn pill-360" onclick="triggerQualityDownload('360P', 'video')">
                  <span class="pill-badge sd">360P</span>
                  <span class="pill-label">Data Saver</span>
                </button>
                <button type="button" class="pill-btn pill-audio" onclick="triggerQualityDownload('320KBPS', 'audio')">
                  <span class="pill-badge audio">320K</span>
                  <span class="pill-label">Ultra MP3</span>
                </button>
                <button type="button" class="pill-btn pill-audio" onclick="triggerQualityDownload('128KBPS', 'audio')">
                  <span class="pill-badge audio">128K</span>
                  <span class="pill-label">Standard MP3</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Segmented Quality View Switcher -->
      <div class="filter-switcher">
        <button class="filter-btn active" onclick="switchMode('video')">
          <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
          <span id="labelVideoCount">Video Qualities</span>
        </button>
        <button class="filter-btn" onclick="switchMode('audio')">
          <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path></svg>
          <span id="labelAudioCount">Audio Bitrates</span>
        </button>
      </div>

      <!-- Dynamic Interactive Quality Grid -->
      <div id="videoGrid" class="quality-grid"></div>
      <div id="audioGrid" class="quality-grid" style="display: none;"></div>

      <!-- Sticky Download Action Bar -->
      <div id="stickyBar" class="sticky-download-bar" style="display: none;">
        <div class="sticky-info">
          <div id="stickyLabel" class="sticky-quality-label">1080p Full HD (MP4)</div>
          <div id="stickySize" class="sticky-subtext">Estimated size: ~90.4 MB • Complete Sound Included</div>
        </div>
        <button id="stickyBtn" class="btn-sticky-trigger" onclick="downloadSelectedStream()">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
          <span>Download Now</span>
        </button>
      </div>
    </div>
  </main>

  <!-- In-Browser Stream Player Modal -->
  <div id="playerModal" class="player-modal" onclick="closePlayer(event)">
    <div class="player-window" onclick="event.stopPropagation()">
      <div class="player-top">
        <span id="playerTitle">Stream Preview</span>
        <button class="btn-close-modal" onclick="closePlayer()">&times;</button>
      </div>
      <div class="video-container">
        <video id="modalVideo" controls style="display: none;"></video>
        <audio id="modalAudio" controls style="display: none; padding: 30px 20px;"></audio>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer>
    <p>⚡ VORTEX Media Engine • Multi-Tier Cascade (VidsSave ⭢ SaveFrom REA ⭢ YT-DLP) • Zero Datacenter Ban</p>
  </footer>

  <script>
    let currentData = null;
    let currentTargetUrl = '';
    let currentSelectedQuality = null;

    async function quickPaste() {
      try {
        const text = await navigator.clipboard.readText();
        if (text) {
          document.getElementById('urlField').value = text.trim();
          handleExtract();
        }
      } catch (e) {
        document.getElementById('urlField').focus();
      }
    }

    function switchMode(mode) {
      const vGrid = document.getElementById('videoGrid');
      const aGrid = document.getElementById('audioGrid');
      const btns = document.querySelectorAll('.filter-btn');

      if (mode === 'video') {
        vGrid.style.display = 'grid';
        aGrid.style.display = 'none';
        btns[0].classList.add('active');
        btns[1].classList.remove('active');
      } else {
        vGrid.style.display = 'none';
        aGrid.style.display = 'grid';
        btns[1].classList.add('active');
        btns[0].classList.remove('active');
      }
    }

    function formatBytes(bytes) {
      if (!bytes || bytes === 0 || isNaN(bytes)) return 'Lossless Stream';
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return (bytes / Math.pow(k, i)).toFixed(1) + ' ' + sizes[i];
    }

    function getQualityBadge(q) {
      const qUpper = String(q || '').toUpperCase();
      if (qUpper.includes('1080') || qUpper.includes('2K') || qUpper.includes('4K')) {
        return { label: 'FULL HD 1080P', cls: 'fhd', note: 'Studio Quality' };
      }
      if (qUpper.includes('720')) {
        return { label: 'HD 720P', cls: 'hd', note: 'Recommended' };
      }
      if (qUpper.includes('480')) {
        return { label: 'STANDARD 480P', cls: '', note: 'Balanced' };
      }
      if (qUpper.includes('360')) {
        return { label: 'FAST 360P', cls: '', note: 'Lightweight' };
      }
      return { label: qUpper || 'MP4', cls: '', note: 'Video' };
    }

    function getAudioBadge(q) {
      const qUpper = String(q || '').toUpperCase();
      if (qUpper.includes('320') || qUpper.includes('256')) {
        return { label: 'STUDIO 256K', cls: 'audio', note: 'Lossless Audio' };
      }
      if (qUpper.includes('140') || qUpper.includes('128') || qUpper.includes('139') || qUpper.includes('131')) {
        return { label: 'HIGH 128K', cls: 'audio', note: 'Crisp Audio' };
      }
      return { label: qUpper || 'MP3', cls: 'audio', note: 'Standard Audio' };
    }

    async function handleExtract(e) {
      if (e) e.preventDefault();
      const url = document.getElementById('urlField').value.trim();
      if (!url) return;

      currentTargetUrl = url;
      const loaderBox = document.getElementById('loaderBox');
      const errorAlert = document.getElementById('errorAlert');
      const resultHub = document.getElementById('resultHub');
      const extractBtn = document.getElementById('extractBtn');

      loaderBox.style.display = 'block';
      errorAlert.style.display = 'none';
      resultHub.style.display = 'none';
      extractBtn.disabled = true;

      try {
        const res = await fetch(`/api/info?url=${encodeURIComponent(url)}`);
        const data = await res.json();

        if (!res.ok || data.status !== 'success') {
          throw new Error(data.detail || data.message || 'Media extraction failed. Please check the URL.');
        }

        currentData = data;

        // Render Media Card Header
        document.getElementById('cardTitle').textContent = data.title || 'Untitled Video';
        document.getElementById('cardThumb').src = data.thumbnail || 'https://via.placeholder.com/480x270?text=No+Thumbnail';
        document.getElementById('cardDuration').textContent = data.duration || 'Video';
        document.getElementById('cardEngine').textContent = `ENGINE: ${data.engine || 'SMART WATERFALL'}`;

        const vList = data.videos || [];
        const aList = data.audios || [];
        document.getElementById('cardTotalStreams').textContent = `${vList.length + aList.length} Formats Available`;
        document.getElementById('labelVideoCount').textContent = `Video Formats (${vList.length})`;
        document.getElementById('labelAudioCount').textContent = `Audio Formats (${aList.length})`;

        // Populate Video Grid
        const vGrid = document.getElementById('videoGrid');
        vGrid.innerHTML = '';
        if (vList.length === 0) {
          vGrid.innerHTML = '<div style="color:#64748b;grid-column:1/-1;text-align:center;padding:20px;">No video formats detected. Try Audio tab.</div>';
        } else {
          vList.forEach((v, idx) => {
            const badge = getQualityBadge(v.quality);
            const card = document.createElement('div');
            card.className = `quality-card ${idx === 0 ? 'selected' : ''}`;
            card.onclick = () => selectCard(v, 'video', card);

            const directLink = v.download_url || `/api/download?url=${encodeURIComponent(url)}&type=video&quality=${encodeURIComponent(v.quality)}`;
            const streamLink = `/api/stream?url=${encodeURIComponent(url)}&type=video&quality=${encodeURIComponent(v.quality)}`;

            card.innerHTML = `
              <div class="q-top">
                <div class="q-res">
                  <span>${escapeHtml(v.quality || 'Video')}</span>
                  <span class="q-tag ${badge.cls}">${badge.label}</span>
                </div>
              </div>
              <div class="q-details">
                <span>Format: <b>${escapeHtml((v.format || 'mp4').toUpperCase())}</b></span>
                <span>Size: <b>${formatBytes(v.size)}</b></span>
                <span>Type: <b>${v.has_audio === false ? 'Video Only' : '🔊 Complete'}</b></span>
              </div>
              <button class="btn-download-card" onclick="event.stopPropagation(); triggerDirectStream('${streamLink}', '${v.download_url}')">
                <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                Download ${escapeHtml(v.quality || 'MP4')}
              </button>
            `;
            vGrid.appendChild(card);
            if (idx === 0) selectCard(v, 'video', card);
          });
        }

        // Populate Audio Grid
        const aGrid = document.getElementById('audioGrid');
        aGrid.innerHTML = '';
        if (aList.length === 0) {
          aGrid.innerHTML = '<div style="color:#64748b;grid-column:1/-1;text-align:center;padding:20px;">No audio formats detected.</div>';
        } else {
          aList.forEach((a, idx) => {
            const badge = getAudioBadge(a.quality);
            const card = document.createElement('div');
            card.className = 'quality-card';
            card.onclick = () => selectCard(a, 'audio', card);

            const directLink = a.download_url || `/api/download?url=${encodeURIComponent(url)}&type=audio&quality=${encodeURIComponent(a.quality)}`;
            const streamLink = `/api/stream?url=${encodeURIComponent(url)}&type=audio`;

            card.innerHTML = `
              <div class="q-top">
                <div class="q-res">
                  <span>${escapeHtml(a.quality || 'Audio')}</span>
                  <span class="q-tag ${badge.cls}">${badge.label}</span>
                </div>
              </div>
              <div class="q-details">
                <span>Format: <b>${escapeHtml((a.format || 'mp3').toUpperCase())}</b></span>
                <span>Size: <b>${formatBytes(a.size)}</b></span>
                <span>Bitrate: <b>${escapeHtml(a.quality)}</b></span>
              </div>
              <button class="btn-download-card" onclick="event.stopPropagation(); triggerDirectStream('${streamLink}', '${a.download_url}')">
                <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path></svg>
                Download MP3 (${escapeHtml(a.quality)})
              </button>
            `;
            aGrid.appendChild(card);
          });
        }

        resultHub.style.display = 'block';
        document.getElementById('stickyBar').style.display = 'flex';
        resultHub.scrollIntoView({ behavior: 'smooth', block: 'start' });

      } catch (err) {
        document.getElementById('errorMessage').textContent = err.message || 'An error occurred while fetching media.';
        errorAlert.style.display = 'flex';
      } finally {
        loaderBox.style.display = 'none';
        extractBtn.disabled = false;
      }
    }

    function selectCard(item, type, element) {
      document.querySelectorAll('.quality-card').forEach(c => c.classList.remove('selected'));
      element.classList.add('selected');
      currentSelectedQuality = { item, type };

      const stickyLabel = document.getElementById('stickyLabel');
      const stickySize = document.getElementById('stickySize');

      const qName = item.quality || (type === 'video' ? 'Best Video' : 'Best Audio');
      const fName = (item.format || (type === 'video' ? 'mp4' : 'mp3')).toUpperCase();
      stickyLabel.textContent = `Selected: ${qName} (${fName})`;
      stickySize.textContent = `Size: ${formatBytes(item.size)} • Instant Direct Download`;
    }

    function downloadSelectedStream() {
      if (!currentSelectedQuality || !currentTargetUrl) {
        const defaultStream = `/api/stream?url=${encodeURIComponent(currentTargetUrl)}&type=video&quality=best`;
        window.location.href = defaultStream;
        return;
      }
      const { item, type } = currentSelectedQuality;
      const q = item.quality || 'best';
      const streamUrl = `/api/stream?url=${encodeURIComponent(currentTargetUrl)}&type=${type}&quality=${encodeURIComponent(q)}`;
      window.location.href = streamUrl;
    }

    function downloadBestAudio() {
      const audioUrl = `/api/stream?url=${encodeURIComponent(currentTargetUrl)}&type=audio`;
      window.location.href = audioUrl;
    }

    function triggerDirectStream(streamUrl, directCdnUrl) {
      // Direct stream triggers browser download dialog instantly
      window.location.href = streamUrl;
    }

    function closePlayer() {
      const modal = document.getElementById('playerModal');
      const v = document.getElementById('modalVideo');
      const a = document.getElementById('modalAudio');
      v.pause();
      a.pause();
      v.src = '';
      a.src = '';
      modal.style.display = 'none';
    }

    function escapeHtml(str) {
      return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
  </script>
</body>
</html>"""
