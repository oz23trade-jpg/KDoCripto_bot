# backend/models/payment.py
from typing import Optional, Dict
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import JSON, Index


class Payment(SQLModel, table=True):
    """
    Платёж пользователя через Telegram Stars.
    Хранит информацию о транзакции, наградах и статусе.
    """

    __tablename__ = "payments"
    __table_args__ = (
        Index("ix_payment_user_status", "user_id", "status"),
        Index("ix_payment_created", "created_at"),
        Index("ix_payment_telegram_id", "telegram_payment_id", unique=True),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(
        foreign_key="users.id",
        index=True,
        nullable=False,
        description="ID пользователя, который произвёл платёж"
    )

    telegram_stars_amount: int = Field(
        description="Сумма в Telegram Stars"
    )

    tickets_granted: int = Field(
        default=0,
        description="Количество выданных билетов в лотерею"
    )

    badge_granted: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Бейдж, выданный за поддержку (если есть)"
    )

    tier: str = Field(
        max_length=50,
        description="Уровень поддержки: small / medium / large"
    )

    status: str = Field(
        default="pending",
        index=True,
        description="Статус: pending / completed / failed / refunded"
    )

    telegram_payment_id: Optional[str] = Field(
        default=None,
        unique=True,
        description="Уникальный ID платежа от Telegram"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        description="Время создания записи"
    )

    completed_at: Optional[datetime] = Field(
        default=None,
        description="Время успешного завершения платежа"
    )

    payload: Dict = Field(
        default_factory=dict,
        sa_column=JSON,
        description="Сырые данные от Telegram (pre-checkout, invoice и т.д.)"
    )

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self) -> str:
        return f"<Payment id={self.id} user={self.user_id} tier={self.tier} status={self.status}>"
