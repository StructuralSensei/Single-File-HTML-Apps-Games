import http.server
import socketserver
import webbrowser
import urllib.parse
import os
import sys
import threading

PORT = 8000

GAMES = [
    ("tactical-breach.html", "🎯", "3D First-Person Wave Shooter", "Hold the arena through escalating Heat Waves and buy weapons between breaches."),
    ("neon-swarm.html", "⚡", "Reverse Bullet-Hell Roguelite", "Auto-firing arena survival with magnetic XP shards and level-up drafts."),
    ("fruit-jar.html", "🍉", "Physics Fruit Merge Puzzle", "Suika-style drop-and-merge physics game with combos and high scores."),
    ("orbital-sandbox.html", "🪐", "N-Body Gravity Simulator", "Slingshot planets into orbit and experiment with Black Hole mode."),
]

APPS = [
    ("command-center.html", "🌐", "Live Global Intelligence Dashboard", "Real-time weather, crypto, forex, earthquakes, and tech news."),
    ("night-in.html", "🍿", "All-in-One Evening Planner", "Find fridge recipes, swipe TV shows, and spin background music."),
    ("stillwater.html", "🎧", "Procedural Ambient Sound Mixer", "Six Web Audio API soundscapes with a 40Hz binaural focus channel."),
    ("infinite-board.html", "📐", "Spatial Mind-Map & Sticky Canvas", "Offline infinite canvas for sticky notes, node links, and PNG export."),
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Structural Sensei | Single-File HTML Apps &amp; Games</title>
<style>
    :root {
        --bg-primary: #090d16;
        --bg-surface: #0f1624;
        --bg-surface-hover: #141d2f;
        --border-subtle: rgba(148, 163, 184, 0.12);
        --border-accent: rgba(245, 158, 11, 0.45);
        --accent: #f59e0b;
        --accent-hover: #fbbf24;
        --accent-soft: rgba(245, 158, 11, 0.12);
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --text-dim: #64748b;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
        font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        background-color: var(--bg-primary);
        background-image:
            linear-gradient(to right, rgba(255, 255, 255, 0.025) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255, 255, 255, 0.025) 1px, transparent 1px);
        background-size: 40px 40px;
        color: var(--text-main);
        line-height: 1.55;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }
    .navbar {
        border-bottom: 1px solid var(--border-subtle);
        background: rgba(9, 13, 22, 0.85);
        backdrop-filter: blur(12px);
        position: sticky;
        top: 0;
        z-index: 10;
    }
    .nav-inner {
        max-width: 1160px;
        margin: 0 auto;
        padding: 14px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
        text-decoration: none;
        color: var(--text-main);
        font-weight: 700;
        font-size: 1.08rem;
        letter-spacing: -0.01em;
    }
    .brand-mark {
        width: 30px;
        height: 30px;
        border-radius: 7px;
        background: var(--accent-soft);
        border: 1px solid var(--border-accent);
        color: var(--accent);
        display: grid;
        place-items: center;
        font-weight: 800;
        font-size: 0.9rem;
    }
    .brand em { font-style: italic; color: var(--accent); font-weight: 800; }
    .nav-links { display: flex; align-items: center; gap: 20px; }
    .nav-links a {
        color: var(--text-muted);
        text-decoration: none;
        font-size: 0.85rem;
        font-weight: 500;
        transition: color 0.15s ease;
    }
    .nav-links a:hover { color: var(--accent); }
    .status-pill {
        font-size: 0.75rem;
        font-weight: 600;
        color: #10b981;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.25);
        padding: 4px 10px;
        border-radius: 999px;
    }
    .container {
        max-width: 1160px;
        width: 100%;
        margin: 0 auto;
        padding: 36px 24px 64px;
        flex: 1;
    }
    .hero {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        gap: 24px;
        padding-bottom: 28px;
        border-bottom: 1px solid var(--border-subtle);
        margin-bottom: 32px;
        flex-wrap: wrap;
    }
    .eyebrow {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--accent);
        background: var(--accent-soft);
        border: 1px solid var(--border-accent);
        padding: 4px 10px;
        border-radius: 6px;
        margin-bottom: 12px;
    }
    .hero h1 { font-size: 1.95rem; font-weight: 800; letter-spacing: -0.025em; line-height: 1.2; }
    .hero p { color: var(--text-muted); margin-top: 8px; max-width: 600px; font-size: 0.94rem; }
    .stats {
        display: flex;
        gap: 24px;
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        padding: 14px 20px;
        border-radius: 12px;
    }
    .stat-item strong {
        display: block;
        font-size: 1.25rem;
        font-weight: 800;
        color: var(--accent);
        line-height: 1.1;
    }
    .stat-item span {
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 32px 0 16px;
    }
    .section-header h2 {
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        color: var(--text-main);
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-header h2::before {
        content: "";
        width: 8px;
        height: 8px;
        border-radius: 2px;
        background: var(--accent);
        display: inline-block;
    }
    .section-header span { font-size: 0.8rem; color: var(--text-dim); }
    .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
    @media (max-width: 980px) { .grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 560px) { .grid { grid-template-columns: 1fr; } }
    .card {
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease;
    }
    .card:hover {
        transform: translateY(-3px);
        border-color: var(--border-accent);
        background: var(--bg-surface-hover);
    }
    .card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
    }
    .icon-box {
        width: 38px;
        height: 38px;
        border-radius: 9px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid var(--border-subtle);
        display: grid;
        place-items: center;
        font-size: 1.2rem;
    }
    .badge {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        padding: 3px 8px;
        border-radius: 5px;
        background: rgba(255, 255, 255, 0.05);
        color: var(--text-muted);
        border: 1px solid var(--border-subtle);
    }
    .card h3 { font-size: 1.08rem; font-weight: 700; color: var(--text-main); letter-spacing: -0.01em; }
    .subtitle { font-size: 0.8rem; color: var(--accent); font-weight: 600; margin-top: 3px; }
    .desc { font-size: 0.84rem; color: var(--text-muted); margin: 10px 0 20px; flex-grow: 1; }
    .btn {
        display: flex;
        justify-content: space-between;
        align-items: center;
        text-decoration: none;
        font-weight: 700;
        font-size: 0.86rem;
        padding: 10px 14px;
        border-radius: 8px;
        transition: all 0.15s ease;
    }
    .btn-primary { background: var(--accent); color: #090d16; }
    .btn-primary:hover { background: var(--accent-hover); }
    .btn-secondary {
        background: rgba(255, 255, 255, 0.05);
        color: var(--text-main);
        border: 1px solid var(--border-subtle);
    }
    .btn-secondary:hover { border-color: var(--accent); color: var(--accent); }
    .arrow { transition: transform 0.15s ease; }
    .btn:hover .arrow { transform: translateX(3px); }
    footer {
        border-top: 1px solid var(--border-subtle);
        padding: 20px 24px;
        text-align: center;
        color: var(--text-dim);
        font-size: 0.82rem;
    }
    footer a { color: var(--text-muted); text-decoration: none; }
    footer a:hover { color: var(--accent); }
</style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-inner">
            <a href="/" class="brand">
                <span class="brand-mark">SS</span>
                <span>Structural <em>Sensei</em></span>
            </a>
            <div class="nav-links">
                <a href="#">Website</a>
                <a href="#">GitHub Repo</a>
                <span class="status-pill">● Active on Port __PORT__</span>
            </div>
        </div>
    </nav>

    <main class="container">
        <section class="hero">
            <div>
                <span class="eyebrow">Single-File Web Suite</span>
                <h1>Browser Games &amp; Productivity Tools</h1>
                <p>Zero-dependency, self-contained HTML systems engineered for instant execution. Click any module below to launch in a dedicated browser tab.</p>
            </div>
            <div class="stats">
                <div class="stat-item"><strong>4</strong><span>Games</span></div>
                <div class="stat-item"><strong>4</strong><span>Apps</span></div>
                <div class="stat-item"><strong>0</strong><span>Dependencies</span></div>
            </div>
        </section>

        <div class="section-header">
            <h2>Interactive Games</h2>
            <span>4 Modules Available</span>
        </div>
        <div class="grid">
__GAMES__
        </div>

        <div class="section-header">
            <h2>Utility &amp; Lifestyle Apps</h2>
            <span>4 Modules Available</span>
        </div>
        <div class="grid">
__APPS__
        </div>
    </main>

    <footer>
        Built with purpose by Structural Sensei · Mastering the art of design, one system at a time.
    </footer>
</body>
</html>
"""


def get_resource_dir():
    """When frozen into an .exe, serve files from the folder that contains the .exe.
    Otherwise, serve from the folder that contains this script."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def render_cards(items, badge_text, btn_label, is_primary=True):
    cards = []
    for filename, icon, subtitle, desc in items:
        title = os.path.splitext(filename)[0].replace("-", " ").title()
        encoded_url = "/" + urllib.parse.quote(filename)
        btn_class = "btn btn-primary" if is_primary else "btn btn-secondary"
        cards.append(f"""
        <div class="card">
            <div class="card-top">
                <div class="icon-box">{icon}</div>
                <span class="badge">{badge_text}</span>
            </div>
            <h3>{title}</h3>
            <p class="subtitle">{subtitle}</p>
            <p class="desc">{desc}</p>
            <a href="{encoded_url}" target="_blank" rel="noopener" class="{btn_class}">
                <span>{btn_label}</span>
                <span class="arrow">→</span>
            </a>
        </div>""")
    return "\n".join(cards)


def build_hub_html(active_port):
    return (
        HTML_TEMPLATE
        .replace("__PORT__", str(active_port))
        .replace("__GAMES__", render_cards(GAMES, "GAME", "Play Now", is_primary=True))
        .replace("__APPS__", render_cards(APPS, "APP", "Launch App", is_primary=False))
    )


class HubHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            content = build_hub_html(self.server.server_address[1]).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            super().do_GET()

    def log_message(self, format, *args):
        pass


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def start_server():
    os.chdir(get_resource_dir())
    for port in range(PORT, PORT + 20):
        try:
            return ReusableTCPServer(("127.0.0.1", port), HubHandler)
        except OSError:
            continue
    raise RuntimeError("Could not find an open local port.")


if __name__ == "__main__":
    httpd = start_server()
    url = f"http://127.0.0.1:{httpd.server_address[1]}/"
    print(f"🥋 Structural Sensei Launcher running at {url}")
    print("Close this window to stop the launcher.")

    threading.Timer(0.8, webbrowser.open, args=(url,)).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Launcher stopped.")
    finally:
        httpd.server_close()