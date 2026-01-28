from sqlmodel import Session, select
from models import User
from schemas import UserCreate, UserUpdate

def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)

def create_user(session: Session, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def update_user(session: Session, user_id: int, update_data: UserUpdate) -> User | None:
    user = session.get(User, user_id)
    if not user:
        return None
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def increment_referrals(session: Session, referrer_id: int):
    user = session.get(User, referrer_id)
    if user:
        user.referrals_count += 1
        session.add(user)
        session.commit()