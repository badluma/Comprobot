import os
import socket
import subprocess
import webbrowser
from pathlib import Path

from .data import DATA_DIR

# Dashboard release this bot is compatible with. The installer reads this via
# `comprobot --dashboard-version` to fetch the matching tarball. Bump on every
# release that requires a newer dashboard.
DASHBOARD_VERSION = "v1.0.0"

PORT = int(os.environ.get("DASHBOARD_PORT", "7626"))
URL = f"http://localhost:{PORT}"

def _dashboard_dir() -> Path:
    return Path(DATA_DIR) / "dashboard"

def _port_in_use() -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", PORT)) == 0

def launch(foreground: bool = False):
    dashboard = _dashboard_dir()
    if not dashboard.exists():
        print(f"Dashboard directory not found: {dashboard}")
        return
    if _port_in_use():
        print(f"Dashboard already running at {URL}")
        return
    env = {**os.environ, "PORT": str(PORT)}
    if foreground:
        print(f"Starting dashboard at {URL} (Ctrl+C to stop)")
        webbrowser.open(URL)
        subprocess.run(["bun", "run", "index.ts"], cwd=dashboard, env=env)
    else:
        print(f"Dashboard running at {URL}")
        subprocess.Popen(["bun", "run", "index.ts"], cwd=dashboard, env=env)
