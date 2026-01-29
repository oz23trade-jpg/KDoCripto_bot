# bot/handlers/referral.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from texts import get_text
from keyboards.inline import get_main_menu

router = Router()

# ← ОБЯЗАТЕЛЬНО замени на реальный username твоего бота (без @)
BOT_USERNAME = "KDoCripto_bot"  


def get_referral_kb(user_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для реферального меню"""
    ref_link = f"https://t.me/{KDoCripto_bot}?start=ref_{user_id}"
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📤 Поделиться ссылкой",
                switch_inline_query_current_chat=(
                    f"Присоединяйся к K DoCripto! Учи крипту, зарабатывай очки и билеты в лотерею 🚀\n"
                    f"Твоя ссылка: {ref_link}"
                )
            )
        ],
        [
            InlineKeyboardButton(text="📋 Скопировать ссылку", callback_data="ref_copy")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu")
        ]
    ])


@router.callback_query(F.data == "menu_referral")
async def show_referral_menu(cb: CallbackQuery):
    """Показывает реферальное меню с персональной ссылкой"""
    user_id = cb.from_user.id
    ref_link = f"https://t.me/{KDoCripto_bot}?start=ref_{user_id}"
    
    text = get_text("referral_menu", ref_link=ref_link)
    
    if not text:
        text = "Ошибка загрузки текста меню. Попробуй позже."
    
    await cb.message.edit_text(text, reply_markup=get_referral_kb(user_id))
    await cb.answer()


@router.callback_query(F.data == "ref_copy")
async def copy_referral_link(cb: CallbackQuery):
    """Показывает алерт с реферальной ссылкой для копирования"""
    user_id = cb.from_user.id
    ref_link = f"https://t.me/{KDoCripto_bot}?start=ref_{user_id}"
    
    await cb.answer(
        text=(
            f"📋 Твоя реферальная ссылка:\n\n"
            f"{https://t.me/{KDoCripto_bot}?start=ref_{user_id}}\n\n"
            "Зажми текст и выбери «Скопировать»"
        ),
        show_alert=True
    )


@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(cb: CallbackQuery):
    """Возврат в главное меню"""
    await cb.message.edit_text(
        get_text("main_menu"),
        reply_markup=get_main_menu()
    )
    await cb.answer()
