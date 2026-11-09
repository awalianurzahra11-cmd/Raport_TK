import os
import sys
import uvicorn

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

if __name__ == "__main__":
    print("=" * 60)
    print(" [OK] E-Raport TK ABK - FastAPI Server (backend-fix)")
    print(" [*] Server URL : http://127.0.0.1:8000 (Port 8000)")
    print(" [*] API Docs   : http://127.0.0.1:8000/docs")
    print("=" * 60)
    try:
        uvicorn.run(
            "backend.app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
        )
    except KeyboardInterrupt:
        print("\n[INFO] Server dihentikan.")
