from typing import Optional, Dict
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON, Index


class Payment(SQLModel, table=True):

    __tablename__ = "payments"
    __table_args__ = (
        Index("ix_payment_user_status", "user_id", "status"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id", index=True)

    telegram_stars_amount: int
    tickets_granted: int = Field(default=0)
    badge_granted: Optional[str] = None
    tier: str

    status: str = Field(default="pending", index=True)

    telegram_payment_id: Optional[str] = Field(default=None, unique=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    payload: Dict = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=False)
    )

    def __repr__(self):
        return f"<Payment {self.id} user={self.user_id} status={self.status}>"
