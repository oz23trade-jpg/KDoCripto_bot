# backend/crud.py

import logging
from typing import Optional, List

from sqlmodel import Session, select

from models import User, Referral
from schemas import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


# ───────────────── USER ─────────────────

def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)


def create_user(session: Session, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump())

    session.add(user)
    session.commit()
    session.refresh(user)

    logger.info(f"User created: {user.id}")
    return user


def update_user(session: Session, user_id: int, update_data: UserUpdate) -> Optional[User]:
    user = session.get(User, user_id)
    if not user:
        return None

    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)

    logger.info(f"User updated: {user_id}")
    return user


def increment_referrals(session: Session, referrer_id: int) -> bool:
    referrer = session.get(User, referrer_id)
    if not referrer:
        return False

    referrer.referrals_count += 1
    session.add(referrer)
    session.commit()

    return True


# ───────────────── REFERRALS ─────────────────

def create_referral(session: Session, referrer_id: int, referred_id: int) -> Referral:
    existing = session.exec(
        select(Referral).where(
            Referral.referrer_id == referrer_id,
            Referral.referred_id == referred_id
        )
    ).first()

    if existing:
        return existing

    referral = Referral(referrer_id=referrer_id, referred_id=referred_id)

    session.add(referral)
    session.commit()
    session.refresh(referral)

    return referral


def update_referral_first_lesson(session: Session, referred_id: int) -> bool:
    referrals = session.exec(
        select(Referral).where(
            Referral.referred_id == referred_id,
            Referral.first_lesson_completed == False
        )
    ).all()

    if not referrals:
        return False

    for referral in referrals:
        referral.first_lesson_completed = True

        referrer = session.get(User, referral.referrer_id)
        if referrer:
            referrer.points += 15
            session.add(referrer)

        session.add(referral)

    session.commit()
    return True


def get_referrals(session: Session, user_id: int) -> List[Referral]:
    return session.exec(
        select(Referral).where(Referral.referrer_id == user_id)
    ).all()
