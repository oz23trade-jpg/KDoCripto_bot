# bot/handlers/support.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from texts import get_text
from keyboards.inline import get_main_menu, get_support_tiers_kb
import logging

router = Router()

logger = logging.getLogger(__name__)

# Конфиг тиров (можно вынести в отдельный config.py позже)
TIERS = {
    "small": {"stars": 100, "tickets": 5, "badge": None, "name": "Маленькая поддержка ☕"},
    "medium": {"stars": 500, "tickets": 30, "badge": "Supporter", "name": "Средняя поддержка 🔥"},
    "large": {"stars": 1000, "tickets": 100, "badge": "Big Supporter", "name": "Большая поддержка 🚀"},
}


@router.callback_query(F.data == "menu_support")
async def show_support_menu(cb: CallbackQuery):
    """
    Показывает меню поддержки проекта (покупка Stars).
    """
    text = get_text("support_menu")
    if not text:
        text = "Меню поддержки временно недоступно. Попробуй позже."
    
    await cb.message.edit_text(text, reply_markup=get_support_tiers_kb())
    await cb.answer()


@router.callback_query(F.data.startswith("support_buy:"))
async def buy_support_tier(cb: CallbackQuery):
    """
    Обработка выбора тира поддержки.
    Показывает подтверждение покупки.
    """
    tier = cb.data.split(":")[1]  # support_buy:small → small
    
    if tier not in TIERS:
        logger.warning(f"Invalid support tier: {tier} from user {cb.from_user.id}")
        await cb.answer("Неверный уровень поддержки", show_alert=True)
        return
    
    config = TIERS[tier]
    
    text = (
        f"{config['name']}\n\n"
        f"Стоимость: {config['stars']} Telegram Stars\n"
        f"Ты получишь:\n"
        f"🎟 +{config['tickets']} билетов в лотерею\n"
        f"{f'🏅 Бейдж: {config['badge']}' if config['badge'] else ''}\n\n"
        "Нажми «Подтвердить», чтобы продолжить."
    )
    
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
    Пока — имитация успешной оплаты.
    В будущем здесь будет Telegram Payment API (sendInvoice).
    """
    tier = cb.data.split(":")[1]
    
    if tier not in TIERS:
        await cb.answer("Ошибка обработки", show_alert=True)
        return
    
    config = TIERS[tier]
    
    # Имитация успешной оплаты
    text = get_text(
        "support_thanks",
        tickets=config["tickets"],
        badge=config["badge"] or "Нет бейджа"
    )
    
    if not text:
        text = (
            f"Спасибо за поддержку уровня {tier.upper()}!\n"
            f"Ты получил {config['tickets']} билетов и {config['badge'] or 'ничего'} 🎉"
        )
    
    await cb.message.edit_text(text, reply_markup=get_main_menu())
    await cb.answer(f"Спасибо за поддержку! 🎉\nУровень: {tier}", show_alert=True)
    
    logger.info(f"Imitated support payment: user={cb.from_user.id}, tier={tier}")
