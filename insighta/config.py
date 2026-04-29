# insighta/config.py
from pathlib import Path
import json

CONFIG_DIR = Path.home() / ".insighta"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"

API_BASE_URL = "http://127.0.0.1:8000"


def ensure_config():
    CONFIG_DIR.mkdir(exist_ok=True)


def save_credentials(data: dict):
    ensure_config()

    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(data, f)


def load_credentials():
    if not CREDENTIALS_FILE.exists():
        return None

    with open(CREDENTIALS_FILE) as f:
        return json.load(f)


def clear_credentials():
    if CREDENTIALS_FILE.exists():
        CREDENTIALS_FILE.unlink()
        