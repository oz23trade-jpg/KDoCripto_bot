from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Index


class LotteryDraw(SQLModel, table=True):

    __tablename__ = "lottery_draws"

    id: Optional[int] = Field(default=None, primary_key=True)
    draw_number: int = Field(index=True)

    start_date: datetime = Field(index=True)
    end_date: datetime = Field(index=True)

    status: str = Field(default="active", index=True)

    winner_id: Optional[int] = Field(default=None, foreign_key="users.id")

    prize_description: str
    seed: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)


class LotteryTicket(SQLModel, table=True):

    __tablename__ = "lottery_tickets"
    __table_args__ = (
        Index("ix_ticket_user_draw", "user_id", "draw_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id", index=True)
    draw_id: int = Field(foreign_key="lottery_draws.id", index=True)

    source: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    is_winner: bool = Field(default=False)
