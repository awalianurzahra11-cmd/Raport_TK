import os
import sys
import subprocess
import signal
import time

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend-react")

processes = []

def signal_handler(sig, frame):
    print("\n[INFO] Menghentikan semua service (Backend & Vite React)...")
    for p in processes:
        try:
            if sys.platform == "win32":
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                p.terminate()
        except Exception:
            pass
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    print("=" * 65)
    print("   E-RAPORT TK ABK — DUAL DEV SERVER (BACKEND + FRONTEND REACT)")
    print("=" * 65)
    print(" 1. Backend FastAPI  : http://127.0.0.1:8000")
    print(" 2. Frontend React   : http://localhost:5173")
    print("=" * 65)
    print(" Tekan Ctrl+C untuk menghentikan kedua server sekaligus.")
    print("=" * 65)

    # 1. Jalankan Backend
    p_back = subprocess.Popen([sys.executable, "run_backend.py"], cwd=ROOT_DIR)
    processes.append(p_back)

    time.sleep(1.5)

    # 2. Jalankan Frontend React
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    p_front = subprocess.Popen([npm_cmd, "run", "dev"], cwd=FRONTEND_DIR)
    processes.append(p_front)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)
