from typing import Optional, Dict
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON, Index


class AdminActionLog(SQLModel, table=True):

    __tablename__ = "admin_action_logs"
    __table_args__ = (
        Index("ix_admin_created", "admin_id", "created_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    admin_id: int = Field(index=True)
    action: str = Field(max_length=100)

    target_id: Optional[int] = Field(default=None, index=True)

    details: Dict = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=False)
    )

    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<AdminLog {self.admin_id} {self.action}>"
