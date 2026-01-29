# backend/crud.py
"""
CRUD-операции для модели User.
Все функции работают с сессией SQLModel.
"""

import logging
from typing import Optional

from sqlmodel import Session, select
from models import User
from schemas import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


def get_user(session: Session, user_id: int) -> Optional[User]:
    """
    Получает пользователя по Telegram ID.
    Возвращает None, если пользователя нет.
    """
    user = session.get(User, user_id)
    if user:
        logger.debug(f"User {user_id} found")
    else:
        logger.debug(f"User {user_id} not found")
    return user


def create_user(session: Session, user_data: UserCreate) -> User:
    """
    Создаёт нового пользователя.
    Автоматически устанавливает joined_at и другие дефолтные значения.
    """
    try:
        user = User(**user_data.model_dump())
        session.add(user)
        session.commit()
        session.refresh(user)
        logger.info(f"User {user.id} created successfully")
        return user
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating user {user_data.id}: {e}")
        raise


def update_user(session: Session, user_id: int, update_data: UserUpdate) -> Optional[User]:
    """
    Обновляет данные пользователя (только переданные поля).
    Возвращает обновлённого пользователя или None, если не найден.
    """
    user = session.get(User, user_id)
    if not user:
        logger.warning(f"User {user_id} not found for update")
        return None

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(user, key, value)

    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        logger.info(f"User {user_id} updated: {update_dict}")
        return user
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating user {user_id}: {e}")
        raise


def increment_referrals(session: Session, referrer_id: int) -> bool:
    """
    Увеличивает счётчик referrals_count у пользователя-реферера.
    Возвращает True, если счётчик успешно увеличен, False — если реферер не найден.
    """
    referrer = session.get(User, referrer_id)
    if not referrer:
        logger.warning(f"Referrer {referrer_id} not found, referral not counted")
        return False

    referrer.referrals_count += 1
    session.add(referrer)
    
    try:
        session.commit()
        logger.info(f"Referrals count incremented for user {referrer_id} → {referrer.referrals_count}")
        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Error incrementing referrals for {referrer_id}: {e}")
        return False
