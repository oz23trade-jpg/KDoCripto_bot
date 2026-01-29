from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import Optional
import models  # ← это импортирует все модели через __init__.py
import uvicorn

from database import engine, get_session
import models  # ← Импорт всех моделей через models/__init__.py
from schemas import UserCreate, UserUpdate, UserOut
from crud import get_user, create_user, update_user, increment_referrals
# from models.referral import Referral  # раскомментируй, когда добавишь таблицу Referral

app = FastAPI(
    title="K DoCripto Bot API",
    description="Backend API для Telegram-бота K DoCripto",
    version="0.1.0",
    # lifespan=lifespan,  # ← включаем ниже
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация базы данных при старте приложения"""
    # Создаём все таблицы, если их ещё нет
    models.SQLModel.metadata.create_all(engine)
    yield
    # Здесь можно добавить cleanup, если нужно


app.router.lifespan_context = lifespan


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
    user = get_user(db, user_id)

    if user:
        # Обновляем только если данные изменились
        update_data = UserUpdate(username=username, name=first_name)
        user = update_user(db, user_id, update_data)
    else:
        # Новый пользователь
        user_data = UserCreate(
            id=user_id,
            username=username,
            name=first_name,
            referrer_id=referrer_id if referrer_id != user_id else None  # защита от self-referral
        )
        user = create_user(db, user_data)

        # Засчитываем реферала только если это новый пользователь и referrer существует
        if referrer_id and referrer_id != user_id:
            # Проверяем, не был ли уже засчитан этот реферал (если есть таблица Referral)
            # Пока просто увеличиваем счётчик — позже добавим проверку
            increment_referrals(db, referrer_id)

    return UserOut.from_orm(user)


@app.post("/user/language", response_model=dict)
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
        return {"status": "already_set", "lang": lang}

    update_data = UserUpdate(lang=lang)
    updated_user = update_user(db, user_id, update_data)

    return {"status": "language_updated", "lang": updated_user.lang}


@app.get("/user/{user_id}", response_model=UserOut)
async def get_user_profile(user_id: int, db: Session = Depends(get_session)):
    """Получение профиля пользователя по ID"""
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserOut.from_orm(user)


# Опционально: CORS (раскомментируй, если будет WebApp или внешние клиенты)
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # или конкретные домены
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    
