import json
import os
from config import CACHE_FILE


def load_cache() -> dict:
    """Carrega o cache de gêneros do disco."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache: dict):
    """Salva o cache de gêneros no disco."""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)