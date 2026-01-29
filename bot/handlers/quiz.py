# bot/handlers/quiz.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from texts import get_text
from keyboards.inline import get_main_menu, get_quiz_options_kb

router = Router()


@router.callback_query(F.data == "menu_quiz")
async def show_quiz_menu(cb: CallbackQuery):
    """Показывает меню квиза (пока статический ежедневный)"""
    # В будущем — проверка через API, делал ли пользователь квиз сегодня
    text = get_text("quiz_menu")
    
    await cb.message.edit_text(text, reply_markup=get_main_menu())
    await cb.answer()


@router.callback_query(F.data == "quiz_start")  # или "quiz_start:{id}"
async def start_quiz(cb: CallbackQuery):
    """Начинает квиз (пока статический пример)"""
    quiz_id = 1  # в будущем — из callback
    
    text = get_text("quiz_start", title="Daily Crypto Quiz", passing=70, reward=10)
    
    # Пример вопроса (в будущем — из API / БД)
    question = "Кто создал Bitcoin?"
    options = ["A. Elon Musk", "B. Satoshi Nakamoto", "C. Vitalik Buterin"]
    
    kb = get_quiz_options_kb(quiz_id=quiz_id, question_idx=0, options=options)
    
    await cb.message.edit_text(text + "\n\n" + get_text("quiz_question", current=1, total=5, question=question), reply_markup=kb)
    await cb.answer()


@router.callback_query(F.data.startswith("quiz_ans:"))
async def answer_quiz(cb: CallbackQuery):
    """Обработка ответа на вопрос квиза"""
    _, quiz_id, q_idx, opt_idx = cb.data.split(":")
    
    # Пока статический правильный ответ (в будущем — проверка через API)
    correct_idx = 1  # B. Satoshi Nakamoto
    
    if int(opt_idx) == correct_idx:
        text = get_text("quiz_correct")
    else:
        text = get_text("quiz_wrong", correct_option="B. Satoshi Nakamoto")
    
    # В будущем — переход к следующему вопросу или результат
    await cb.message.edit_text(text + "\n\nРезультат квиза будет здесь...", reply_markup=get_main_menu())
    await cb.answer()
