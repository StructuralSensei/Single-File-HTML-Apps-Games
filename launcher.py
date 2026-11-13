import http.server
import socketserver
import webbrowser
import urllib.parse
import os
import threading
import time

PORT = 8000

GAMES = {
    "Tactical Breach.html": ("🎮", "3D First-Person Wave Shooter", "Hold the arena through escalating Heat Waves and buy weapons between breaches."),
    "neon-swarm.html": ("⚡", "Reverse Bullet-Hell Roguelite", "Auto-firing arena survival with magnetic XP shards and level-up drafts."),
    "FRUIT JAR.html": ("🍉", "Physics Fruit Merge Puzzle", "Suika-style drop-and-merge physics game with combos and high scores."),
    "Orbital Sandbox.html": ("🪐", "N-Body Gravity Simulator", "Slingshot planets into orbit and experiment with Black Hole mode."),
}

APPS = {
    "Command Center.html": ("🌐", "Live Global Intelligence Dashboard", "Real-time weather, crypto, forex, earthquakes, and tech news."),
    "NIGHT IN.html": ("🍿", "All-in-One Evening Planner", "Find fridge recipes, swipe TV shows, and spin background music."),
    "Stillwater.html": ("🎧", "Procedural Ambient Sound Mixer", "Six Web Audio API soundscapes with a 40Hz binaural focus channel."),
    "infinite-board.html": ("🧠", "Spatial Mind-Map & Sticky Canvas", "Offline infinite canvas for sticky notes, node links, and PNG export."),
}


def build_hub_html():
    html_files = sorted([f for f in os.listdir(".") if f.lower().endswith(".html")])

    def render_cards(catalog, badge_text, btn_label, btn_color):
        cards = []
        for filename in html_files:
            if filename in catalog:
                icon, subtitle, desc = catalog[filename]
                title = os.path.splitext(filename)[0].replace("-", " ").title()
                encoded_url = "/" + urllib.parse.quote(filename)
                cards.append(f"""
                <div class="card">
                    <div class="card-top">
                        <span class="icon">{icon}</span>
                        <span class="badge">{badge_text}</span>
                    </div>
                    <h3>{title}</h3>
                    <p class="subtitle">{subtitle}</p>
                    <p class="desc">{desc}</p>
                    <a href="{encoded_url}" target="_blank" rel="noopener" class="btn" style="background:{btn_color}">
                        {btn_label} ↗
                    </a>
                </div>
                """)
        return "\n".join(cards)

    # Catch any extra .html files added later that aren't in GAMES or APPS yet
    known = set(GAMES.keys()) | set(APPS.keys())
    extra_cards = []
    for filename in html_files:
        if filename not in known:
            title = os.path.splitext(filename)[0].replace("-", " ").title()
            encoded_url = "/" + urllib.parse.quote(filename)
            extra_cards.append(f"""
            <div class="card">
                <div class="card-top">
                    <span class="icon">✨</span>
                    <span class="badge">HTML App</span>
                </div>
                <h3>{title}</h3>
                <p class="subtitle">Single-File Web App</p>
                <p class="desc">Standalone local browser application.</p>
                <a href="{encoded_url}" target="_blank" rel="noopener" class="btn" style="background:#6366f1">
                    Open App ↗
                </a>
            </div>
            """)

    games_html = render_cards(GAMES, "GAME", "▶ Play Now", "#ef4444")
    apps_html = render_cards(APPS, "APP", "🚀 Launch App", "#10b981")
    extras_html = "\n".join(extra_cards)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Single-File HTML Apps & Games Launcher</title>
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        background: #0b0f19;
        color: #f8fafc;
        padding: 32px 24px 60px;
        line-height: 1.5;
    }}
    .container {{ max-width: 1120px; margin: 0 auto; }}
    header {{
        text-align: center;
        margin-bottom: 40px;
        padding-bottom: 24px;
        border-bottom: 1px solid #1e293b;
    }}
    header h1 {{ font-size: 2rem; font-weight: 800; letter-spacing: -0.02em; }}
    header p {{ color: #94a3b8; margin-top: 8px; font-size: 0.98rem; }}
    h2 {{
        font-size: 1.15rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
        margin: 32px 0 16px;
    }}
    .grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 18px;
    }}
    .card {{
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }}
    .card:hover {{ transform: translateY(-3px); border-color: #374151; }}
    .card-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
    .icon {{ font-size: 1.7rem; }}
    .badge {{
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        padding: 3px 8px;
        border-radius: 999px;
        background: #1e293b;
        color: #cbd5e1;
    }}
    .card h3 {{ font-size: 1.15rem; font-weight: 700; color: #f1f5f9; }}
    .subtitle {{ font-size: 0.82rem; color: #38bdf8; font-weight: 600; margin-top: 2px; }}
    .desc {{ font-size: 0.86rem; color: #94a3b8; margin: 10px 0 18px; flex-grow: 1; }}
    .btn {{
        display: block;
        text-align: center;
        text-decoration: none;
        color: #ffffff;
        font-weight: 700;
        font-size: 0.9rem;
        padding: 10px 14px;
        border-radius: 9px;
        transition: opacity 0.15s ease;
    }}
    .btn:hover {{ opacity: 0.9; }}
</style>
</head>
<body>
<div class="container">
    <header>
        <h1>🎮 Single-File HTML Apps & Games</h1>
        <p>Click any button below to launch the app or game in a new browser tab.</p>
    </header>

    <h2>🕹️ Browser Games</h2>
    <div class="grid">{games_html}</div>

    <h2>🛠️ Utility & Lifestyle Apps</h2>
    <div class="grid">{apps_html}{extras_html}</div>
</div>
</body>
</html>"""


class HubHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            content = build_hub_html().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            super().do_GET()

    def log_message(self, format, *args):
        pass  # Keep terminal output clean


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def open_browser():
    time.sleep(0.6)
    webbrowser.open(f"http://localhost:{PORT}/")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"🚀 Launcher running at http://localhost:{PORT}/ (Press Ctrl+C to stop)")
    threading.Thread(target=open_browser, daemon=True).start()
    with ReusableTCPServer(("", PORT), HubHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Launcher stopped.")
