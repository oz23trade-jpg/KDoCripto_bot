# backend/main.py

import logging
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from database import engine, get_session
import models
from schemas import UserCreate, UserUpdate, UserOut
from crud import get_user, create_user, update_user, increment_referrals, create_referral


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения...")
    models.SQLModel.metadata.create_all(engine)
    yield
    logger.info("Остановка приложения...")


app = FastAPI(
    title="K DoCripto Bot API",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # в проде ограничить
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


# ───────────────── USER START ─────────────────

@app.post("/user/start", response_model=UserOut)
async def start_user(
    data: UserCreate,
    db: Session = Depends(get_session)
):
    user = get_user(db, data.id)

    if user:
        user = update_user(
            db,
            data.id,
            UserUpdate(username=data.username, name=data.name)
        )
    else:
        user = create_user(db, data)

        if data.referrer_id and data.referrer_id != data.id:
            referrer = get_user(db, data.referrer_id)
            if referrer:
                increment_referrals(db, data.referrer_id)
                create_referral(db, data.referrer_id, data.id)

    return UserOut.model_validate(user)


# ───────────────── LANGUAGE ─────────────────

@app.post("/user/language", response_model=UserOut)
async def set_language(
    user_id: int,
    lang: Literal["en", "ru", "fi"],
    db: Session = Depends(get_session)
):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user = update_user(db, user_id, UserUpdate(lang=lang))
    return UserOut.model_validate(user)


# ───────────────── PROFILE ─────────────────

@app.get("/user/{user_id}", response_model=UserOut)
async def get_profile(user_id: int, db: Session = Depends(get_session)):
    user = get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserOut.model_validate(user)
