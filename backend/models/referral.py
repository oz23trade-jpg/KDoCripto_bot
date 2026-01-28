from sqlmodel import SQLModel, Field
from datetime import datetime

class Referral(SQLModel, table=True):
    __tablename__ = "referrals"

    id: Optional[int] = Field(default=None, primary_key=True)
    referrer_id: int = Field(foreign_key="users.id")
    referred_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    first_lesson_completed: bool = Field(default=False)
    active: bool = Field(default=True)