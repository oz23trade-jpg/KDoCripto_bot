from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
from sqlalchemy import JSON

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)                   # telegram_id
    lang: str = Field(default="en", max_length=5)
    username: Optional[str] = Field(default=None, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    points: int = Field(default=0)
    xp: int = Field(default=0)
    level: int = Field(default=1)
    referrer_id: Optional[int] = Field(default=None, foreign_key="users.id")
    referrals_count: int = Field(default=0)
    tickets: int = Field(default=0)
    badges: List[dict] = Field(default_factory=list, sa_column=JSON)
    settings: dict = Field(default_factory=dict, sa_column=JSON)

    class Config:
        arbitrary_types_allowed = True