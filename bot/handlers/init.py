import json
import os
from pathlib import Path

LANG_DIR = Path(__file__).parent
DEFAULT_LANG = "en"

texts = {}

def load_texts(lang: str):
    global texts
    file = LANG_DIR / f"{lang}.json"
    if file.exists():
        with open(file, "r", encoding="utf-8") as f:
            texts = json.load(f)
    else:
        load_texts(DEFAULT_LANG)

def get_text(key: str, **kwargs):
    text = texts.get("texts", {}).get(key, key)
    return text.format(**kwargs) if kwargs else text

def get_keyboard(key: str):
    return texts.get("keyboards", {}).get(key, {})