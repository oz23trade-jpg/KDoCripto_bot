# bot/config.py

import logging
import os
from typing import Set
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class Settings:
    # ── Обязательные ─────────────────────────────
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

    if not BOT_TOKEN:
        logger.critical("BOT_TOKEN не найден в .env или переменных окружения!")
        raise ValueError("BOT_TOKEN обязателен")

    # ── Опциональные ─────────────────────────────
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")

    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # ── ADMIN_IDS ────────────────────────────────
    ADMIN_IDS: Set[int] = set()

    admin_ids_raw = os.getenv("ADMIN_IDS", "").strip()
    if admin_ids_raw:
        try:
            ADMIN_IDS = {
                int(x.strip()) for x in admin_ids_raw.split(",") if x.strip()
            }
        except ValueError as e:
            logger.error(f"Ошибка парсинга ADMIN_IDS: {e}")

    # ── Дополнительно ────────────────────────────
    DROP_PENDING_UPDATES: bool = True


settings = Settings()

logger.info(f"API_BASE_URL: {settings.API_BASE_URL}")
logger.info(f"DEBUG: {settings.DEBUG}")
logger.info(f"ADMIN_IDS: {settings.ADMIN_IDS}")
