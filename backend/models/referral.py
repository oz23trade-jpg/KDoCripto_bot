# backend/models/referral.py
from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Index


class Referral(SQLModel, table=True):
    """
    Таблица рефералов: кто кого пригласил, статус и награды.
    """

    __tablename__ = "referrals"
    __table_args__ = (
        Index("ix_referral_referrer_referred", "referrer_id", "referred_id", unique=True),
        Index("ix_referral_referrer", "referrer_id"),
        Index("ix_referral_referred", "referred_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    referrer_id: int = Field(
        foreign_key="users.id",
        index=True,
        nullable=False,
        description="Кто пригласил (реферер)"
    )

    referred_id: int = Field(
        foreign_key="users.id",
        index=True,
        nullable=False,
        description="Кого пригласили (новый пользователь)"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        description="Время создания связи"
    )

    first_lesson_completed: bool = Field(
        default=False,
        index=True,
        description="+15 points рефереру за первый урок приглашённого"
    )

    active: bool = Field(
        default=True,
        index=True,
        description="Связь активна (можно деактивировать при бане/фроде)"
    )

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self) -> str:
        return f"<Referral referrer={self.referrer_id} → referred={self.referred_id} active={self.active}>"
