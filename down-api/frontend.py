def get_downloader_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>VORTEX 3D // Quantum Media Engine & Stream Downloader</title>
  <meta name="description" content="Awwwards-grade, 3D spatial universal media downloader. Download videos and audio from YouTube, Shorts, TikTok, Instagram Reels, and Twitter in 1080p, 720p, MP4, and 320kbps MP3.">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">

  <!-- Premium Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

  <!-- Three.js 3D WebGL Library -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

  <style>
    :root {
      --bg-dark: #040711;
      --bg-panel: rgba(10, 16, 33, 0.65);
      --bg-glass: rgba(15, 23, 46, 0.45);
      --bg-glass-hover: rgba(22, 34, 66, 0.75);
      --border-glass: rgba(255, 255, 255, 0.08);
      --border-glow: rgba(0, 242, 254, 0.4);

      --neon-cyan: #00f2fe;
      --neon-blue: #4facfe;
      --neon-purple: #8b5cf6;
      --neon-pink: #ec4899;
      --neon-emerald: #10b981;
      
      --text-white: #ffffff;
      --text-light: #f1f5f9;
      --text-dim: #94a3b8;
      --text-muted: #64748b;

      --font-main: "Plus Jakarta Sans", system-ui, -apple-system, sans-serif;
      --font-mono: "JetBrains Mono", monospace;
      --radius-sm: 10px;
      --radius-md: 16px;
      --radius-lg: 24px;
      --radius-xl: 32px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      background-color: var(--bg-dark);
      color: var(--text-light);
      font-family: var(--font-main);
      min-height: 100vh;
      overflow-x: hidden;
      scroll-behavior: smooth;
    }

    /* 3D WebGL Background Canvas */
    #webgl-canvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 0;
      pointer-events: none;
    }

    /* Ambient Spatial Fog & Lighting */
    .spatial-vignette {
      position: fixed;
      inset: 0;
      background: radial-gradient(circle at 50% 30%, transparent 20%, rgba(4, 7, 17, 0.7) 70%, #040711 100%);
      z-index: 1;
      pointer-events: none;
    }
    .neon-grid {
      position: fixed;
      inset: 0;
      background-image: 
        linear-gradient(to right, rgba(0, 242, 254, 0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(139, 92, 246, 0.03) 1px, transparent 1px);
      background-size: 50px 50px;
      z-index: 1;
      pointer-events: none;
      mask-image: radial-gradient(circle at 50% 40%, black 30%, transparent 80%);
      -webkit-mask-image: radial-gradient(circle at 50% 40%, black 30%, transparent 80%);
    }

    /* Main Container */
    .app-viewport {
      position: relative;
      z-index: 10;
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }

    /* Top Futuristic Navbar */
    header {
      position: sticky;
      top: 0;
      z-index: 100;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 18px 36px;
      background: rgba(4, 7, 17, 0.75);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border-glass);
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
      text-decoration: none;
    }
    .brand-cube {
      width: 42px;
      height: 42px;
      border-radius: 12px;
      background: linear-gradient(135deg, var(--neon-cyan), var(--neon-purple));
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 25px rgba(0, 242, 254, 0.5), inset 0 0 10px rgba(255,255,255,0.4);
      transform: perspective(600px) rotateY(-15deg) rotateX(10deg);
      transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .brand:hover .brand-cube {
      transform: perspective(600px) rotateY(15deg) rotateX(-10deg) scale(1.08);
      box-shadow: 0 0 35px rgba(0, 242, 254, 0.8);
    }
    .brand-title {
      font-size: 21px;
      font-weight: 900;
      color: #fff;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .brand-title span {
      background: linear-gradient(90deg, #fff 0%, var(--neon-cyan) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .version-tag {
      font-size: 10px;
      font-family: var(--font-mono);
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
      background: rgba(0, 242, 254, 0.12);
      border: 1px solid rgba(0, 242, 254, 0.35);
      color: var(--neon-cyan);
      letter-spacing: 0.5px;
    }
    .nav-stats {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .chip-indicator {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      font-weight: 700;
      color: #34d399;
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.25);
      padding: 6px 14px;
      border-radius: 30px;
      backdrop-filter: blur(10px);
    }
    .pulse-beacon {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--neon-emerald);
      box-shadow: 0 0 10px var(--neon-emerald);
      animation: beacon 1.8s infinite;
    }
    @keyframes beacon {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.3; transform: scale(0.7); }
    }
    .nav-link-btn {
      color: var(--text-dim);
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      padding: 7px 14px;
      border-radius: 10px;
      border: 1px solid transparent;
      transition: all 0.2s;
    }
    .nav-link-btn:hover {
      color: #fff;
      border-color: var(--border-glass);
      background: rgba(255, 255, 255, 0.05);
    }

    /* Hero Center Stage */
    .hero-stage {
      max-width: 980px;
      margin: 0 auto;
      padding: 60px 24px 30px;
      text-align: center;
    }
    .hero-badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 16px;
      border-radius: 50px;
      background: linear-gradient(90deg, rgba(0, 242, 254, 0.1), rgba(139, 92, 246, 0.1));
      border: 1px solid rgba(0, 242, 254, 0.3);
      color: var(--neon-cyan);
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 22px;
      text-transform: uppercase;
      letter-spacing: 1px;
      box-shadow: 0 0 20px rgba(0, 242, 254, 0.15);
    }
    .hero-headline {
      font-size: clamp(38px, 6vw, 68px);
      font-weight: 900;
      line-height: 1.08;
      letter-spacing: -1.5px;
      color: var(--text-white);
      margin-bottom: 18px;
    }
    .hero-headline .gradient-text {
      background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #c084fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      filter: drop-shadow(0 0 35px rgba(0, 242, 254, 0.35));
    }
    .hero-subline {
      font-size: clamp(15px, 2.2vw, 19px);
      color: var(--text-dim);
      max-width: 680px;
      margin: 0 auto 38px;
      line-height: 1.6;
    }

    /* 3D Floating Console Container */
    .console-wrapper {
      perspective: 1200px;
      max-width: 860px;
      margin: 0 auto 40px;
      position: relative;
    }
    .console-card {
      background: var(--bg-panel);
      backdrop-filter: blur(28px);
      -webkit-backdrop-filter: blur(28px);
      border: 1px solid var(--border-glass);
      border-radius: var(--radius-xl);
      padding: 30px;
      box-shadow: 
        0 30px 60px rgba(0, 0, 0, 0.6),
        0 0 80px rgba(0, 242, 254, 0.12),
        inset 0 1px 1px rgba(255, 255, 255, 0.15);
      position: relative;
      transform-style: preserve-3d;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .console-card::before {
      content: "";
      position: absolute;
      inset: -1px;
      border-radius: var(--radius-xl);
      padding: 1px;
      background: linear-gradient(135deg, rgba(0, 242, 254, 0.5), transparent 40%, rgba(139, 92, 246, 0.5));
      -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
      -webkit-mask-composite: xor;
      mask-composite: exclude;
      pointer-events: none;
    }

    /* 3D Search & Input Bar */
    .search-chassis {
      position: relative;
      background: rgba(5, 9, 20, 0.85);
      border-radius: var(--radius-lg);
      padding: 8px 10px 8px 18px;
      display: flex;
      align-items: center;
      gap: 12px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.8), 0 10px 25px rgba(0, 0, 0, 0.3);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      transform: translateZ(20px);
    }
    .search-chassis:focus-within {
      border-color: var(--neon-cyan);
      box-shadow: 
        0 0 35px rgba(0, 242, 254, 0.35),
        inset 0 2px 6px rgba(0, 0, 0, 0.8);
    }
    .search-icon-orb {
      color: var(--neon-cyan);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .search-input {
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      color: #fff;
      font-size: 16px;
      font-family: var(--font-main);
      font-weight: 500;
      min-width: 0;
    }
    .search-input::placeholder {
      color: var(--text-muted);
    }
    .btn-action-paste {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--text-light);
      padding: 10px 16px;
      border-radius: var(--radius-md);
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
      white-space: nowrap;
    }
    .btn-action-paste:hover {
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
      border-color: rgba(255, 255, 255, 0.25);
    }

    .btn-quantum-submit {
      background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #6366f1 100%);
      color: #040711;
      font-size: 15px;
      font-weight: 800;
      padding: 14px 28px;
      border-radius: var(--radius-md);
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 4px 25px rgba(0, 242, 254, 0.45);
      transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
      white-space: nowrap;
    }
    .btn-quantum-submit:hover {
      transform: translateY(-2px) scale(1.02);
      box-shadow: 0 8px 35px rgba(0, 242, 254, 0.7);
      color: #000;
    }
    .btn-quantum-submit:active {
      transform: translateY(0) scale(0.98);
    }

    /* Platform Pills Matrix */
    .platform-matrix {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 24px;
      transform: translateZ(10px);
    }
    .platform-chip {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.06);
      padding: 7px 14px;
      border-radius: 30px;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-dim);
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.25s;
    }
    .platform-chip:hover {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 255, 255, 0.2);
      color: #fff;
      transform: translateY(-2px);
    }
    .chip-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
    }
    .chip-yt { background: #ff0000; box-shadow: 0 0 8px rgba(255,0,0,0.6); }
    .chip-tt { background: #00f2fe; box-shadow: 0 0 8px rgba(0,242,254,0.6); }
    .chip-ig { background: #e1306c; box-shadow: 0 0 8px rgba(225,48,108,0.6); }
    .chip-tw { background: #1da1f2; box-shadow: 0 0 8px rgba(29,161,242,0.6); }
    .chip-fb { background: #1877f2; box-shadow: 0 0 8px rgba(24,119,242,0.6); }

    /* 3D Loading Reactor */
    .loader-reactor {
      display: none;
      background: var(--bg-panel);
      backdrop-filter: blur(25px);
      border: 1px solid var(--border-glass);
      border-radius: var(--radius-xl);
      max-width: 860px;
      margin: 0 auto 30px;
      padding: 40px 24px;
      text-align: center;
    }
    .reactor-core {
      position: relative;
      width: 70px;
      height: 70px;
      margin: 0 auto 20px;
    }
    .reactor-ring {
      position: absolute;
      inset: 0;
      border-radius: 50%;
      border: 3px solid transparent;
      border-top-color: var(--neon-cyan);
      animation: spin 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    }
    .reactor-ring:nth-child(2) {
      inset: 6px;
      border-top-color: var(--neon-purple);
      animation: spin-reverse 0.9s linear infinite;
    }
    .reactor-ring:nth-child(3) {
      inset: 12px;
      border-top-color: var(--neon-emerald);
      animation: spin 1.5s linear infinite;
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }
    @keyframes spin-reverse { 100% { transform: rotate(-360deg); } }
    .loader-title {
      font-size: 18px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 8px;
    }
    .loader-step {
      font-size: 13px;
      color: var(--neon-cyan);
      font-family: var(--font-mono);
    }

    /* Error Banner */
    .error-card {
      display: none;
      background: rgba(239, 68, 68, 0.1);
      border: 1px solid rgba(239, 68, 68, 0.3);
      color: #fca5a5;
      padding: 18px 24px;
      border-radius: var(--radius-lg);
      max-width: 860px;
      margin: 0 auto 30px;
      display: flex;
      align-items: center;
      gap: 14px;
      font-size: 14px;
      font-weight: 600;
    }

    /* 3D Result Spatial Hub */
    .result-hub {
      display: none;
      max-width: 980px;
      margin: 0 auto 50px;
      perspective: 1400px;
    }
    .media-card-hero {
      background: var(--bg-panel);
      backdrop-filter: blur(28px);
      border: 1px solid var(--border-glass);
      border-radius: var(--radius-xl);
      padding: 30px;
      display: flex;
      gap: 28px;
      margin-bottom: 30px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5);
      position: relative;
      overflow: hidden;
    }
    .media-card-hero::after {
      content: "";
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: radial-gradient(circle, rgba(0, 242, 254, 0.08) 0%, transparent 60%);
      pointer-events: none;
    }
    .thumb-3d-box {
      width: 320px;
      min-width: 320px;
      height: 190px;
      border-radius: var(--radius-lg);
      overflow: hidden;
      position: relative;
      background: #060914;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .thumb-3d-box img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.5s ease;
    }
    .thumb-3d-box:hover img {
      transform: scale(1.05);
    }
    .thumb-duration-pill {
      position: absolute;
      bottom: 12px;
      right: 12px;
      background: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(8px);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      color: #fff;
      font-family: var(--font-mono);
      border: 1px solid rgba(255,255,255,0.15);
    }
    .media-meta {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-width: 0;
    }
    .media-meta-top {
      margin-bottom: 15px;
    }
    .engine-status-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-family: var(--font-mono);
      font-weight: 700;
      color: var(--neon-cyan);
      background: rgba(0, 242, 254, 0.1);
      border: 1px solid rgba(0, 242, 254, 0.25);
      padding: 4px 10px;
      border-radius: 20px;
      margin-bottom: 12px;
      text-transform: uppercase;
    }
    .media-title-text {
      font-size: 20px;
      font-weight: 800;
      color: #fff;
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .media-quick-stats {
      display: flex;
      align-items: center;
      gap: 15px;
      font-size: 13px;
      color: var(--text-dim);
      font-weight: 600;
      margin-top: 10px;
    }
    .media-quick-stats span b {
      color: #fff;
    }

    /* Format Switcher Tabs */
    .tabs-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }
    .tabs-group {
      display: inline-flex;
      background: rgba(5, 9, 20, 0.7);
      border: 1px solid var(--border-glass);
      padding: 5px;
      border-radius: var(--radius-md);
      gap: 6px;
    }
    .tab-btn {
      background: transparent;
      border: none;
      color: var(--text-dim);
      font-size: 14px;
      font-weight: 700;
      padding: 10px 20px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
    }
    .tab-btn.active {
      background: linear-gradient(135deg, rgba(0, 242, 254, 0.2), rgba(99, 102, 241, 0.2));
      border: 1px solid rgba(0, 242, 254, 0.4);
      color: #fff;
      box-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
    }

    /* 3D Quality Cards Grid */
    .stream-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 18px;
      perspective: 1000px;
    }
    .quality-3d-card {
      background: var(--bg-panel);
      backdrop-filter: blur(20px);
      border: 1px solid var(--border-glass);
      border-radius: var(--radius-lg);
      padding: 22px;
      cursor: pointer;
      position: relative;
      transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s ease, border-color 0.3s ease;
      transform-style: preserve-3d;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 185px;
    }
    .quality-3d-card:hover {
      transform: translateY(-6px) scale(1.02) rotateX(4deg);
      border-color: var(--neon-cyan);
      box-shadow: 0 15px 40px rgba(0, 242, 254, 0.25);
    }
    .quality-3d-card.selected {
      border-color: var(--neon-cyan);
      background: linear-gradient(145deg, rgba(0, 242, 254, 0.08), rgba(15, 23, 46, 0.8));
      box-shadow: 0 0 35px rgba(0, 242, 254, 0.35);
    }
    .q-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
    }
    .q-badge {
      font-size: 18px;
      font-weight: 900;
      color: #fff;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .q-pill {
      font-size: 10px;
      font-family: var(--font-mono);
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(0, 242, 254, 0.15);
      border: 1px solid rgba(0, 242, 254, 0.35);
      color: var(--neon-cyan);
      text-transform: uppercase;
    }
    .q-pill.gold {
      background: rgba(245, 158, 11, 0.15);
      border-color: rgba(245, 158, 11, 0.4);
      color: #fbbf24;
    }
    .q-pill.purple {
      background: rgba(168, 85, 247, 0.15);
      border-color: rgba(168, 85, 247, 0.4);
      color: #c084fc;
    }
    .q-specs {
      font-size: 13px;
      color: var(--text-dim);
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 18px;
    }
    .q-specs div {
      display: flex;
      justify-content: space-between;
    }
    .q-specs b {
      color: #fff;
      font-family: var(--font-mono);
    }
    .btn-card-stream {
      background: linear-gradient(135deg, rgba(0, 242, 254, 0.15), rgba(79, 172, 254, 0.15));
      border: 1px solid rgba(0, 242, 254, 0.35);
      color: #fff;
      font-size: 13px;
      font-weight: 800;
      padding: 10px;
      border-radius: var(--radius-md);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s;
    }
    .btn-card-stream:hover {
      background: linear-gradient(135deg, #00f2fe, #4facfe);
      color: #040711;
      box-shadow: 0 0 25px rgba(0, 242, 254, 0.5);
    }

    /* Floating Quantum Dock (Bottom Floating Bar) */
    .quantum-dock {
      display: none;
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 1000;
      background: rgba(8, 14, 28, 0.85);
      backdrop-filter: blur(25px);
      -webkit-backdrop-filter: blur(25px);
      border: 1px solid rgba(0, 242, 254, 0.35);
      border-radius: 40px;
      padding: 10px 18px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), 0 0 40px rgba(0, 242, 254, 0.2);
      align-items: center;
      gap: 16px;
      max-width: 90vw;
    }
    .dock-info {
      display: flex;
      flex-direction: column;
      padding-left: 8px;
    }
    .dock-info-title {
      font-size: 13px;
      font-weight: 800;
      color: #fff;
    }
    .dock-info-sub {
      font-size: 11px;
      color: var(--neon-cyan);
      font-family: var(--font-mono);
    }
    .btn-dock-download {
      background: linear-gradient(135deg, var(--neon-cyan), #3b82f6);
      color: #040711;
      font-size: 14px;
      font-weight: 800;
      padding: 12px 24px;
      border-radius: 30px;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 0 25px rgba(0, 242, 254, 0.5);
      transition: all 0.2s;
    }
    .btn-dock-download:hover {
      transform: scale(1.04);
      box-shadow: 0 0 35px rgba(0, 242, 254, 0.8);
    }
    .btn-dock-audio {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #fff;
      font-size: 13px;
      font-weight: 700;
      padding: 12px 18px;
      border-radius: 30px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-dock-audio:hover {
      background: rgba(255, 255, 255, 0.16);
      border-color: rgba(255, 255, 255, 0.3);
    }

    /* Toast Notifications */
    .toast-box {
      position: fixed;
      top: 24px;
      right: 24px;
      z-index: 2000;
      display: flex;
      flex-direction: column;
      gap: 10px;
      pointer-events: none;
    }
    .toast {
      background: rgba(8, 14, 28, 0.9);
      backdrop-filter: blur(16px);
      border: 1px solid var(--neon-cyan);
      padding: 12px 20px;
      border-radius: var(--radius-md);
      color: #fff;
      font-size: 13px;
      font-weight: 600;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(0, 242, 254, 0.3);
      display: flex;
      align-items: center;
      gap: 10px;
      animation: toastIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    @keyframes toastIn {
      from { opacity: 0; transform: translateY(-20px) scale(0.9); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    /* Responsive */
    @media (max-width: 768px) {
      header { padding: 14px 18px; }
      .hero-stage { padding: 35px 16px 20px; }
      .console-card { padding: 20px; }
      .search-chassis { flex-direction: column; align-items: stretch; padding: 12px; gap: 10px; }
      .btn-quantum-submit { justify-content: center; width: 100%; }
      .btn-action-paste { justify-content: center; }
      .media-card-hero { flex-direction: column; }
      .thumb-3d-box { width: 100%; min-width: 0; height: 210px; }
      .quantum-dock { width: 92vw; padding: 10px 14px; bottom: 16px; }
      .dock-info { display: none; }
      .btn-dock-download, .btn-dock-audio { flex: 1; justify-content: center; }
    }
  </style>
</head>
<body>

  <!-- WebGL 3D Background Canvas -->
  <canvas id="webgl-canvas"></canvas>
  <div class="spatial-vignette"></div>
  <div class="neon-grid"></div>

  <div class="app-viewport">
    
    <!-- Top Nav -->
    <header>
      <a href="/" class="brand">
        <div class="brand-cube">
          <svg width="22" height="22" fill="none" stroke="#fff" stroke-width="2.5" viewBox="0 0 24 24">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
          </svg>
        </div>
        <div class="brand-title">
          <span>VORTEX</span>
          <span class="version-tag">3D STUDIO</span>
        </div>
      </a>
      <div class="nav-stats">
        <div class="chip-indicator">
          <div class="pulse-beacon"></div>
          <span>ZERO-PROXY DIRECT ENGINE</span>
        </div>
        <a href="/logs" target="_blank" class="nav-link-btn">Live Logs</a>
        <a href="/docs" target="_blank" class="nav-link-btn">API Docs</a>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="hero-stage">
      <div class="hero-badge-pill">
        <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>
        Next-Gen Spatial Stream Extraction
      </div>
      <h1 class="hero-headline">
        Paste Any Media Link.<br>
        <span class="gradient-text">Stream & Download in 4K.</span>
      </h1>
      <p class="hero-subline">
        Ultra-high-speed multi-engine downloader. YouTube, Shorts, TikTok, Instagram Reels, and Twitter/X with zero rate limits, lossless audio, and instant direct downloads.
      </p>

      <!-- 3D Floating Console Card -->
      <div class="console-wrapper">
        <div class="console-card" id="mainConsoleCard">
          <form id="extractForm" onsubmit="handleExtract(event)">
            <div class="search-chassis">
              <div class="search-icon-orb">
                <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
                  <path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
                </svg>
              </div>
              <input 
                type="url" 
                id="urlField" 
                class="search-input" 
                placeholder="Paste YouTube, Shorts, TikTok, Instagram or Twitter URL..." 
                required 
                autocomplete="off"
              >
              <button type="button" class="btn-action-paste" onclick="pasteClipboard()">
                <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
                Paste
              </button>
              <button type="submit" id="extractBtn" class="btn-quantum-submit">
                <span>Extract Stream</span>
                <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                  <path d="M5 12h14M12 5l7 7-7 7"></path>
                </svg>
              </button>
            </div>
          </form>

          <!-- Platforms Matrix -->
          <div class="platform-matrix">
            <div class="platform-chip"><div class="chip-dot chip-yt"></div> YouTube & Shorts</div>
            <div class="platform-chip"><div class="chip-dot chip-tt"></div> TikTok (No Watermark)</div>
            <div class="platform-chip"><div class="chip-dot chip-ig"></div> Instagram Reels</div>
            <div class="platform-chip"><div class="chip-dot chip-tw"></div> Twitter / X</div>
            <div class="platform-chip"><div class="chip-dot chip-fb"></div> Facebook HD</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3D Loading Reactor -->
    <div class="loader-reactor" id="loaderBox">
      <div class="reactor-core">
        <div class="reactor-ring"></div>
        <div class="reactor-ring"></div>
        <div class="reactor-ring"></div>
      </div>
      <div class="loader-title">Analyzing Quantum Stream...</div>
      <div class="loader-step" id="loaderStepText">Connecting through Zero-Proxy Direct Engine</div>
    </div>

    <!-- Error Alert -->
    <div class="error-card" id="errorAlert" style="display: none;">
      <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><path d="M12 8v4m0 4h.01"></path></svg>
      <div id="errorMessage">Unable to resolve stream. Please verify the URL.</div>
    </div>

    <!-- 3D Result Spatial Hub -->
    <main class="result-hub" id="resultHub">
      
      <!-- Video Hero Showcase -->
      <div class="media-card-hero">
        <div class="thumb-3d-box">
          <img id="cardThumb" src="" alt="Thumbnail Preview">
          <div class="thumb-duration-pill" id="cardDuration">00:00</div>
        </div>
        <div class="media-meta">
          <div class="media-meta-top">
            <div class="engine-status-tag" id="cardEngine">ENGINE: ZERO-PROXY DIRECT</div>
            <h2 class="media-title-text" id="cardTitle">Video Title</h2>
            <div class="media-quick-stats">
              <span id="cardTotalStreams">8 Formats Available</span>
              <span>•</span>
              <span>Lossless Spatial Audio</span>
            </div>
          </div>
          <div>
            <!-- Quick Actions -->
            <button class="btn-quantum-submit" style="display:inline-flex; padding: 10px 22px; font-size:13px;" onclick="downloadSelectedStream()">
              ⚡ Download Best Video (1080p/HD)
            </button>
            <button class="btn-action-paste" style="display:inline-flex; margin-left: 10px; padding: 10px 18px;" onclick="downloadBestAudio()">
              🎵 Download MP3 Audio
            </button>
          </div>
        </div>
      </div>

      <!-- Format Tabs -->
      <div class="tabs-bar">
        <div class="tabs-group">
          <button class="tab-btn active" id="tabVideo" onclick="switchFormatMode('video')">
            <svg width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
            <span id="labelVideoCount">Video Formats</span>
          </button>
          <button class="tab-btn" id="tabAudio" onclick="switchFormatMode('audio')">
            <svg width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path></svg>
            <span id="labelAudioCount">Audio Formats</span>
          </button>
        </div>
        <div style="font-size:12px; font-family:var(--font-mono); color:var(--text-dim);">
          Direct 1-Click Stream Links
        </div>
      </div>

      <!-- Video Grid -->
      <div class="stream-grid" id="videoGrid"></div>

      <!-- Audio Grid -->
      <div class="stream-grid" id="audioGrid" style="display: none;"></div>

    </main>

    <!-- Floating Quantum Dock -->
    <div class="quantum-dock" id="quantumDock">
      <div class="dock-info">
        <div class="dock-info-title" id="dockTitle">Selected: 1080P MP4</div>
        <div class="dock-info-sub" id="dockSub">Ready for instant download</div>
      </div>
      <button class="btn-dock-download" onclick="downloadSelectedStream()">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
        Download MP4
      </button>
      <button class="btn-dock-audio" onclick="downloadBestAudio()">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M9 19V6l12-3v13"></path></svg>
        Download MP3
      </button>
    </div>

  </div>

  <!-- Toast Container -->
  <div class="toast-box" id="toastContainer"></div>

  <!-- Three.js 3D Interactive Scene Script -->
  <script>
    let scene, camera, renderer, particles, torusKnot, ring1, ring2;
    let mouseX = 0, mouseY = 0;
    let windowHalfX = window.innerWidth / 2;
    let windowHalfY = window.innerHeight / 2;
    let isWarpSpeed = false;

    function init3DScene() {
      const canvas = document.getElementById('webgl-canvas');
      scene = new THREE.Scene();
      scene.fog = new THREE.FogExp2(0x040711, 0.0018);

      camera = new THREE.PerspectiveCamera(65, window.innerWidth / window.innerHeight, 1, 3000);
      camera.position.z = 1000;

      renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

      // 1. Cosmic Particles Vortex (2,000 points)
      const particleCount = 2000;
      const geometry = new THREE.BufferGeometry();
      const positions = new Float32Array(particleCount * 3);
      const colors = new Float32Array(particleCount * 3);

      const color1 = new THREE.Color(0x00f2fe);
      const color2 = new THREE.Color(0x8b5cf6);
      const color3 = new THREE.Color(0x4facfe);

      for (let i = 0; i < particleCount; i++) {
        const i3 = i * 3;
        const radius = 300 + Math.random() * 1200;
        const theta = Math.random() * Math.PI * 2;
        const phi = (Math.random() - 0.5) * Math.PI;

        positions[i3] = radius * Math.cos(theta) * Math.cos(phi);
        positions[i3 + 1] = radius * Math.sin(phi);
        positions[i3 + 2] = radius * Math.sin(theta) * Math.cos(phi);

        const mixedColor = Math.random() > 0.5 ? color1.clone().lerp(color2, Math.random()) : color3;
        colors[i3] = mixedColor.r;
        colors[i3 + 1] = mixedColor.g;
        colors[i3 + 2] = mixedColor.b;
      }

      geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

      const particleMaterial = new THREE.PointsMaterial({
        size: 3.5,
        vertexColors: true,
        transparent: true,
        opacity: 0.75,
        blending: THREE.AdditiveBlending
      });

      particles = new THREE.Points(geometry, particleMaterial);
      scene.add(particles);

      // 2. Central 3D Cyber Torus Knot Core
      const knotGeo = new THREE.TorusKnotGeometry(140, 28, 120, 16);
      const knotMat = new THREE.MeshBasicMaterial({
        color: 0x00f2fe,
        wireframe: true,
        transparent: true,
        opacity: 0.18
      });
      torusKnot = new THREE.Mesh(knotGeo, knotMat);
      torusKnot.position.set(0, 40, -100);
      scene.add(torusKnot);

      // 3. Concentric Orbital Cyber Rings
      const ringGeo1 = new THREE.RingGeometry(220, 222, 64);
      const ringMat1 = new THREE.MeshBasicMaterial({ color: 0x8b5cf6, side: THREE.DoubleSide, transparent: true, opacity: 0.25 });
      ring1 = new THREE.Mesh(ringGeo1, ringMat1);
      ring1.position.set(0, 40, -100);
      ring1.rotation.x = Math.PI / 3;
      scene.add(ring1);

      const ringGeo2 = new THREE.RingGeometry(260, 262, 64);
      const ringMat2 = new THREE.MeshBasicMaterial({ color: 0x00f2fe, side: THREE.DoubleSide, transparent: true, opacity: 0.2 });
      ring2 = new THREE.Mesh(ringGeo2, ringMat2);
      ring2.position.set(0, 40, -100);
      ring2.rotation.y = Math.PI / 4;
      scene.add(ring2);

      // Listeners
      window.addEventListener('resize', onWindowResize, false);
      document.addEventListener('mousemove', onDocumentMouseMove, false);
      animate3D();
    }

    function onWindowResize() {
      windowHalfX = window.innerWidth / 2;
      windowHalfY = window.innerHeight / 2;
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }

    function onDocumentMouseMove(event) {
      mouseX = (event.clientX - windowHalfX) * 0.4;
      mouseY = (event.clientY - windowHalfY) * 0.4;
    }

    function animate3D() {
      requestAnimationFrame(animate3D);

      // Smooth Camera Parallax Lerp
      camera.position.x += (mouseX - camera.position.x) * 0.04;
      camera.position.y += (-mouseY - camera.position.y) * 0.04;
      camera.lookAt(scene.position);

      const rotSpeed = isWarpSpeed ? 0.04 : 0.003;

      if (particles) {
        particles.rotation.y += rotSpeed * 0.8;
        particles.rotation.x += rotSpeed * 0.4;
      }
      if (torusKnot) {
        torusKnot.rotation.x += rotSpeed * 1.5;
        torusKnot.rotation.y += rotSpeed * 2;
      }
      if (ring1) ring1.rotation.z += rotSpeed * 1.2;
      if (ring2) ring2.rotation.z -= rotSpeed * 1.5;

      renderer.render(scene, camera);
    }

    // Initialize 3D Scene when DOM is ready
    window.addEventListener('DOMContentLoaded', init3DScene);

    // 3D Tilt Effect on Console Card
    const consoleCard = document.getElementById('mainConsoleCard');
    if (consoleCard) {
      consoleCard.addEventListener('mousemove', (e) => {
        const rect = consoleCard.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * -6;
        const rotateY = ((x - centerX) / centerX) * 6;

        consoleCard.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.01, 1.01, 1.01)`;
      });

      consoleCard.addEventListener('mouseleave', () => {
        consoleCard.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
      });
    }

    // --- State & Handlers ---
    let currentTargetUrl = "";
    let currentData = null;
    let currentSelectedQuality = null;

    function showToast(msg) {
      const container = document.getElementById('toastContainer');
      const toast = document.createElement('div');
      toast.className = 'toast';
      toast.innerHTML = `
        <svg width="18" height="18" fill="none" stroke="#00f2fe" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"></path></svg>
        <span>${escapeHtml(msg)}</span>
      `;
      container.appendChild(toast);
      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-20px)';
        setTimeout(() => toast.remove(), 300);
      }, 3500);
    }

    async function pasteClipboard() {
      try {
        const text = await navigator.clipboard.readText();
        if (text) {
          document.getElementById('urlField').value = text.trim();
          showToast("Link pasted from clipboard!");
          handleExtract();
        }
      } catch (e) {
        document.getElementById('urlField').focus();
      }
    }

    function switchFormatMode(mode) {
      const vGrid = document.getElementById('videoGrid');
      const aGrid = document.getElementById('audioGrid');
      const btnV = document.getElementById('tabVideo');
      const btnA = document.getElementById('tabAudio');

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
      if (!bytes || bytes === 0 || isNaN(bytes)) return 'Lossless HD';
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return (bytes / Math.pow(k, i)).toFixed(1) + ' ' + sizes[i];
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
      const dock = document.getElementById('quantumDock');

      loaderBox.style.display = 'block';
      errorAlert.style.display = 'none';
      resultHub.style.display = 'none';
      dock.style.display = 'none';
      extractBtn.disabled = true;
      isWarpSpeed = true;

      // Animated Step Messages
      const stepText = document.getElementById('loaderStepText');
      stepText.textContent = "Connecting to Zero-Proxy Direct Engine...";
      const stepTimer1 = setTimeout(() => stepText.textContent = "Resolving CDN video & audio streams...", 1800);
      const stepTimer2 = setTimeout(() => stepText.textContent = "Synthesizing full multi-quality presets...", 3500);

      try {
        const res = await fetch(`/api/info?url=${encodeURIComponent(url)}`);
        const data = await res.json();

        if (!res.ok || data.status !== 'success') {
          throw new Error(data.detail || data.message || 'Media extraction failed. Please check the URL.');
        }

        currentData = data;

        // Render Hero Preview
        document.getElementById('cardTitle').textContent = data.title || 'Untitled Video';
        document.getElementById('cardThumb').src = data.thumbnail || 'https://via.placeholder.com/640x360?text=Stream+Preview';
        document.getElementById('cardDuration').textContent = data.duration || 'Full HD';
        document.getElementById('cardEngine').textContent = `ENGINE: ${(data.engine || 'ZERO-PROXY DIRECT').toUpperCase()}`;

        const vList = data.videos || [];
        const aList = data.audios || [];
        document.getElementById('cardTotalStreams').textContent = `${vList.length + aList.length} Qualities Generated`;
        document.getElementById('labelVideoCount').textContent = `Video (${vList.length})`;
        document.getElementById('labelAudioCount').textContent = `Audio (${aList.length})`;

        // Populate Video Cards Grid
        const vGrid = document.getElementById('videoGrid');
        vGrid.innerHTML = '';
        vList.forEach((v, idx) => {
          const card = document.createElement('div');
          card.className = `quality-3d-card ${idx === 0 ? 'selected' : ''}`;
          card.onclick = () => selectCard(v, 'video', card);

          const qStr = String(v.quality || '720P').toUpperCase();
          let pillCls = "";
          let pillLabel = "HD STREAM";
          if (qStr.includes("1080") || qStr.includes("4K")) { pillCls = "gold"; pillLabel = "4K / FHD"; }
          else if (qStr.includes("720")) { pillCls = ""; pillLabel = "RECOMMENDED"; }
          else { pillCls = "purple"; pillLabel = "COMPACT"; }

          const streamLink = `/api/stream?url=${encodeURIComponent(url)}&type=video&quality=${encodeURIComponent(v.quality)}`;

          card.innerHTML = `
            <div>
              <div class="q-header">
                <div class="q-badge">
                  <span>${escapeHtml(v.quality || 'HD')}</span>
                </div>
                <span class="q-pill ${pillCls}">${pillLabel}</span>
              </div>
              <div class="q-specs">
                <div><span>Container:</span><b>${escapeHtml((v.format || 'mp4').toUpperCase())}</b></div>
                <div><span>Estimated Size:</span><b>${formatBytes(v.size)}</b></div>
                <div><span>Soundtrack:</span><b>🔊 Integrated</b></div>
              </div>
            </div>
            <button class="btn-card-stream" onclick="event.stopPropagation(); triggerDownload('${streamLink}')">
              <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
              Download ${escapeHtml(v.quality || 'Video')}
            </button>
          `;
          vGrid.appendChild(card);
          if (idx === 0) selectCard(v, 'video', card);
        });

        // Populate Audio Cards Grid
        const aGrid = document.getElementById('audioGrid');
        aGrid.innerHTML = '';
        aList.forEach((a, idx) => {
          const card = document.createElement('div');
          card.className = 'quality-3d-card';
          card.onclick = () => selectCard(a, 'audio', card);

          const streamLink = `/api/stream?url=${encodeURIComponent(url)}&type=audio&quality=${encodeURIComponent(a.quality || 'best')}`;

          card.innerHTML = `
            <div>
              <div class="q-header">
                <div class="q-badge">
                  <span>${escapeHtml(a.quality || 'MP3')}</span>
                </div>
                <span class="q-pill purple">LOSSLESS MP3</span>
              </div>
              <div class="q-specs">
                <div><span>Codec:</span><b>MP3 AUDIO</b></div>
                <div><span>Bitrate:</span><b>${escapeHtml(a.quality || '320kbps')}</b></div>
                <div><span>File Size:</span><b>${formatBytes(a.size)}</b></div>
              </div>
            </div>
            <button class="btn-card-stream" onclick="event.stopPropagation(); triggerDownload('${streamLink}')">
              <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M9 19V6l12-3v13"></path></svg>
              Download MP3 (${escapeHtml(a.quality)})
            </button>
          `;
          aGrid.appendChild(card);
        });

        resultHub.style.display = 'block';
        dock.style.display = 'flex';
        resultHub.scrollIntoView({ behavior: 'smooth', block: 'start' });
        showToast("Streams extracted successfully!");

      } catch (err) {
        clearTimeout(stepTimer1);
        clearTimeout(stepTimer2);
        document.getElementById('errorMessage').textContent = err.message || 'An error occurred while fetching media.';
        errorAlert.style.display = 'flex';
      } finally {
        isWarpSpeed = false;
        loaderBox.style.display = 'none';
        extractBtn.disabled = false;
      }
    }

    function selectCard(item, type, element) {
      document.querySelectorAll('.quality-3d-card').forEach(c => c.classList.remove('selected'));
      element.classList.add('selected');
      currentSelectedQuality = { item, type };

      const q = item.quality || (type === 'video' ? 'Best Video' : 'Best Audio');
      const f = (item.format || (type === 'video' ? 'mp4' : 'mp3')).toUpperCase();
      document.getElementById('dockTitle').textContent = `Selected: ${q} (${f})`;
      document.getElementById('dockSub').textContent = `Size: ${formatBytes(item.size)} • Ready to download`;
    }

    function downloadSelectedStream() {
      if (!currentTargetUrl) return;
      const q = (currentSelectedQuality && currentSelectedQuality.item && currentSelectedQuality.item.quality) ? currentSelectedQuality.item.quality : 'best';
      const type = (currentSelectedQuality && currentSelectedQuality.type) ? currentSelectedQuality.type : 'video';
      const streamUrl = `/api/stream?url=${encodeURIComponent(currentTargetUrl)}&type=${type}&quality=${encodeURIComponent(q)}`;
      triggerDownload(streamUrl);
    }

    function downloadBestAudio() {
      if (!currentTargetUrl) return;
      const audioUrl = `/api/stream?url=${encodeURIComponent(currentTargetUrl)}&type=audio&quality=best`;
      triggerDownload(audioUrl);
    }

    function triggerDownload(streamUrl) {
      showToast("Starting direct high-speed download...");
      window.location.href = streamUrl;
    }

    function escapeHtml(str) {
      return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
  </script>
</body>
</html>"""
