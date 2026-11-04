def get_downloader_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>VORTEX 3D // Quantum Media Engine & Stream Downloader</title>
  <meta name="description" content="Ultra-premium 3D spatial media downloader. Download 4K, 1080p, MP4, and 320kbps MP3 from YouTube, Shorts, TikTok, Instagram Reels, and Twitter with zero proxy limits.">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">

  <!-- World-Class Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <!-- Three.js 3D WebGL Engine -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

  <style>
    :root {
      --bg-dark: #050814;
      --bg-card: rgba(13, 19, 36, 0.72);
      --bg-card-hover: rgba(18, 27, 50, 0.85);
      --bg-input: rgba(7, 11, 22, 0.88);
      
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-highlight: rgba(255, 255, 255, 0.16);
      --border-neon: rgba(0, 242, 254, 0.45);

      --neon-cyan: #00f2fe;
      --neon-blue: #38bdf8;
      --neon-indigo: #6366f1;
      --neon-purple: #a855f7;
      --neon-emerald: #10b981;
      --neon-amber: #f59e0b;
      --neon-rose: #f43f5e;

      --text-white: #ffffff;
      --text-main: #e2e8f0;
      --text-dim: #94a3b8;
      --text-muted: #64748b;

      --font-display: "Outfit", sans-serif;
      --font-body: "Plus Jakarta Sans", system-ui, -apple-system, sans-serif;
      --font-mono: "JetBrains Mono", monospace;

      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --radius-xl: 28px;
      --radius-full: 9999px;

      --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    html, body {
      background-color: var(--bg-dark);
      color: var(--text-main);
      font-family: var(--font-body);
      min-height: 100vh;
      min-height: 100dvh;
      overflow-x: hidden;
      width: 100%;
      scroll-behavior: smooth;
    }

    /* 3D WebGL Background Canvas */
    #webgl-canvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 0;
      pointer-events: none;
      opacity: 0.85;
    }

    /* Ambient Spatial Fog & Lighting */
    .spatial-aurora {
      position: fixed;
      inset: 0;
      background: 
        radial-gradient(circle at 50% -10%, rgba(0, 242, 254, 0.12) 0%, transparent 60%),
        radial-gradient(circle at 10% 40%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 90% 70%, rgba(168, 85, 247, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 50% 100%, #050814 20%, transparent 80%);
      z-index: 1;
      pointer-events: none;
    }

    .subtle-grid {
      position: fixed;
      inset: 0;
      background-image: 
        linear-gradient(to right, rgba(255, 255, 255, 0.02) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
      background-size: 40px 40px;
      z-index: 1;
      pointer-events: none;
      mask-image: radial-gradient(circle at 50% 40%, black 30%, transparent 80%);
      -webkit-mask-image: radial-gradient(circle at 50% 40%, black 30%, transparent 80%);
    }

    /* App Shell Container */
    .app-shell {
      position: relative;
      z-index: 10;
      display: flex;
      flex-direction: column;
      min-height: 100vh;
      min-height: 100dvh;
      width: 100%;
    }

    /* Luxury Header */
    header {
      position: sticky;
      top: 0;
      z-index: 100;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 28px;
      background: rgba(5, 8, 20, 0.78);
      backdrop-filter: blur(24px) saturate(180%);
      -webkit-backdrop-filter: blur(24px) saturate(180%);
      border-bottom: 1px solid var(--border-subtle);
      transition: all 0.3s ease;
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
    }

    .brand-emblem {
      width: 38px;
      height: 38px;
      border-radius: 10px;
      background: linear-gradient(135deg, var(--neon-cyan), var(--neon-indigo));
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 24px rgba(0, 242, 254, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.4);
      transform: perspective(400px) rotateY(-8deg);
      transition: transform 0.4s var(--ease-spring), box-shadow 0.4s ease;
    }
    .brand-group:hover .brand-emblem {
      transform: perspective(400px) rotateY(12deg) scale(1.05);
      box-shadow: 0 0 32px rgba(0, 242, 254, 0.7);
    }

    .brand-title {
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 800;
      color: #fff;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .brand-title span.accent {
      background: linear-gradient(90deg, #fff 0%, var(--neon-cyan) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .brand-badge {
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 6px;
      background: rgba(0, 242, 254, 0.12);
      border: 1px solid rgba(0, 242, 254, 0.3);
      color: var(--neon-cyan);
      letter-spacing: 0.5px;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .engine-status-pill {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-size: 11px;
      font-weight: 600;
      color: #34d399;
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.25);
      padding: 5px 12px;
      border-radius: var(--radius-full);
      backdrop-filter: blur(8px);
    }
    .status-dot-pulse {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--neon-emerald);
      box-shadow: 0 0 10px var(--neon-emerald);
      animation: pulse-ring 2s infinite;
    }
    @keyframes pulse-ring {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.35; transform: scale(0.75); }
    }

    .nav-btn-link {
      color: var(--text-dim);
      text-decoration: none;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      border: 1px solid transparent;
      transition: all 0.2s;
    }
    .nav-btn-link:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.05);
      border-color: var(--border-subtle);
    }

    /* Hero Section */
    .hero-container {
      max-width: 960px;
      margin: 0 auto;
      padding: 50px 20px 20px;
      text-align: center;
      width: 100%;
    }

    .pill-hero-tag {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 5px 15px;
      border-radius: var(--radius-full);
      background: linear-gradient(90deg, rgba(0, 242, 254, 0.1), rgba(99, 102, 241, 0.1));
      border: 1px solid rgba(0, 242, 254, 0.25);
      color: var(--neon-cyan);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      margin-bottom: 20px;
      box-shadow: 0 0 20px rgba(0, 242, 254, 0.1);
    }

    .hero-title {
      font-family: var(--font-display);
      font-size: clamp(32px, 5.5vw, 62px);
      font-weight: 900;
      line-height: 1.1;
      letter-spacing: -1.5px;
      color: #ffffff;
      margin-bottom: 16px;
    }
    .hero-title .text-gradient {
      background: linear-gradient(135deg, #00f2fe 0%, #38bdf8 45%, #c084fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      filter: drop-shadow(0 0 30px rgba(0, 242, 254, 0.25));
    }

    .hero-subtitle {
      font-size: clamp(14px, 2vw, 17px);
      color: var(--text-dim);
      max-width: 620px;
      margin: 0 auto 34px;
      line-height: 1.6;
    }

    /* 3D Console Card (Liquid Glass) */
    .console-stage {
      perspective: 1200px;
      max-width: 820px;
      margin: 0 auto 35px;
      width: 100%;
    }

    .liquid-console-card {
      background: var(--bg-card);
      backdrop-filter: blur(28px) saturate(180%);
      -webkit-backdrop-filter: blur(28px) saturate(180%);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-xl);
      padding: 26px;
      box-shadow: 
        0 30px 60px rgba(0, 0, 0, 0.5),
        0 0 60px rgba(0, 242, 254, 0.08),
        inset 0 1px 1px rgba(255, 255, 255, 0.15);
      position: relative;
      transform-style: preserve-3d;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .liquid-console-card::before {
      content: "";
      position: absolute;
      inset: -1px;
      border-radius: var(--radius-xl);
      padding: 1px;
      background: linear-gradient(135deg, rgba(0, 242, 254, 0.4), transparent 45%, rgba(168, 85, 247, 0.4));
      -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
      -webkit-mask-composite: xor;
      mask-composite: exclude;
      pointer-events: none;
    }

    /* Responsive Input Chassis */
    .input-chassis {
      position: relative;
      background: var(--bg-input);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: var(--radius-lg);
      padding: 8px 8px 8px 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.6), 0 8px 24px rgba(0, 0, 0, 0.25);
      transition: all 0.3s ease;
    }
    .input-chassis:focus-within {
      border-color: var(--neon-cyan);
      box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.6), 0 0 28px rgba(0, 242, 254, 0.3);
    }

    .input-icon {
      color: var(--neon-cyan);
      display: flex;
      align-items: center;
      flex-shrink: 0;
    }

    .input-field {
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      color: #fff;
      font-size: 15px;
      font-family: var(--font-body);
      min-width: 0;
    }
    .input-field::placeholder {
      color: var(--text-muted);
      font-size: 14px;
    }

    .btn-paste {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-subtle);
      color: var(--text-dim);
      font-size: 12px;
      font-weight: 600;
      padding: 8px 12px;
      border-radius: var(--radius-md);
      cursor: pointer;
      white-space: nowrap;
      flex-shrink: 0;
      transition: all 0.2s ease;
    }
    .btn-paste:hover {
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
      border-color: rgba(255, 255, 255, 0.2);
    }
    .btn-paste:active {
      transform: scale(0.96);
    }

    .btn-clear {
      display: none;
      align-items: center;
      justify-content: center;
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      padding: 6px;
      border-radius: 50%;
      flex-shrink: 0;
      transition: color 0.2s;
    }
    .btn-clear:hover {
      color: #fff;
    }

    .btn-extract-main {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: linear-gradient(135deg, var(--neon-cyan) 0%, #2563eb 100%);
      border: none;
      color: #030712;
      font-family: var(--font-display);
      font-size: 14px;
      font-weight: 800;
      letter-spacing: 0.2px;
      padding: 12px 24px;
      border-radius: var(--radius-md);
      cursor: pointer;
      white-space: nowrap;
      flex-shrink: 0;
      box-shadow: 0 4px 18px rgba(0, 242, 254, 0.35);
      transition: all 0.25s var(--ease-spring);
    }
    .btn-extract-main:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 26px rgba(0, 242, 254, 0.6);
      filter: brightness(1.1);
    }
    .btn-extract-main:active {
      transform: translateY(0) scale(0.97);
    }
    .btn-extract-main:disabled {
      opacity: 0.6;
      cursor: not-allowed;
      transform: none;
      box-shadow: none;
    }

    /* Mobile Separate Extract Button (hidden on desktop) */
    .mobile-extract-wrapper {
      display: none;
      margin-top: 10px;
    }

    /* Platform Showcase Strip */
    .platform-strip {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-top: 18px;
      flex-wrap: wrap;
    }

    .platform-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 600;
      color: var(--text-dim);
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      padding: 6px 12px;
      border-radius: var(--radius-full);
      cursor: pointer;
      transition: all 0.25s ease;
      user-select: none;
    }
    .platform-pill:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 255, 255, 0.2);
      transform: translateY(-1px);
    }
    .platform-pill.active {
      background: rgba(0, 242, 254, 0.15);
      border-color: var(--neon-cyan);
      color: #fff;
      box-shadow: 0 0 12px rgba(0, 242, 254, 0.25);
    }

    .pill-icon {
      width: 14px;
      height: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    /* Loading Reactor Box */
    .loader-box {
      display: none;
      margin: 30px auto;
      max-width: 420px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 28px 20px;
      text-align: center;
      backdrop-filter: blur(20px);
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
    }

    .quantum-reactor-spinner {
      position: relative;
      width: 60px;
      height: 60px;
      margin: 0 auto 16px;
    }
    .quantum-ring {
      position: absolute;
      inset: 0;
      border-radius: 50%;
      border: 2px solid transparent;
      border-top-color: var(--neon-cyan);
      animation: spin-clockwise 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    }
    .quantum-ring:nth-child(2) {
      inset: 6px;
      border-top-color: var(--neon-indigo);
      animation: spin-counter 0.9s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    }
    .quantum-ring:nth-child(3) {
      inset: 12px;
      border-top-color: var(--neon-emerald);
      animation: spin-clockwise 1.5s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    }
    @keyframes spin-clockwise {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    @keyframes spin-counter {
      0% { transform: rotate(360deg); }
      100% { transform: rotate(0deg); }
    }

    .loader-title {
      font-family: var(--font-display);
      font-size: 16px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 6px;
    }
    .loader-subtext {
      font-size: 12px;
      font-family: var(--font-mono);
      color: var(--neon-cyan);
      min-height: 18px;
    }

    /* Error Alert */
    .alert-error {
      display: none;
      align-items: center;
      gap: 12px;
      max-width: 680px;
      margin: 20px auto;
      padding: 14px 20px;
      background: rgba(244, 63, 94, 0.1);
      border: 1px solid rgba(244, 63, 94, 0.35);
      border-radius: var(--radius-md);
      color: #fecdd3;
      font-size: 13px;
      text-align: left;
      backdrop-filter: blur(14px);
    }
    .alert-error svg {
      flex-shrink: 0;
      color: var(--neon-rose);
    }

    /* Results Showcase Hub */
    .results-hub {
      display: none;
      max-width: 960px;
      margin: 0 auto 80px;
      padding: 0 20px;
      width: 100%;
      animation: fade-slide-up 0.45s var(--ease-spring);
    }
    @keyframes fade-slide-up {
      from { opacity: 0; transform: translateY(24px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Media Hero Card */
    .media-hero-card {
      background: var(--bg-card);
      backdrop-filter: blur(28px) saturate(180%);
      -webkit-backdrop-filter: blur(28px) saturate(180%);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-xl);
      padding: 22px;
      display: flex;
      gap: 22px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.55), inset 0 1px 1px rgba(255, 255, 255, 0.1);
      margin-bottom: 24px;
      position: relative;
      overflow: hidden;
    }
    .media-hero-card::after {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 2px;
      background: linear-gradient(90deg, var(--neon-cyan), var(--neon-indigo), var(--neon-purple));
    }

    .thumb-wrapper {
      position: relative;
      width: 280px;
      min-width: 280px;
      aspect-ratio: 16/9;
      border-radius: var(--radius-md);
      overflow: hidden;
      background: #000;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    }
    .thumb-wrapper img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.4s ease;
    }
    .thumb-wrapper:hover img {
      transform: scale(1.05);
    }
    .thumb-duration {
      position: absolute;
      bottom: 8px;
      right: 8px;
      background: rgba(0, 0, 0, 0.8);
      color: #fff;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
      backdrop-filter: blur(6px);
    }
    .thumb-play-overlay {
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(0, 0, 0, 0.25);
      pointer-events: none;
    }
    .thumb-play-icon {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: rgba(0, 242, 254, 0.85);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 20px rgba(0, 242, 254, 0.5);
    }

    .media-details {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-width: 0;
    }

    .media-top-meta {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .meta-badges-row {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }

    .engine-tag {
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 700;
      color: var(--neon-cyan);
      background: rgba(0, 242, 254, 0.1);
      border: 1px solid rgba(0, 242, 254, 0.3);
      padding: 3px 8px;
      border-radius: 6px;
      letter-spacing: 0.5px;
    }

    .media-headline {
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 700;
      color: #fff;
      line-height: 1.35;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      word-break: break-word;
    }

    .media-summary-stats {
      font-size: 12px;
      color: var(--text-dim);
      display: flex;
      align-items: center;
      gap: 10px;
    }

    /* Hero Fast Action Buttons */
    .hero-action-buttons {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: 16px;
      flex-wrap: wrap;
    }

    .btn-quick-video {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: linear-gradient(135deg, var(--neon-cyan) 0%, #2563eb 100%);
      border: none;
      color: #030712;
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 800;
      padding: 10px 18px;
      border-radius: var(--radius-md);
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(0, 242, 254, 0.35);
      transition: all 0.2s var(--ease-spring);
    }
    .btn-quick-video:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 22px rgba(0, 242, 254, 0.5);
    }

    .btn-quick-audio {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border-subtle);
      color: #fff;
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 700;
      padding: 10px 18px;
      border-radius: var(--radius-md);
      cursor: pointer;
      transition: all 0.2s var(--ease-spring);
    }
    .btn-quick-audio:hover {
      background: rgba(255, 255, 255, 0.14);
      border-color: rgba(255, 255, 255, 0.25);
      transform: translateY(-2px);
    }

    /* Tabs Bar */
    .tabs-controller {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 12px;
      flex-wrap: wrap;
      gap: 12px;
    }

    .tab-pills-wrap {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .format-tab-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      color: var(--text-dim);
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 700;
      padding: 8px 16px;
      border-radius: var(--radius-md);
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .format-tab-btn:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.08);
    }
    .format-tab-btn.active {
      color: #fff;
      background: rgba(0, 242, 254, 0.14);
      border-color: var(--neon-cyan);
      box-shadow: 0 0 16px rgba(0, 242, 254, 0.2);
    }

    /* Stream Cards Grid */
    .streams-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
    }

    .stream-quality-card {
      background: var(--bg-card);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 16px;
      transition: all 0.25s var(--ease-spring);
      cursor: pointer;
      position: relative;
    }
    .stream-quality-card:hover {
      background: var(--bg-card-hover);
      border-color: rgba(0, 242, 254, 0.4);
      transform: translateY(-3px);
      box-shadow: 0 14px 30px rgba(0, 0, 0, 0.4), 0 0 24px rgba(0, 242, 254, 0.15);
    }
    .stream-quality-card.selected {
      border-color: var(--neon-cyan);
      background: rgba(14, 25, 48, 0.85);
      box-shadow: 0 0 28px rgba(0, 242, 254, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.15);
    }

    .card-meta-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .quality-chip {
      font-family: var(--font-display);
      font-size: 18px;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: baseline;
      gap: 4px;
    }
    .quality-chip span.fmt {
      font-size: 11px;
      font-family: var(--font-mono);
      font-weight: 600;
      color: var(--text-dim);
    }

    .badge-resolution {
      font-size: 10px;
      font-weight: 700;
      font-family: var(--font-mono);
      padding: 3px 8px;
      border-radius: 6px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      background: rgba(0, 242, 254, 0.1);
      border: 1px solid rgba(0, 242, 254, 0.3);
      color: var(--neon-cyan);
    }
    .badge-resolution.gold {
      background: rgba(245, 158, 11, 0.12);
      border-color: rgba(245, 158, 11, 0.4);
      color: #fbbf24;
    }
    .badge-resolution.purple {
      background: rgba(168, 85, 247, 0.12);
      border-color: rgba(168, 85, 247, 0.4);
      color: #c084fc;
    }

    .card-specs-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 12px;
      color: var(--text-dim);
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      padding-top: 10px;
    }
    .spec-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .spec-item b {
      color: var(--text-main);
      font-family: var(--font-mono);
      font-size: 11px;
    }

    .btn-download-card {
      width: 100%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.07);
      border: 1px solid var(--border-subtle);
      color: #fff;
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 700;
      padding: 10px;
      border-radius: var(--radius-md);
      cursor: pointer;
      transition: all 0.2s var(--ease-spring);
    }
    .stream-quality-card:hover .btn-download-card,
    .stream-quality-card.selected .btn-download-card {
      background: linear-gradient(135deg, var(--neon-cyan) 0%, #2563eb 100%);
      color: #030712;
      border-color: transparent;
      box-shadow: 0 4px 14px rgba(0, 242, 254, 0.35);
    }

    /* Floating Dock (Desktop & Mobile) */
    .floating-quantum-dock {
      display: none;
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 90;
      background: rgba(8, 12, 28, 0.88);
      backdrop-filter: blur(24px) saturate(180%);
      -webkit-backdrop-filter: blur(24px) saturate(180%);
      border: 1px solid var(--border-highlight);
      border-radius: var(--radius-full);
      padding: 10px 18px;
      box-shadow: 
        0 20px 50px rgba(0, 0, 0, 0.7),
        0 0 35px rgba(0, 242, 254, 0.2),
        inset 0 1px 1px rgba(255, 255, 255, 0.2);
      align-items: center;
      gap: 16px;
      max-width: 92vw;
      width: max-content;
      animation: dock-pop 0.4s var(--ease-spring);
    }
    @keyframes dock-pop {
      from { opacity: 0; transform: translate(-50%, 30px) scale(0.95); }
      to { opacity: 1; transform: translate(-50%, 0) scale(1); }
    }

    .dock-selection-info {
      display: flex;
      flex-direction: column;
      gap: 2px;
      min-width: 140px;
    }
    .dock-sel-title {
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 800;
      color: #fff;
      white-space: nowrap;
    }
    .dock-sel-sub {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--neon-cyan);
      white-space: nowrap;
    }

    .dock-btn-main {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: linear-gradient(135deg, var(--neon-cyan) 0%, #2563eb 100%);
      border: none;
      color: #030712;
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 800;
      padding: 10px 18px;
      border-radius: var(--radius-full);
      cursor: pointer;
      white-space: nowrap;
      box-shadow: 0 4px 16px rgba(0, 242, 254, 0.35);
      transition: all 0.2s var(--ease-spring);
    }
    .dock-btn-main:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 22px rgba(0, 242, 254, 0.55);
    }

    .dock-btn-alt {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border-subtle);
      color: #fff;
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 700;
      padding: 10px 16px;
      border-radius: var(--radius-full);
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s ease;
    }
    .dock-btn-alt:hover {
      background: rgba(255, 255, 255, 0.14);
      color: #fff;
    }

    /* Features Grid */
    .features-section {
      max-width: 960px;
      margin: 40px auto 70px;
      padding: 0 20px;
      width: 100%;
    }
    .features-header {
      text-align: center;
      margin-bottom: 26px;
    }
    .features-header h3 {
      font-family: var(--font-display);
      font-size: 22px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 6px;
    }
    .features-header p {
      font-size: 13px;
      color: var(--text-dim);
    }

    .features-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
    }
    .feature-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 20px;
      backdrop-filter: blur(16px);
      transition: all 0.3s ease;
    }
    .feature-card:hover {
      border-color: rgba(0, 242, 254, 0.3);
      transform: translateY(-3px);
    }
    .feature-icon-orb {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 12px;
      background: rgba(0, 242, 245, 0.1);
      color: var(--neon-cyan);
    }
    .feature-card h4 {
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 6px;
    }
    .feature-card p {
      font-size: 12px;
      color: var(--text-dim);
      line-height: 1.5;
    }

    /* Footer */
    footer {
      border-top: 1px solid var(--border-subtle);
      padding: 26px 20px 40px;
      text-align: center;
      font-size: 12px;
      color: var(--text-muted);
      background: rgba(5, 8, 20, 0.6);
      backdrop-filter: blur(12px);
    }
    footer a {
      color: var(--neon-cyan);
      text-decoration: none;
    }
    footer a:hover {
      text-decoration: underline;
    }

    /* Toast Notification System */
    .toast-tray {
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 1000;
      display: flex;
      flex-direction: column;
      gap: 10px;
      pointer-events: none;
    }
    .toast-item {
      background: rgba(9, 14, 28, 0.95);
      border: 1px solid var(--border-highlight);
      color: #fff;
      padding: 12px 18px;
      border-radius: var(--radius-md);
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), 0 0 20px rgba(0, 242, 254, 0.2);
      backdrop-filter: blur(20px);
      pointer-events: auto;
      animation: toast-in 0.3s var(--ease-spring);
      transition: all 0.3s ease;
      max-width: 90vw;
    }
    @keyframes toast-in {
      from { opacity: 0; transform: translateY(-15px) scale(0.95); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    /* ======================================================== */
    /* MOBILE OPTIMIZATIONS (Smartphones & Small Tablets)      */
    /* ======================================================== */
    @media (max-width: 768px) {
      header {
        padding: 12px 16px;
      }
      .brand-title {
        font-size: 17px;
      }
      .brand-emblem {
        width: 32px;
        height: 32px;
      }
      .nav-btn-link {
        display: none;
      }
      .engine-status-pill {
        padding: 4px 8px;
        font-size: 10px;
      }

      .hero-container {
        padding: 30px 16px 16px;
      }
      .hero-title {
        letter-spacing: -0.8px;
        margin-bottom: 12px;
      }
      .hero-subtitle {
        margin-bottom: 24px;
        font-size: 14px;
      }

      .liquid-console-card {
        padding: 16px;
        border-radius: var(--radius-lg);
      }

      /* Desktop extract button hidden inside input bar on mobile */
      .input-chassis .btn-extract-main {
        display: none;
      }

      /* Dedicated Full-Width Extract Button on Mobile */
      .mobile-extract-wrapper {
        display: block;
      }
      .btn-mobile-extract {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background: linear-gradient(135deg, var(--neon-cyan) 0%, #2563eb 100%);
        border: none;
        color: #030712;
        font-family: var(--font-display);
        font-size: 15px;
        font-weight: 800;
        padding: 14px 20px;
        border-radius: var(--radius-md);
        box-shadow: 0 4px 20px rgba(0, 242, 254, 0.4);
        cursor: pointer;
        transition: transform 0.2s ease;
      }
      .btn-mobile-extract:active {
        transform: scale(0.98);
      }

      .platform-strip {
        flex-wrap: nowrap;
        overflow-x: auto;
        justify-content: flex-start;
        padding: 4px 0 8px;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
      }
      .platform-strip::-webkit-scrollbar {
        display: none;
      }
      .platform-pill {
        flex-shrink: 0;
      }

      /* Results Mobile Layout */
      .results-hub {
        padding: 0 14px;
      }
      .media-hero-card {
        flex-direction: column;
        padding: 16px;
        gap: 16px;
      }
      .thumb-wrapper {
        width: 100%;
        min-width: 0;
        aspect-ratio: 16/9;
      }
      .media-headline {
        font-size: 17px;
      }
      .hero-action-buttons {
        flex-direction: column;
        align-items: stretch;
      }
      .btn-quick-video, .btn-quick-audio {
        justify-content: center;
        width: 100%;
        padding: 12px;
      }

      .streams-grid {
        grid-template-columns: 1fr;
      }

      /* Floating Dock on Mobile */
      .floating-quantum-dock {
        bottom: max(14px, env(safe-area-inset-bottom));
        width: calc(100% - 24px);
        max-width: 480px;
        padding: 8px 12px;
        justify-content: space-between;
      }
      .dock-selection-info {
        display: none;
      }
      .dock-btn-main, .dock-btn-alt {
        flex: 1;
        justify-content: center;
        padding: 10px 8px;
        font-size: 12px;
      }

      .toast-tray {
        top: 14px;
        right: 14px;
        left: 14px;
      }
      .toast-item {
        width: 100%;
      }
    }
  </style>
</head>
<body>

  <!-- Three.js 3D Background Canvas -->
  <canvas id="webgl-canvas"></canvas>
  <div class="spatial-aurora"></div>
  <div class="subtle-grid"></div>

  <!-- App Main Content Shell -->
  <div class="app-shell">

    <!-- Top Navigation -->
    <header>
      <a href="/" class="brand-group">
        <div class="brand-emblem">
          <svg width="20" height="20" fill="none" stroke="#fff" stroke-width="2.5" viewBox="0 0 24 24">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
          </svg>
        </div>
        <div class="brand-title">
          <span>VORTEX</span>
          <span class="accent">3D</span>
          <span class="brand-badge">PRO</span>
        </div>
      </a>
      
      <div class="header-actions">
        <div class="engine-status-pill">
          <div class="status-dot-pulse"></div>
          <span>ZERO-PROXY ACTIVE</span>
        </div>
        <a href="/logs" target="_blank" class="nav-btn-link">Live Logs</a>
        <a href="/docs" target="_blank" class="nav-btn-link">API Docs</a>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="hero-container">
      <div class="pill-hero-tag">
        <svg width="13" height="13" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>
        <span>High-Speed Universal Stream Engine</span>
      </div>

      <h1 class="hero-title">
        Paste Any Media Link.<br>
        <span class="text-gradient">Download in 4K & Lossless MP3.</span>
      </h1>

      <p class="hero-subtitle">
        Universal multi-engine media extractor for YouTube, Shorts, TikTok, Instagram Reels, and Twitter/X with zero proxy blockages and 1-click downloads.
      </p>

      <!-- 3D Console Glass Card -->
      <div class="console-stage">
        <div class="liquid-console-card" id="consoleCard">
          <form id="mediaForm" onsubmit="executeExtraction(event)">
            <div class="input-chassis">
              <div class="input-icon">
                <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
                  <path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
                </svg>
              </div>

              <input 
                type="url" 
                id="urlInput" 
                class="input-field" 
                placeholder="Paste YouTube, Shorts, TikTok, Reels, or Twitter link..." 
                required 
                autocomplete="off"
                oninput="onUrlInput(this.value)"
              >

              <button type="button" id="btnClear" class="btn-clear" onclick="clearInput()" title="Clear text">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"></path></svg>
              </button>

              <button type="button" class="btn-paste" onclick="pasteFromClipboard()" title="Paste from clipboard">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
                <span>Paste</span>
              </button>

              <!-- Desktop Extract Button -->
              <button type="submit" id="btnExtractDesktop" class="btn-extract-main">
                <span>Extract</span>
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"></path></svg>
              </button>
            </div>

            <!-- Mobile Full-Width Extract Button -->
            <div class="mobile-extract-wrapper">
              <button type="submit" id="btnExtractMobile" class="btn-mobile-extract">
                <span>Extract Video & Audio</span>
                <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"></path></svg>
              </button>
            </div>
          </form>

          <!-- Platforms Showcase Strip -->
          <div class="platform-strip">
            <div class="platform-pill" id="pillYT" onclick="fillSample('https://youtube.com/shorts/nUgWZ37u9fY?si=Xc2H2NP2nGNoxA3V')">
              <span class="pill-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="#ff0000"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
              </span>
              <span>YouTube & Shorts</span>
            </div>

            <div class="platform-pill" id="pillTT" onclick="fillSample('https://www.tiktok.com/@tiktok/video/7106594312292453675')">
              <span class="pill-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="#00f2fe"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 3 15.7a6.34 6.34 0 0 0 10.86 4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-2.92-1.39 4.77 4.77 0 0 1-1.12-3.17h3z"/></svg>
              </span>
              <span>TikTok HD (No Watermark)</span>
            </div>

            <div class="platform-pill" id="pillIG" onclick="fillSample('https://www.instagram.com/reels/')">
              <span class="pill-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="#e1306c"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
              </span>
              <span>Instagram Reels</span>
            </div>

            <div class="platform-pill" id="pillTW" onclick="fillSample('https://twitter.com/')">
              <span class="pill-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="#fff"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
              </span>
              <span>Twitter / X</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3D Reactor Loader -->
    <div class="loader-box" id="loaderBox">
      <div class="quantum-reactor-spinner">
        <div class="quantum-ring"></div>
        <div class="quantum-ring"></div>
        <div class="quantum-ring"></div>
      </div>
      <div class="loader-title">Extracting Media Stream</div>
      <div class="loader-subtext" id="loaderStepMsg">Connecting to Zero-Proxy Engine...</div>
    </div>

    <!-- Error Alert Banner -->
    <div class="alert-error" id="errorBanner">
      <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><path d="M12 8v4m0 4h.01"></path></svg>
      <div id="errorText">Unable to extract stream from URL.</div>
    </div>

    <!-- Results Section -->
    <main class="results-hub" id="resultsHub">

      <!-- Media Hero Showcase Card -->
      <div class="media-hero-card">
        <div class="thumb-wrapper">
          <img id="thumbImg" src="" alt="Video Thumbnail">
          <div class="thumb-duration" id="thumbDuration">00:00</div>
          <div class="thumb-play-overlay">
            <div class="thumb-play-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="#030712"><polygon points="6 4 20 12 6 20 6 4"></polygon></svg>
            </div>
          </div>
        </div>

        <div class="media-details">
          <div class="media-top-meta">
            <div class="meta-badges-row">
              <span class="engine-tag" id="engineTag">ENGINE: ZERO-PROXY DIRECT</span>
              <span class="badge-resolution gold" id="platformTag">HD STREAM</span>
            </div>
            <h2 class="media-headline" id="mediaTitle">Video Title</h2>
            <div class="media-summary-stats">
              <span id="statFormatsCount">8 Qualities Ready</span>
              <span>•</span>
              <span>High Bitrate Direct Stream</span>
            </div>
          </div>

          <div class="hero-action-buttons">
            <button class="btn-quick-video" onclick="downloadSelectedQuality()">
              <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
              <span>Download 1080p/HD Video</span>
            </button>
            <button class="btn-quick-audio" onclick="downloadBestMp3()">
              <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path></svg>
              <span>Download MP3 Audio</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Format Tabs Bar -->
      <div class="tabs-controller">
        <div class="tab-pills-wrap">
          <button class="format-tab-btn active" id="tabBtnVideo" onclick="switchMediaTab('video')">
            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
            <span id="tabLabelVideo">Video Formats</span>
          </button>
          <button class="format-tab-btn" id="tabBtnAudio" onclick="switchMediaTab('audio')">
            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 19V6l12-3v13"></path></svg>
            <span id="tabLabelAudio">Audio Tracks</span>
          </button>
        </div>
        <div style="font-size: 11px; font-family: var(--font-mono); color: var(--text-dim);">
          Direct 1-Click Browser Downloads
        </div>
      </div>

      <!-- Video Stream Grid -->
      <div class="streams-grid" id="videoCardsGrid"></div>

      <!-- Audio Stream Grid -->
      <div class="streams-grid" id="audioCardsGrid" style="display: none;"></div>

    </main>

    <!-- Features Showcase -->
    <section class="features-section">
      <div class="features-header">
        <h3>Studio-Grade Downloader Architecture</h3>
        <p>Engineered for maximum reliability, speed, and device compatibility</p>
      </div>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon-orb">
            <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
          </div>
          <h4>Zero-Proxy Engine</h4>
          <p>Direct pipeline avoids expired proxies and IP bans with automatic fallback routing.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon-orb">
            <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polygon points="23 7 16 12 23 17 23 7"></polygon><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg>
          </div>
          <h4>4K & 1080p Full HD</h4>
          <p>Lossless video streaming with full audio preservation directly to your local storage.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon-orb">
            <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 18V5l12-2v13"></path><circle cx="6" cy="18" r="3"></circle><circle cx="18" cy="16" r="3"></circle></svg>
          </div>
          <h4>320kbps MP3 Audio</h4>
          <p>Extract high-bitrate soundtracks, songs, and podcasts with clean metadata tags.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon-orb">
            <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect><line x1="12" y1="18" x2="12.01" y2="18"></line></svg>
          </div>
          <h4>Mobile & Desktop</h4>
          <p>Adaptive 3D touch interface designed for iPhones, Androids, laptops, and ultra-wide screens.</p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer>
      <p>VORTEX 3D Downloader • Built with FastAPI, Three.js WebGL & Zero-Proxy Architecture</p>
      <p style="margin-top:6px;"><a href="/docs" target="_blank">Swagger Documentation</a> • <a href="/logs" target="_blank">Live Server Telemetry</a></p>
    </footer>

    <!-- Floating Quantum Dock -->
    <div class="floating-quantum-dock" id="floatingDock">
      <div class="dock-selection-info">
        <span class="dock-sel-title" id="dockQualityTitle">Selected: 1080P MP4</span>
        <span class="dock-sel-sub" id="dockQualitySub">Ready for instant download</span>
      </div>
      <button class="dock-btn-main" onclick="downloadSelectedQuality()">
        <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
        <span>Download MP4</span>
      </button>
      <button class="dock-btn-alt" onclick="downloadBestMp3()">
        <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M9 19V6l12-3v13"></path></svg>
        <span>Download MP3</span>
      </button>
    </div>

  </div>

  <!-- Toast Notification Tray -->
  <div class="toast-tray" id="toastTray"></div>

  <!-- Three.js 3D WebGL Script & Interaction Logic -->
  <script>
    let scene, camera, renderer, starfield, icosahedronCore, ringOrbit1, ringOrbit2;
    let mouseX = 0, mouseY = 0;
    let targetX = 0, targetY = 0;
    let isWarpSpeed = false;
    let isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);

    // Initialize 3D Space Background
    function init3DExperience() {
      const canvas = document.getElementById('webgl-canvas');
      if (!canvas) return;

      scene = new THREE.Scene();
      scene.fog = new THREE.FogExp2(0x050814, 0.0015);

      camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 1, 2500);
      camera.position.z = 900;

      renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, isTouchDevice ? 1.5 : 2));

      // 1. Dual-Tone Ambient Starfield (1,400 points)
      const count = isTouchDevice ? 800 : 1400;
      const starGeo = new THREE.BufferGeometry();
      const positions = new Float32Array(count * 3);
      const colors = new Float32Array(count * 3);

      const c1 = new THREE.Color(0x00f2fe);
      const c2 = new THREE.Color(0x818cf8);
      const c3 = new THREE.Color(0x38bdf8);

      for (let i = 0; i < count; i++) {
        const i3 = i * 3;
        const rad = 250 + Math.random() * 1100;
        const th = Math.random() * Math.PI * 2;
        const ph = (Math.random() - 0.5) * Math.PI;

        positions[i3] = rad * Math.cos(th) * Math.cos(ph);
        positions[i3 + 1] = rad * Math.sin(ph);
        positions[i3 + 2] = rad * Math.sin(th) * Math.cos(ph);

        const chosenColor = Math.random() > 0.6 ? c1 : (Math.random() > 0.5 ? c2 : c3);
        colors[i3] = chosenColor.r;
        colors[i3 + 1] = chosenColor.g;
        colors[i3 + 2] = chosenColor.b;
      }

      starGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      starGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

      const starMat = new THREE.PointsMaterial({
        size: isTouchDevice ? 3.0 : 3.5,
        vertexColors: true,
        transparent: true,
        opacity: 0.75,
        blending: THREE.AdditiveBlending
      });

      starfield = new THREE.Points(starGeo, starMat);
      scene.add(starfield);

      // 2. Central Wireframe Cyber Icosahedron Core
      const icoGeo = new THREE.IcosahedronGeometry(130, 2);
      const icoMat = new THREE.MeshBasicMaterial({
        color: 0x00f2fe,
        wireframe: true,
        transparent: true,
        opacity: 0.14
      });
      icosahedronCore = new THREE.Mesh(icoGeo, icoMat);
      icosahedronCore.position.set(0, 30, -120);
      scene.add(icosahedronCore);

      // 3. Orbital Halo Rings
      const ringGeo1 = new THREE.RingGeometry(210, 212, 64);
      const ringMat1 = new THREE.MeshBasicMaterial({ color: 0x818cf8, side: THREE.DoubleSide, transparent: true, opacity: 0.2 });
      ringOrbit1 = new THREE.Mesh(ringGeo1, ringMat1);
      ringOrbit1.position.set(0, 30, -120);
      ringOrbit1.rotation.x = Math.PI / 3;
      scene.add(ringOrbit1);

      const ringGeo2 = new THREE.RingGeometry(250, 252, 64);
      const ringMat2 = new THREE.MeshBasicMaterial({ color: 0x00f2fe, side: THREE.DoubleSide, transparent: true, opacity: 0.16 });
      ringOrbit2 = new THREE.Mesh(ringGeo2, ringMat2);
      ringOrbit2.position.set(0, 30, -120);
      ringOrbit2.rotation.y = Math.PI / 4;
      scene.add(ringOrbit2);

      // Listeners
      window.addEventListener('resize', onResize);
      if (!isTouchDevice) {
        document.addEventListener('mousemove', onMouseMove);
      }

      render3D();
    }

    function onResize() {
      if (!camera || !renderer) return;
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }

    function onMouseMove(e) {
      const halfW = window.innerWidth / 2;
      const halfH = window.innerHeight / 2;
      targetX = (e.clientX - halfW) * 0.35;
      targetY = (e.clientY - halfH) * 0.35;
    }

    function render3D() {
      requestAnimationFrame(render3D);

      // Smooth camera damping
      if (!isTouchDevice) {
        mouseX += (targetX - mouseX) * 0.05;
        mouseY += (targetY - mouseY) * 0.05;
        camera.position.x = mouseX;
        camera.position.y = -mouseY;
        camera.lookAt(scene.position);
      }

      const baseSpeed = isWarpSpeed ? 0.035 : 0.0025;

      if (starfield) {
        starfield.rotation.y += baseSpeed * 0.7;
        starfield.rotation.x += baseSpeed * 0.3;
      }
      if (icosahedronCore) {
        icosahedronCore.rotation.x += baseSpeed * 1.4;
        icosahedronCore.rotation.y += baseSpeed * 1.8;
      }
      if (ringOrbit1) ringOrbit1.rotation.z += baseSpeed * 1.1;
      if (ringOrbit2) ringOrbit2.rotation.z -= baseSpeed * 1.3;

      renderer.render(scene, camera);
    }

    window.addEventListener('DOMContentLoaded', init3DExperience);

    // 3D Card Tilt for Desktop
    const consoleCardEl = document.getElementById('consoleCard');
    if (consoleCardEl && !isTouchDevice) {
      consoleCardEl.addEventListener('mousemove', (e) => {
        const rect = consoleCardEl.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        const rx = (y / (rect.height / 2)) * -5;
        const ry = (x / (rect.width / 2)) * 5;
        consoleCardEl.style.transform = `perspective(1000px) rotateX(${rx}deg) rotateY(${ry}deg) scale3d(1.01, 1.01, 1.01)`;
      });
      consoleCardEl.addEventListener('mouseleave', () => {
        consoleCardEl.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
      });
    }

    // --- State & App Controllers ---
    let currentExtractedUrl = "";
    let extractedData = null;
    let selectedQualityObj = null;

    function showToast(text, type = "success") {
      const tray = document.getElementById('toastTray');
      const item = document.createElement('div');
      item.className = 'toast-item';
      
      const icon = type === 'error'
        ? `<svg width="18" height="18" fill="none" stroke="#f43f5e" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><path d="M12 8v4m0 4h.01"></path></svg>`
        : `<svg width="18" height="18" fill="none" stroke="#00f2fe" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"></path></svg>`;

      item.innerHTML = `${icon}<span>${escapeHtml(text)}</span>`;
      tray.appendChild(item);

      setTimeout(() => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(-12px)';
        setTimeout(() => item.remove(), 300);
      }, 3400);
    }

    function onUrlInput(val) {
      const btnClear = document.getElementById('btnClear');
      btnClear.style.display = val ? 'flex' : 'none';

      // Auto-highlight active platform pill
      const lower = val.toLowerCase();
      document.querySelectorAll('.platform-pill').forEach(p => p.classList.remove('active'));

      if (lower.includes('youtube.com') || lower.includes('youtu.be')) {
        document.getElementById('pillYT').classList.add('active');
      } else if (lower.includes('tiktok.com')) {
        document.getElementById('pillTT').classList.add('active');
      } else if (lower.includes('instagram.com')) {
        document.getElementById('pillIG').classList.add('active');
      } else if (lower.includes('twitter.com') || lower.includes('x.com')) {
        document.getElementById('pillTW').classList.add('active');
      }
    }

    function clearInput() {
      const inp = document.getElementById('urlInput');
      inp.value = '';
      onUrlInput('');
      inp.focus();
    }

    async function pasteFromClipboard() {
      try {
        const text = await navigator.clipboard.readText();
        if (text && text.trim()) {
          const inp = document.getElementById('urlInput');
          inp.value = text.trim();
          onUrlInput(inp.value);
          showToast("URL pasted from clipboard!");
          executeExtraction();
        }
      } catch (err) {
        document.getElementById('urlInput').focus();
      }
    }

    function fillSample(url) {
      const inp = document.getElementById('urlInput');
      inp.value = url;
      onUrlInput(url);
      showToast("Sample loaded. Extracting stream...");
      executeExtraction();
    }

    function switchMediaTab(mode) {
      const vGrid = document.getElementById('videoCardsGrid');
      const aGrid = document.getElementById('audioCardsGrid');
      const btnV = document.getElementById('tabBtnVideo');
      const btnA = document.getElementById('tabBtnAudio');

      if (mode === 'video') {
        vGrid.style.display = 'grid';
        aGrid.style.display = 'none';
        btnV.classList.add('active');
        btnA.classList.remove('active');
      } else {
        vGrid.style.display = 'none';
        aGrid.style.display = 'grid';
        btnA.classList.add('active');
        btnV.classList.remove('active');
      }
    }

    function formatBytes(bytes) {
      if (!bytes || isNaN(bytes) || bytes === 0) return 'Lossless HD';
      const k = 1024;
      const units = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return (bytes / Math.pow(k, i)).toFixed(1) + ' ' + units[i];
    }

    async function executeExtraction(e) {
      if (e) e.preventDefault();
      const url = document.getElementById('urlInput').value.trim();
      if (!url) return;

      currentExtractedUrl = url;
      const loader = document.getElementById('loaderBox');
      const errorBanner = document.getElementById('errorBanner');
      const resultsHub = document.getElementById('resultsHub');
      const dock = document.getElementById('floatingDock');
      const btnD = document.getElementById('btnExtractDesktop');
      const btnM = document.getElementById('btnExtractMobile');

      loader.style.display = 'block';
      errorBanner.style.display = 'none';
      resultsHub.style.display = 'none';
      dock.style.display = 'none';
      btnD.disabled = true;
      btnM.disabled = true;
      isWarpSpeed = true;

      const stepMsg = document.getElementById('loaderStepMsg');
      stepMsg.textContent = "Connecting to Zero-Proxy Engine...";
      const t1 = setTimeout(() => stepMsg.textContent = "Resolving high-speed stream buffers...", 1500);
      const t2 = setTimeout(() => stepMsg.textContent = "Synthesizing multi-quality presets...", 3200);

      try {
        const res = await fetch(`/api/info?url=${encodeURIComponent(url)}`);
        const data = await res.json();

        if (!res.ok || data.status !== 'success') {
          throw new Error(data.detail || data.message || 'Stream extraction failed. Please check the URL.');
        }

        extractedData = data;

        // Render Hero Preview
        document.getElementById('mediaTitle').textContent = data.title || 'Extracted Video Stream';
        document.getElementById('thumbImg').src = data.thumbnail || 'https://via.placeholder.com/640x360?text=Preview';
        document.getElementById('thumbDuration').textContent = data.duration || 'Full HD';
        document.getElementById('engineTag').textContent = `ENGINE: ${(data.engine || 'ZERO-PROXY DIRECT').toUpperCase()}`;

        const vList = data.videos || [];
        const aList = data.audios || [];

        document.getElementById('statFormatsCount').textContent = `${vList.length + aList.length} Qualities Available`;
        document.getElementById('tabLabelVideo').textContent = `Video Formats (${vList.length})`;
        document.getElementById('tabLabelAudio').textContent = `Audio Tracks (${aList.length})`;

        // Populate Video Cards Grid
        const vGrid = document.getElementById('videoCardsGrid');
        vGrid.innerHTML = '';
        vList.forEach((v, index) => {
          const card = document.createElement('div');
          card.className = `stream-quality-card ${index === 0 ? 'selected' : ''}`;
          card.onclick = () => selectCard(v, 'video', card);

          const qStr = String(v.quality || '720P').toUpperCase();
          let pillCls = "";
          let pillText = "HD STREAM";
          if (qStr.includes("1080") || qStr.includes("4K")) {
            pillCls = "gold";
            pillText = "ULTRA HD";
          } else if (qStr.includes("720")) {
            pillCls = "";
            pillText = "RECOMMENDED";
          } else {
            pillCls = "purple";
            pillText = "FAST STREAM";
          }

          const streamUrl = `/api/stream?url=${encodeURIComponent(url)}&type=video&quality=${encodeURIComponent(v.quality)}`;

          card.innerHTML = `
            <div>
              <div class="card-meta-top">
                <div class="quality-chip">
                  <span>${escapeHtml(v.quality || 'HD')}</span>
                  <span class="fmt">${escapeHtml((v.format || 'mp4').toUpperCase())}</span>
                </div>
                <span class="badge-resolution ${pillCls}">${pillText}</span>
              </div>
              <div class="card-specs-list">
                <div class="spec-item"><span>Format Container:</span><b>${escapeHtml((v.format || 'mp4').toUpperCase())}</b></div>
                <div class="spec-item"><span>Estimated Size:</span><b>${formatBytes(v.size)}</b></div>
                <div class="spec-item"><span>Audio Status:</span><b>Integrated Track</b></div>
              </div>
            </div>
            <button class="btn-download-card" onclick="event.stopPropagation(); triggerDownload('${streamUrl}')">
              <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
              <span>Download ${escapeHtml(v.quality || 'Video')}</span>
            </button>
          `;
          vGrid.appendChild(card);
          if (index === 0) selectCard(v, 'video', card);
        });

        // Populate Audio Cards Grid
        const aGrid = document.getElementById('audioCardsGrid');
        aGrid.innerHTML = '';
        aList.forEach((a, index) => {
          const card = document.createElement('div');
          card.className = 'stream-quality-card';
          card.onclick = () => selectCard(a, 'audio', card);

          const streamUrl = `/api/stream?url=${encodeURIComponent(url)}&type=audio&quality=${encodeURIComponent(a.quality || 'best')}`;

          card.innerHTML = `
            <div>
              <div class="card-meta-top">
                <div class="quality-chip">
                  <span>${escapeHtml(a.quality || 'MP3')}</span>
                  <span class="fmt">AUDIO</span>
                </div>
                <span class="badge-resolution purple">LOSSLESS AUDIO</span>
              </div>
              <div class="card-specs-list">
                <div class="spec-item"><span>Audio Codec:</span><b>MP3 320KBPS</b></div>
                <div class="spec-item"><span>File Size:</span><b>${formatBytes(a.size)}</b></div>
                <div class="spec-item"><span>Sound Quality:</span><b>High Fidelity</b></div>
              </div>
            </div>
            <button class="btn-download-card" onclick="event.stopPropagation(); triggerDownload('${streamUrl}')">
              <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M9 19V6l12-3v13"></path></svg>
              <span>Download MP3</span>
            </button>
          `;
          aGrid.appendChild(card);
        });

        resultsHub.style.display = 'block';
        dock.style.display = 'flex';
        resultsHub.scrollIntoView({ behavior: 'smooth', block: 'start' });
        showToast("Stream extracted successfully!");

      } catch (err) {
        clearTimeout(t1);
        clearTimeout(t2);
        document.getElementById('errorText').textContent = err.message || 'Media extraction failed. Please check the URL.';
        errorBanner.style.display = 'flex';
      } finally {
        isWarpSpeed = false;
        loader.style.display = 'none';
        btnD.disabled = false;
        btnM.disabled = false;
      }
    }

    function selectCard(item, type, element) {
      document.querySelectorAll('.stream-quality-card').forEach(c => c.classList.remove('selected'));
      element.classList.add('selected');
      selectedQualityObj = { item, type };

      const q = item.quality || (type === 'video' ? 'Best HD' : 'Best MP3');
      const f = (item.format || (type === 'video' ? 'mp4' : 'mp3')).toUpperCase();
      document.getElementById('dockQualityTitle').textContent = `Selected: ${q} (${f})`;
      document.getElementById('dockQualitySub').textContent = `Size: ${formatBytes(item.size)} • Ready to download`;
    }

    function downloadSelectedQuality() {
      if (!currentExtractedUrl) return;
      const q = (selectedQualityObj && selectedQualityObj.item && selectedQualityObj.item.quality) ? selectedQualityObj.item.quality : 'best';
      const type = (selectedQualityObj && selectedQualityObj.type) ? selectedQualityObj.type : 'video';
      const url = `/api/stream?url=${encodeURIComponent(currentExtractedUrl)}&type=${type}&quality=${encodeURIComponent(q)}`;
      triggerDownload(url);
    }

    function downloadBestMp3() {
      if (!currentExtractedUrl) return;
      const url = `/api/stream?url=${encodeURIComponent(currentExtractedUrl)}&type=audio&quality=best`;
      triggerDownload(url);
    }

    function triggerDownload(url) {
      showToast("Starting high-speed stream download...");
      window.location.href = url;
    }

    function escapeHtml(str) {
      return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
  </script>
</body>
</html>"""
