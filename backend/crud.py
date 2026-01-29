# backend/crud.py — добавь эти функции в конец файла

def create_referral(session: Session, referrer_id: int, referred_id: int) -> Referral:
    """
    Создаёт запись о реферале (только если её ещё нет).
    """
    # Проверяем, не существует ли уже такая связь
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
    session.commit()
    session.refresh(referral)
    logger.info(f"New referral created: {referrer_id} → {referred_id}")
    return referral


def update_referral_first_lesson(session: Session, referred_id: int) -> bool:
    """
    Отмечает, что реферал завершил первый урок (+15 points рефереру).
    Возвращает True, если обновление прошло успешно.
    """
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
        session.add(referral)
        
        # Начисляем +15 points рефереру
        referrer = get_user(session, referral.referrer_id)
        if referrer:
            referrer.points += 15
            session.add(referrer)

    try:
        session.commit()
        logger.info(f"First lesson completed by {referred_id}, +15 points to referrers")
        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating referral first lesson: {e}")
        return False
