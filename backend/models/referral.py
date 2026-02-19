from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Index


class Referral(SQLModel, table=True):

    __tablename__ = "referrals"
    __table_args__ = (
        Index("ix_referral_unique", "referrer_id", "referred_id", unique=True),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    referrer_id: int = Field(foreign_key="users.id", index=True)
    referred_id: int = Field(foreign_key="users.id", index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    first_lesson_completed: bool = Field(default=False, index=True)
    active: bool = Field(default=True, index=True)

    def __repr__(self):
        return f"<Referral {self.referrer_id}->{self.referred_id}>"
