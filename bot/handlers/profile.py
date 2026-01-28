from aiogram import Router
from aiogram.types import CallbackQuery
from api.client import api_get_profile
from texts import get_text

router = Router()

@router.callback_query(F.data == "profile")
async def show_profile(cb: CallbackQuery):
    profile = await api_get_profile(cb.from_user.id)
    if not profile:
        await cb.answer("Error loading profile", show_alert=True)
        return

    text = get_text("profile",
                    id=profile["id"],
                    name=profile.get("name", "Unknown"),
                    username=profile.get("username", "none"),
                    level=profile["level"],
                    xp=profile["xp"],
                    points=profile["points"],
                    tickets=profile["tickets"],
                    referrals_count=profile["referrals_count"])

    await cb.message.edit_text(text, reply_markup=cb.message.reply_markup)  # сохраняем меню
    await cb.answer()