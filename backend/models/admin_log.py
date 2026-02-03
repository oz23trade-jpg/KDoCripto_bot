# backend/models/admin_log.py
from typing import Optional, Dict
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import JSON, Index


class AdminActionLog(SQLModel, table=True):
    """
    Лог действий администраторов.
    Используется для аудита: кто, когда и что сделал.
    """

    __tablename__ = "admin_action_logs"
    __table_args__ = (
        Index("ix_admin_action_log_admin_created", "admin_id", "created_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    admin_id: int = Field(
        index=True,
        nullable=False,
        description="Telegram ID администратора"
    )

    action: str = Field(
        max_length=100,
        nullable=False,
        description="Тип действия: grant_points, revoke_points, start_draw, broadcast и т.д."
    )

    target_id: Optional[int] = Field(
        default=None,
        index=True,
        description="ID цели действия (user_id, draw_id, quiz_id и т.д.)"
    )

    details: Dict = Field(
        default_factory=dict,
        sa_column=JSON,
        description="Дополнительные данные в JSON: {'points': 100, 'reason': 'bug fix'}"
    )

    ip_address: Optional[str] = Field(
        default=None,
        max_length=45,
        description="IP-адрес администратора (если удалось получить)"
    )

    user_agent: Optional[str] = Field(
        default=None,
        description="User-Agent браузера/бота админа"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        nullable=False,
        description="Время выполнения действия"
    )

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self) -> str:
        return f"<AdminActionLog id={self.id} admin={self.admin_id} action={self.action}>"
