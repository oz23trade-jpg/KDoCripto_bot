from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from typing import Optional

import uvicorn
import logging

from database import engine, get_session
import models  # ← один импорт всех моделей через __init__.py
from schemas import UserCreate, UserUpdate, UserOut
from crud import get_user, create_user, update_user, increment_referrals, create_referral

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация базы данных при старте приложения"""
    logger.info("Инициализация базы данных...")
    models.SQLModel.metadata.create_all(engine)
    yield
    logger.info("Остановка приложения...")


app = FastAPI(
    title="K DoCripto Bot API",
    description="Backend API для Telegram-бота K DoCripto",
    version="0.1.0",
    lifespan=lifespan
)

# CORS для будущих WebApp / внешних клиентов
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В проде ограничь: ["https://t.me", "https://web.telegram.org"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Проверка состояния сервиса"""
    return {"status": "healthy", "version": app.version}


@app.post("/user/start", response_model=UserOut)
async def start_user(
    user_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    referrer_id: Optional[int] = None,
    db: Session = Depends(get_session)
):
    """
    Обработка команды /start.
    Создаёт нового пользователя или обновляет существующего.
    Засчитывает реферала только один раз.
    """
    logger.info(f"Start request: user={user_id}, referrer={referrer_id}")

    user = get_user(db, user_id)

    if user:
        update_data = UserUpdate(username=username, name=first_name)
        user = update_user(db, user_id, update_data)
    else:
        user_data = UserCreate(
            id=user_id,
            username=username,
            name=first_name,
            referrer_id=referrer_id if referrer_id != user_id else None
        )
        user = create_user(db, user_data)

        if referrer_id and referrer_id != user_id:
            referrer = get_user(db, referrer_id)
            if referrer:
                increment_referrals(db, referrer_id)
                create_referral(db, referrer_id, user_id)
                logger.info(f"Referral recorded: {referrer_id} → {user_id}")
            else:
                logger.warning(f"Invalid referrer_id: {referrer_id}")

    return UserOut.from_orm(user)


@app.post("/user/language", response_model=UserOut)
async def set_language(
    user_id: int,
    lang: str = Query(..., regex="^(en|ru|fi)$"),
    db: Session = Depends(get_session)
):
    """Смена языка пользователя"""
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.lang == lang:
        logger.info(f"Language already set for user {user_id}: {lang}")
        return UserOut.from_orm(user)

    update_data = UserUpdate(lang=lang)
    updated_user = update_user(db, user_id, update_data)
    logger.info(f"Language updated for user {user_id}: {lang}")

    return UserOut.from_orm(updated_user)


@app.get("/user/{user_id}", response_model=UserOut)
async def get_user_profile(user_id: int, db: Session = Depends(get_session)):
    """Получение профиля пользователя по ID"""
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserOut.from_orm(user)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
