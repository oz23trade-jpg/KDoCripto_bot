# backend/models/lottery.py
from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Index


class LotteryDraw(SQLModel, table=True):
    """
    Розыгрыш лотереи (один draw = один розыгрыш).
    """

    __tablename__ = "lottery_draws"
    __table_args__ = (
        Index("ix_lottery_draw_status", "status"),
        Index("ix_lottery_draw_dates", "start_date", "end_date"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    draw_number: int = Field(index=True, description="Порядковый номер розыгрыша (1, 2, 3...)")
    start_date: datetime = Field(index=True)
    end_date: datetime = Field(index=True)
    status: str = Field(default="active", index=True)  # active / finished / cancelled
    winner_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    prize_description: str
    seed: Optional[str] = Field(default=None, description="Сид для воспроизводимого рандома")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LotteryTicket(SQLModel, table=True):
    """
    Билет пользователя в конкретном розыгрыше.
    """

    __tablename__ = "lottery_tickets"
    __table_args__ = (
        Index("ix_lottery_ticket_user_draw", "user_id", "draw_id"),
        Index("ix_lottery_ticket_draw", "draw_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    draw_id: int = Field(foreign_key="lottery_draws.id", index=True)
    source: str = Field(description="Источник билета: quiz / referral / stars / manual / admin")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_winner: bool = Field(default=False, description="Выиграл ли этот билет (после розыгрыша)")
