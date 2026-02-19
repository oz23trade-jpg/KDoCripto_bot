from typing import Optional, List, Dict
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON, Index


class User(SQLModel, table=True):

    __tablename__ = "users"
    __table_args__ = (
        Index("ix_user_referrer", "referrer_id"),
        Index("ix_user_joined", "joined_at"),
        Index("ix_user_username", "username"),
    )

    id: int = Field(primary_key=True)

    lang: str = Field(default="en", max_length=5)

    username: Optional[str] = Field(default=None, max_length=255, index=True)
    name: Optional[str] = Field(default=None, max_length=255)

    joined_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    points: int = Field(default=0)
    xp: int = Field(default=0)
    level: int = Field(default=1)

    referrer_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    referrals_count: int = Field(default=0)

    tickets: int = Field(default=0)

    badges: List[Dict] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False)
    )

    settings: Dict = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=False)
    )

    def recalculate_level(self):
        self.level = self.xp // 100 + 1

    def __repr__(self) -> str:
        return f"<User {self.id} lvl={self.level} pts={self.points}>"
