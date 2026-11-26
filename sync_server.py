#!/usr/bin/env python3
"""Local Plug Shelf server: static files plus a GitHub sync endpoint.

The browser never sees a token. It POSTs its current edits to /api/sync; this
helper compares them with edits.json, commits only that file, pushes to GitHub,
rebuilds the public site and redeploys to Vercel.
"""
import json
import mimetypes
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = 8902
BINDINGS = ["127.0.0.1", "192.168.1.79", "100.74.139.124"]
MISE = "/usr/sbin/mise"
SYNC_LOCK = threading.Lock()
LIVE_URL = "https://plug-shelf.vercel.app"


def run(cmd, timeout=240):
    return subprocess.run(
        cmd, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False
    )


class Handler(BaseHTTPRequestHandler):
    server_version = "PlugShelfLocal/1.0"

    def log_message(self, fmt, *args):
        if not self.path.startswith("/api/"):
            return
        print("[plug-shelf]", fmt % args, flush=True)

    def reply(self, code, body, ctype="application/json"):
        if isinstance(body, str):
            data = body.encode("utf-8")
        elif isinstance(body, (bytes, bytearray)):
            data = bytes(body)
        else:
            data = json.dumps(body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            target, ctype = ROOT / "index.html", "text/html; charset=utf-8"
        elif path in ("/edits.json", "/DESIGN.md", "/README.md"):
            target = ROOT / path.lstrip("/")
            ctype = "application/json" if path.endswith(".json") else "text/plain; charset=utf-8"
        elif path.startswith("/assets/"):
            name = Path(path).name
            target = ROOT / "assets" / name
            ctype = mimetypes.guess_type(name)[0] or "application/octet-stream"
        else:
            return self.reply(404, {"error": "not found"})
        if not target.is_file() or ROOT not in target.resolve().parents:
            return self.reply(404, {"error": "not found"})
        self.reply(200, target.read_bytes(), ctype)

    def do_POST(self):
        if self.path.split("?", 1)[0] != "/api/sync":
            return self.reply(404, {"error": "not found"})
        if self.client_address[0] != "127.0.0.1":
            return self.reply(403, {"error": "Sync is only available from this laptop"})
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > 3_000_000:
            return self.reply(413, {"error": "Invalid payload size"})
        raw = self.rfile.read(length)
        try:
            incoming = json.loads(raw)
        except Exception:
            return self.reply(400, {"error": "Payload is not valid JSON"})
        if not isinstance(incoming, dict):
            return self.reply(400, {"error": "Expected an object keyed by plugin slug"})
        for slug, override in incoming.items():
            if not isinstance(slug, str) or not isinstance(override, dict):
                return self.reply(400, {"error": "Invalid plugin entry"})

        with SYNC_LOCK:
            edits_path = ROOT / "edits.json"
            current = json.loads(edits_path.read_text())
            if incoming == current:
                return self.reply(200, {"status": "unchanged", "message": "Already up to date"})

            (ROOT / "edits.json.pre-sync").write_text(json.dumps(current, indent=2) + "\n")
            edits_path.write_text(json.dumps(incoming, indent=2) + "\n")

            add = run(["git", "add", "--", "edits.json"])
            if add.returncode:
                return self.reply(500, {"error": "git add failed", "detail": add.stderr})
            commit = run(["git", "commit", "-m", "Sync edits from local browser", "--", "edits.json"])
            if commit.returncode:
                return self.reply(500, {"error": "git commit failed", "detail": commit.stderr})
            sha = run(["git", "rev-parse", "--short", "HEAD"]).stdout.strip()

            push = run(["git", "push", "origin", "master"])
            if push.returncode:
                return self.reply(502, {"error": "git push failed", "detail": push.stderr})

            build = run([sys.executable, "build-live.py"])
            if build.returncode:
                return self.reply(500, {"error": "public rebuild failed", "detail": build.stderr})

            deploy = run([MISE, "exec", "node@26.8.1", "--", "vercel", "deploy", "--prod", "--yes"])
            deployed = deploy.returncode == 0

            return self.reply(200, {
                "status": "synced",
                "commit": sha,
                "deployed": deployed,
                "url": LIVE_URL if deployed else None,
                "message": "Synced to GitHub and Vercel" if deployed else "GitHub updated; Vercel deploy failed",
            })


def main():
    servers = []
    for address in BINDINGS:
        server = ThreadingHTTPServer((address, PORT), Handler)
        server.daemon_threads = True
        servers.append(server)
    for server in servers[1:]:
        threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"Plug Shelf local server on port {PORT}: {', '.join(BINDINGS)}", flush=True)
    print("Sync endpoint: POST /api/sync (loopback only)", flush=True)
    try:
        servers[0].serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        for server in servers:
            server.shutdown()


if __name__ == "__main__":
    main()
