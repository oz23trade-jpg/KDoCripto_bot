# bot/handlers/support.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from texts import get_text
from keyboards.inline import get_main_menu, get_support_tiers_kb

router = Router()


@router.callback_query(F.data == "menu_support")
async def show_support_menu(cb: CallbackQuery):
    """
    Показывает меню поддержки проекта (покупка Stars).
    """
    text = get_text("support_menu")
    
    await cb.message.edit_text(text, reply_markup=get_support_tiers_kb())
    await cb.answer()


@router.callback_query(F.data.startswith("support_buy:"))
async def buy_support_tier(cb: CallbackQuery):
    """
    Обработка покупки одного из тиров (small / medium / large).
    Здесь начинается Telegram Stars payment flow.
    """
    tier = cb.data.split(":")[1]  # "support_buy:small" → "small"
    
    # Маппинг тиров на суммы и награды (можно вынести в конфиг)
    tiers = {
        "small": {"stars": 100, "tickets": 5, "badge": None, "text": "Маленькая поддержка ☕"},
        "medium": {"stars": 500, "tickets": 30, "badge": "Supporter", "text": "Средняя поддержка 🔥"},
        "large": {"stars": 1000, "tickets": 100, "badge": "Big Supporter", "text": "Большая поддержка 🚀"},
    }
    
    if tier not in tiers:
        await cb.answer("Неверный тир поддержки", show_alert=True)
        return
    
    config = tiers[tier]
    
    # Текст для подтверждения покупки
    text = (
        f"{config['text']}\n\n"
        f"Стоимость: {config['stars']} Telegram Stars\n"
        f"Ты получишь:\n"
        f"🎟 +{config['tickets']} билетов в лотерею\n"
        f"{f'🏅 Бейдж: {config['badge']}' if config['badge'] else ''}\n\n"
        "Подтверди покупку или вернись назад."
    )
    
    # Кнопки подтверждения (в будущем — вызов payment API)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить покупку", callback_data=f"confirm_buy:{tier}")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_support")]
    ])
    
    await cb.message.edit_text(text, reply_markup=kb)
    await cb.answer()


@router.callback_query(F.data.startswith("confirm_buy:"))
async def confirm_buy(cb: CallbackQuery):
    """
    Подтверждение покупки Stars.
    В реальном проекте здесь вызывается Telegram Payment API.
    Пока — имитация успешной оплаты.
    """
    tier = cb.data.split(":")[1]
    
    # Имитация успешной оплаты (в будущем — реальный вызов sendInvoice / preCheckout)
    text = get_text("support_thanks", tickets=5, badge="Supporter")  # подставь реальные значения
    
    await cb.message.edit_text(text, reply_markup=get_main_menu())
    await cb.answer("Спасибо за поддержку! 🎉\nТы помог проекту расти!", show_alert=True)
