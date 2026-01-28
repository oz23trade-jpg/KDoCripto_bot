from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import JSON

class LotteryDraw(SQLModel, table=True):
    __tablename__ = "lottery_draws"

    id: Optional[int] = Field(default=None, primary_key=True)
    draw_number: int                            # 1,2,3,...
    start_date: datetime
    end_date: datetime
    status: str = Field(default="active")       # active / finished / cancelled
    winner_id: Optional[int] = Field(default=None, foreign_key="users.id")
    prize_description: str
    seed: Optional[str] = None                  # для воспроизводимого рандома
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LotteryTicket(SQLModel, table=True):
    __tablename__ = "lottery_tickets"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    draw_id: int = Field(foreign_key="lottery_draws.id")
    source: str                                 # quiz / referral / stars / manual
    created_at: datetime = Field(default_factory=datetime.utcnow)