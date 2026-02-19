# backend/database.py

import logging
import os
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session


load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL не задан. Проверь переменные окружения.")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,   # важно для Render
)


def init_db() -> None:
    logger.info("Создание таблиц (если не существуют)...")
    SQLModel.metadata.create_all(engine)
    logger.info("База данных готова")


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
