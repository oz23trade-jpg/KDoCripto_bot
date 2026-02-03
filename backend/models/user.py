# backend/models/user.py
from typing import Optional, List, Dict
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import JSON, Index


class User(SQLModel, table=True):
    """
    Основная таблица пользователей (Telegram ID как PK).
    Хранит прогресс, рефералы, баллы, билеты и настройки.
    """

    __tablename__ = "users"
    __table_args__ = (
        Index("ix_user_referrer", "referrer_id"),
        Index("ix_user_joined", "joined_at"),
        Index("ix_user_username", "username"),
    )

    id: int = Field(primary_key=True, description="Telegram ID пользователя")

    lang: str = Field(
        default="en",
        max_length=5,
        description="Язык интерфейса: en / ru / fi"
    )

    username: Optional[str] = Field(
        default=None,
        max_length=255,
        index=True,
        description="Telegram username (без @)"
    )

    name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Имя/никнейм из Telegram"
    )

    joined_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        description="Дата регистрации"
    )

    points: int = Field(
        default=0,
        description="Общие баллы (points)"
    )

    xp: int = Field(
        default=0,
        description="Опыт (XP) для уровня"
    )

    level: int = Field(
        default=1,
        description="Уровень пользователя"
    )

    referrer_id: Optional[int] = Field(
        default=None,
        foreign_key="users.id",
        index=True,
        description="Кто пригласил этого пользователя"
    )

    referrals_count: int = Field(
        default=0,
        description="Количество прямых рефералов"
    )

    tickets: int = Field(
        default=0,
        description="Билеты в лотерею"
    )

    badges: List[Dict] = Field(
        default_factory=list,
        sa_column=JSON,
        description="Список бейджей: [{'name': 'Supporter', 'earned_at': '...'}, ...]"
    )

    settings: Dict = Field(
        default_factory=dict,
        sa_column=JSON,
        description="Настройки пользователя в JSON"
    )

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self) -> str:
        return f"<User id={self.id} username=@{self.username} level={self.level} points={self.points}>"
