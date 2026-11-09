from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# Load .env file from BASE_DIR and current directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

# Determine database URL with smart fallback:
# 1. Environment variable DATABASE_URL
# 2. MySQL with password sql123
# 3. MySQL with empty password
# 4. Fallback to SQLite
DATABASE_URL = os.getenv("DATABASE_URL")

def _init_engine(url: str):
    if url.startswith("sqlite"):
        return create_engine(
            url,
            connect_args={"check_same_thread": False},
        )
    else:
        return create_engine(
            url,
            pool_pre_ping=True,
            pool_recycle=3600,
        )

engine = None
if DATABASE_URL:
    try:
        eng = _init_engine(DATABASE_URL)
        with eng.connect() as conn:
            pass
        engine = eng
        print(f"[DB] Terhubung menggunakan DATABASE_URL: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL}")
    except Exception as e:
        print(f"[WARN] Gagal terhubung ke DATABASE_URL ({e}). Mencoba koneksi alternatif...")

if engine is None:
    # Try default MySQL credentials
    candidate_urls = [
        "mysql+pymysql://root:sql123@127.0.0.1:3306/raport_tk",
        "mysql+pymysql://root:@127.0.0.1:3306/raport_tk",
    ]
    for cand in candidate_urls:
        try:
            eng = _init_engine(cand)
            with eng.connect() as conn:
                pass
            engine = eng
            DATABASE_URL = cand
            print(f"[DB] Terhubung ke MySQL: {cand.split('@')[-1]}")
            break
        except Exception:
            continue

if engine is None:
    DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'rapor_tk.db')}"
    engine = _init_engine(DATABASE_URL)
    print(f"[DB] MySQL tidak aktif. Menggunakan fallback SQLite: {DATABASE_URL}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

