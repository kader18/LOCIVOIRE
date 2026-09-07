/**
 * Prépare le dossier www (splash / fallback hors-ligne).
 * L'app Capacitor charge ensuite le serveur Locivoire (Django).
 */
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const www = path.join(root, 'www');

if (!fs.existsSync(www)) fs.mkdirSync(www, { recursive: true });

const html = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="theme-color" content="#101A30" />
  <title>Locivoire</title>
  <style>
    :root {
      --navy: #1B2A4A;
      --navy-deep: #101A30;
      --gold: #D9A441;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      height: 100%;
      font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
      background: linear-gradient(165deg, #0c1322 0%, var(--navy-deep) 45%, #15233f 100%);
      color: #fff;
    }
    .wrap {
      min-height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 32px 24px;
      text-align: center;
    }
    .flag { position: fixed; top: 0; left: 0; right: 0; height: 4px; display: flex; }
    .flag span { flex: 1; }
    .flag .o { background: #F77F00; }
    .flag .w { background: #fff; }
    .flag .g { background: #009E60; }
    .mark {
      width: 78px; height: 78px; border-radius: 18px;
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(217,164,65,0.45);
      display: grid; place-items: center;
      margin-bottom: 20px;
      color: var(--gold);
      box-shadow: 0 18px 50px rgba(0,0,0,0.35);
    }
    .mark svg { width: 38px; height: 38px; }
    h1 {
      font-size: 2rem; font-weight: 600; letter-spacing: -0.02em;
      margin-bottom: 8px;
    }
    p { color: rgba(245,230,200,0.8); font-size: 0.9rem; max-width: 280px; line-height: 1.45; }
    .bar {
      width: 180px; height: 2px; margin-top: 28px; border-radius: 99px;
      background: rgba(255,255,255,0.12); overflow: hidden;
    }
    .bar span {
      display: block; height: 100%; width: 40%;
      background: linear-gradient(90deg, #B9822A, var(--gold), #f0d48a);
      animation: load 1.4s ease-in-out infinite;
    }
    @keyframes load {
      0% { transform: translateX(-100%); }
      100% { transform: translateX(280%); }
    }
    .hint {
      margin-top: 40px; font-size: 0.75rem; opacity: 0.55;
    }
  </style>
</head>
<body>
  <div class="flag" aria-hidden="true"><span class="o"></span><span class="w"></span><span class="g"></span></div>
  <div class="wrap">
    <div class="mark">
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M3 11L12 4l9 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M5 10v9a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1v-9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <h1>Locivoire</h1>
    <p>Côte d'Ivoire · maisons &amp; visites immersives</p>
    <div class="bar" aria-hidden="true"><span></span></div>
    <p class="hint">Chargement de l'application…</p>
  </div>
</body>
</html>
`;

fs.writeFileSync(path.join(www, 'index.html'), html);
console.log('www/ prêt (splash Locivoire)');
