# backend/crud.py
"""
CRUD-операции для модели User и Referral.
Все функции работают с сессией SQLModel и включают логирование + обработку ошибок.
"""

import logging
from typing import Optional

from sqlmodel import Session, select

from models import User, Referral
from schemas import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


# ── User ────────────────────────────────────────────────────────────────

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
    Автоматически устанавливает дефолтные значения.
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
    Увеличивает счётчик referrals_count у реферера.
    Возвращает True при успехе, False — если реферер не найден.
    """
    referrer = session.get(User, referrer_id)
    if not referrer:
        logger.warning(f"Referrer {referrer_id} not found, referral not counted")
        return False

    referrer.referrals_count += 1
    session.add(referrer)

    try:
        session.commit()
        logger.info(f"Referrals count incremented for {referrer_id} → {referrer.referrals_count}")
        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Error incrementing referrals for {referrer_id}: {e}")
        return False


# ── Referral ─────────────────────────────────────────────────────────────

def create_referral(session: Session, referrer_id: int, referred_id: int) -> Referral:
    """
    Создаёт запись о реферале (только если её ещё нет).
    Возвращает существующую или новую запись.
    """
    # Проверяем существование
    existing = session.exec(
        select(Referral).where(
            Referral.referrer_id == referrer_id,
            Referral.referred_id == referred_id
        )
    ).first()

    if existing:
        logger.info(f"Referral {referrer_id} → {referred_id} already exists")
        return existing

    referral = Referral(referrer_id=referrer_id, referred_id=referred_id)
    session.add(referral)

    try:
        session.commit()
        session.refresh(referral)
        logger.info(f"New referral created: {referrer_id} → {referred_id}")
        return referral
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating referral {referrer_id} → {referred_id}: {e}")
        raise


def update_referral_first_lesson(session: Session, referred_id: int) -> bool:
    """
    Отмечает, что реферал завершил первый урок.
    Начисляет +15 points каждому рефереру (если ещё не начислено).
    Возвращает True, если было хотя бы одно обновление.
    """
    referrals = session.exec(
        select(Referral).where(
            Referral.referred_id == referred_id,
            Referral.first_lesson_completed == False
        )
    ).all()

    if not referrals:
        logger.info(f"No pending first-lesson referrals for user {referred_id}")
        return False

    updated_count = 0

    for referral in referrals:
        referral.first_lesson_completed = True
        session.add(referral)

        # Начисляем +15 points рефереру
        referrer = get_user(session, referral.referrer_id)
        if referrer:
            referrer.points += 15
            session.add(referrer)
            updated_count += 1

    try:
        session.commit()
        logger.info(
            f"First lesson completed by {referred_id}, "
            f"+15 points to {updated_count} referrer(s)"
        )
        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating referral first lesson for {referred_id}: {e}")
        return False
