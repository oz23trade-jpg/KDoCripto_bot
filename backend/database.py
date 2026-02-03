# backend/database.py
"""
Модуль подключения к базе данных через SQLModel + PostgreSQL.
"""

import logging
from typing import Generator

from dotenv import load_dotenv
import os

from sqlmodel import SQLModel, create_engine, Session

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.critical("DATABASE_URL не найден в .env или переменных окружения!")
    raise ValueError("DATABASE_URL не задан. Проверь .env или переменные окружения.")

try:
    engine = create_engine(
        DATABASE_URL,
        echo=False,           # Логи SQL отключены
        future=True,          # Совместимость с SQLAlchemy 2.0+
        pool_pre_ping=True,   # Проверка соединения перед использованием
        pool_size=5,
        max_overflow=10
    )
    logger.info("Подключение к базе данных успешно установлено")
except Exception as e:
    logger.critical(f"Ошибка создания engine: {e}")
    raise


def init_db() -> None:
    """Создаёт все таблицы в базе данных, если их ещё нет."""
    logger.info("Инициализация таблиц...")
    SQLModel.metadata.create_all(engine)
    logger.info("Инициализация таблиц завершена")


def get_session() -> Generator[Session, None, None]:
    """
    Генератор сессии для FastAPI Depends.
    Автоматически закрывает сессию после использования.
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
