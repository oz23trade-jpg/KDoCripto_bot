# bot/handlers/quiz.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from texts import get_text
from keyboards.inline import get_main_menu, get_quiz_options_kb
import logging

router = Router()

logger = logging.getLogger(__name__)


@router.callback_query(F.data == "menu_quiz")
async def show_quiz_menu(cb: CallbackQuery):
    """Показывает меню квиза"""
    # В будущем — проверка через API, делал ли пользователь квиз сегодня
    text = get_text("quiz_menu")
    if not text:
        text = "Ежедневный квиз временно недоступен."
    
    # Можно добавить кнопку "Начать квиз", если ещё не пройден
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧠 Начать квиз", callback_data="quiz_start")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])
    
    await cb.message.edit_text(text, reply_markup=kb)
    await cb.answer()


@router.callback_query(F.data == "quiz_start")
async def start_quiz(cb: CallbackQuery):
    """Начинает квиз (пока статический пример)"""
    user_id = cb.from_user.id
    logger.info(f"Quiz started by user {user_id}")
    
    quiz_id = 1  # в будущем — из API
    
    text = get_text("quiz_start", title="Daily Crypto Quiz", passing=70, reward=10)
    if not text:
        text = "Квиз начат! Отвечай на вопросы."
    
    # Пример первого вопроса (в будущем — из API / БД)
    question = "Кто создал Bitcoin?"
    options = ["A. Elon Musk", "B. Satoshi Nakamoto", "C. Vitalik Buterin"]
    
    kb = get_quiz_options_kb(quiz_id=quiz_id, question_idx=0, options=options)
    
    full_text = text + "\n\n" + get_text("quiz_question", current=1, total=5, question=question)
    
    await cb.message.edit_text(full_text, reply_markup=kb)
    await cb.answer()


@router.callback_query(F.data.startswith("quiz_ans:"))
async def answer_quiz(cb: CallbackQuery):
    """Обработка ответа на вопрос квиза"""
    try:
        _, quiz_id, q_idx, opt_idx = cb.data.split(":")
        quiz_id, q_idx, opt_idx = int(quiz_id), int(q_idx), int(opt_idx)
    except ValueError:
        logger.error(f"Invalid quiz callback: {cb.data}")
        await cb.answer("Ошибка обработки ответа", show_alert=True)
        return
    
    # Пока статический правильный ответ (в будущем — из API)
    correct_idx = 1  # B. Satoshi Nakamoto
    
    if opt_idx == correct_idx:
        text = get_text("quiz_correct")
    else:
        text = get_text("quiz_wrong", correct_option="B. Satoshi Nakamoto")
    
    # В будущем — переход к следующему вопросу или результат
    # Пока просто показываем результат и возвращаем в меню
    text += "\n\nРезультат квиза будет здесь... (пока статический пример)"
    
    await cb.message.edit_text(text, reply_markup=get_main_menu())
    await cb.answer("Ответ принят!")
