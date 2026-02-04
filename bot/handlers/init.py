# bot/texts/__init__.py
"""
Модуль локализации: загрузка текстов и клавиатур из JSON-файлов по языку.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

LANG_DIR = Path(__file__).parent
DEFAULT_LANG = "en"

# Кэш текстов (язык → словарь текстов)
_text_cache: Dict[str, Dict[str, Any]] = {}


def load_texts(lang: str) -> None:
    """
    Загружает тексты и клавиатуры для указанного языка.
    При ошибке или отсутствии файла использует английский.
    """
    global _text_cache
    
    if lang in _text_cache:
        logger.debug(f"Using cached texts for language: {lang}")
        return
    
    file_path = LANG_DIR / f"{lang}.json"
    
    if not file_path.exists():
        logger.warning(f"Localization file not found: {file_path}. Falling back to {DEFAULT_LANG}")
        file_path = LANG_DIR / f"{DEFAULT_LANG}.json"
        if not file_path.exists():
            logger.critical(f"Default localization file missing: {file_path}")
            return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            _text_cache[lang] = json.load(f)
        logger.info(f"Localization loaded successfully: {lang}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        if lang != DEFAULT_LANG:
            load_texts(DEFAULT_LANG)  # только один уровень fallback
    except Exception as e:
        logger.exception(f"Failed to load localization {lang}: {e}")


def get_text(key: str, **kwargs) -> str:
    """
    Получает текст по ключу из раздела "texts".
    Если ключа нет — возвращает сам ключ.
    Поддерживает форматирование: get_text("hello", name="User")
    """
    current_texts = _text_cache.get("current_lang", _text_cache.get(DEFAULT_LANG, {}))
    text = current_texts.get("texts", {}).get(key, key)
    
    try:
        return text.format(**kwargs) if kwargs else text
    except KeyError as e:
        logger.warning(f"Missing placeholder in text '{key}': {e}")
        return text


def get_keyboard(key: str) -> Dict:
    """
    Получает клавиатуру по ключу из раздела "keyboards".
    Возвращает пустой словарь, если клавиатура не найдена.
    """
    current_texts = _text_cache.get("current_lang", _text_cache.get(DEFAULT_LANG, {}))
    kb = current_texts.get("keyboards", {}).get(key, {})
    if not kb:
        logger.warning(f"Keyboard '{key}' not found")
    return kb


def set_current_lang(lang: str) -> None:
    """
    Устанавливает текущий язык для последующих вызовов get_text / get_keyboard.
    """
    if lang in _text_cache:
        _text_cache["current_lang"] = _text_cache[lang]
        logger.debug(f"Current language set to: {lang}")
    else:
        logger.warning(f"Language {lang} not loaded. Loading now.")
        load_texts(lang)
        if lang in _text_cache:
            _text_cache["current_lang"] = _text_cache[lang]
