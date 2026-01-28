from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import JSON

class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    telegram_stars_amount: int                  # в звёздах
    tickets_granted: int
    badge_granted: Optional[str] = None
    tier: str                                   # small / medium / large
    status: str = Field(default="pending")      # pending / completed / failed
    telegram_payment_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    payload: dict = Field(default_factory=dict, sa_column=JSON)  # данные от Telegram