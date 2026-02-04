# bot/config.py (или в bot/main.py)
import logging
from dotenv import load_dotenv
import os
from typing import Set

load_dotenv()

logger = logging.getLogger(__name__)

# ── Обязательные переменные ────────────────────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.critical("BOT_TOKEN не найден в .env или переменных окружения!")
    raise ValueError("BOT_TOKEN обязателен. Укажи его в .env")

# ── Опциональные переменные ────────────────────────────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
logger.info(f"API_BASE_URL: {API_BASE_URL}")

# ── ADMIN_IDS ──────────────────────────────────────────────────────────────
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "").strip()
ADMIN_IDS: Set[int] = set()

if ADMIN_IDS_STR:
    try:
        ADMIN_IDS = set(int(x.strip()) for x in ADMIN_IDS_STR.split(",") if x.strip())
        logger.info(f"Загружены ADMIN_IDS: {ADMIN_IDS}")
    except ValueError as e:
        logger.error(f"Ошибка парсинга ADMIN_IDS: {e}. Используется пустой набор.")
else:
    logger.warning("ADMIN_IDS не задан в .env — админ-функции будут недоступны")

# ── Дополнительные настройки (пример) ──────────────────────────────────────
# DEBUG = os.getenv("DEBUG", "false").lower() == "true"
