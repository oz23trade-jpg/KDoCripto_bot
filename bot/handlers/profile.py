# bot/handlers/profile.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from api.client import api_get_profile
from texts import get_text
import logging

router = Router()

logger = logging.getLogger(__name__)


@router.callback_query(F.data == "profile")
async def show_profile(cb: CallbackQuery):
    """Показывает профиль пользователя"""
    user_id = cb.from_user.id
    logger.info(f"Profile requested by user {user_id}")

    try:
        profile = await api_get_profile(user_id)
        if not profile:
            await cb.answer("Ошибка загрузки профиля", show_alert=True)
            return

        # Безопасное получение значений с дефолтами
        text = get_text(
            "profile",
            id=profile.get("id", user_id),
            name=profile.get("name", "Не указано"),
            username=profile.get("username", "нет"),
            level=profile.get("level", 1),
            xp=profile.get("xp", 0),
            points=profile.get("points", 0),
            tickets=profile.get("tickets", 0),
            referrals_count=profile.get("referrals_count", 0)
        )

        # Если текст не найден — fallback
        if text == "profile":
            text = (
                f"👤 Профиль\n\n"
                f"🆔 ID: {user_id}\n"
                f"Имя: {profile.get('name', 'Не указано')}\n"
                f"@{profile.get('username', 'нет')}\n\n"
                f"Уровень: {profile.get('level', 1)} (XP: {profile.get('xp', 0)})\n"
                f"Баллы: {profile.get('points', 0)}\n"
                f"Билеты: {profile.get('tickets', 0)}\n"
                f"Рефералы: {profile.get('referrals_count', 0)}"
            )

        await cb.message.edit_text(text, reply_markup=cb.message.reply_markup)
        await cb.answer()

    except Exception as e:
        logger.exception(f"Error showing profile for user {user_id}: {e}")
        await cb.answer("Не удалось загрузить профиль. Попробуй позже", show_alert=True)
