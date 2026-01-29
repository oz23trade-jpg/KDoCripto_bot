# backend/models/referral.py
from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field


class Referral(SQLModel, table=True):
    """
    Таблица рефералов: кто кого пригласил, статус и награды.
    """

    __tablename__ = "referrals"

    id: Optional[int] = Field(default=None, primary_key=True)

    referrer_id: int = Field(
        foreign_key="users.id",
        index=True,
        description="Кто пригласил (referrer)"
    )

    referred_id: int = Field(
        foreign_key="users.id",
        index=True,
        description="Кого пригласили (новый пользователь)"
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Дополнительные награды и статус
    first_lesson_completed: bool = Field(default=False)  # +15 points за первый урок реферала
    active: bool = Field(default=True)                   # можно деактивировать при бане/фроде

    class Config:
        arbitrary_types_allowed = True
