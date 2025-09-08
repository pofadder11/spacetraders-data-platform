from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
import urllib.request
from typing import Optional


API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_BASE = os.getenv("API_BASE", f"http://{API_HOST}:{API_PORT}")


def wait_for_api(url: str, timeout: float = 20.0) -> bool:
    """Poll /summary until reachable or timeout."""
    deadline = time.time() + timeout
    target = url.rstrip("/") + "/summary"
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(target, timeout=2) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False


def main() -> int:
    env = os.environ.copy()
    # Ensure Panel knows where to find the API
    env.setdefault("API_BASE", API_BASE)

    runner_cmd = [sys.executable, "-m", "runners.async_main"]
    panel_cmd = [
        sys.executable,
        "-m",
        "panel",
        "serve",
        "display/panel_app.py",
        "--show",
        "--autoreload",
    ]

    print(f"[run] API_BASE={env['API_BASE']}")
    print("[run] Starting runner (async_main)...")
    runner = subprocess.Popen(runner_cmd, env=env)

    try:
        # Give runner a moment to start, then probe API
        if wait_for_api(API_BASE, timeout=30.0):
            print("[run] API is up. Starting Panel dashboard...")
        else:
            print("[warn] API not reachable yet; starting Panel anyway.")

        panel = subprocess.Popen(panel_cmd, env=env)

        # Wait on both; if either exits, terminate the other
        while True:
            rc_runner = runner.poll()
            rc_panel = panel.poll()
            if rc_runner is not None:
                print(f"[run] runner exited with code {rc_runner}. Shutting down Panel...")
                try:
                    if rc_panel is None:
                        panel.terminate()
                finally:
                    break
            if rc_panel is not None:
                print(f"[run] Panel exited with code {rc_panel}. Shutting down runner...")
                try:
                    if rc_runner is None:
                        runner.terminate()
                finally:
                    break
            time.sleep(0.5)

        # Give children a moment to exit cleanly
        time.sleep(1.0)
        return 0

    except KeyboardInterrupt:
        print("\n[run] Ctrl+C received. Terminating processes...")
        try:
            runner.terminate()
        except Exception:
            pass
        try:
            panel.terminate()  # type: ignore[name-defined]
        except Exception:
            pass
        return 0

    except Exception as e:
        print(f"[run] Unexpected error: {e}")
        try:
            runner.terminate()
        except Exception:
            pass
        try:
            panel.terminate()  # type: ignore[name-defined]
        except Exception:
            pass
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

