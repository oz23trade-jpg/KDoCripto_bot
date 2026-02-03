# bot/texts/__init__.py
"""
Модуль локализации: загрузка текстов и клавиатур по языку из JSON-файлов.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

LANG_DIR = Path(__file__).parent
DEFAULT_LANG = "en"

# Глобальный кэш текстов (загружается один раз на язык)
_texts: Dict[str, Any] = {}


def load_texts(lang: str) -> None:
    """
    Загружает тексты и клавиатуры для указанного языка.
    При ошибке fallback на английский.
    """
    global _texts
    
    # Очищаем кэш перед загрузкой нового языка
    _texts.clear()
    
    file_path = LANG_DIR / f"{lang}.json"
    
    if not file_path.exists():
        logger.warning(f"Файл локализации не найден: {file_path}. Используем {DEFAULT_LANG}")
        file_path = LANG_DIR / f"{DEFAULT_LANG}.json"
        if not file_path.exists():
            logger.error(f"Файл по умолчанию {DEFAULT_LANG}.json тоже не найден!")
            return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            _texts = json.load(f)
        logger.info(f"Локализация загружена: {lang}")
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON в {file_path}: {e}")
        # Fallback на en
        load_texts(DEFAULT_LANG)
    except Exception as e:
        logger.exception(f"Неизвестная ошибка при загрузке {lang}: {e}")


def get_text(key: str, **kwargs) -> str:
    """
    Получает текст по ключу из раздела "texts".
    Поддерживает форматирование: get_text("hello", name="User") → "Привет, User!"
    Если ключа нет — возвращает сам ключ.
    """
    text = _texts.get("texts", {}).get(key, key)
    try:
        return text.format(**kwargs) if kwargs else text
    except KeyError as e:
        logger.warning(f"Отсутствует плейсхолдер в тексте '{key}': {e}")
        return text


def get_keyboard(key: str) -> Dict:
    """
    Получает клавиатуру по ключу из раздела "keyboards".
    Возвращает пустой словарь, если клавиатура не найдена.
    """
    kb = _texts.get("keyboards", {}).get(key, {})
    if not kb:
        logger.warning(f"Клавиатура '{key}' не найдена")
    return kb
