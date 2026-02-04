# bot/main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher, __version__ as aiogram_version
from dotenv import load_dotenv
import os

# Импорты всех активных роутеров
from handlers.start import router as start_router
from handlers.language import router as lang_router
from handlers.profile import router as profile_router
from handlers.menu import router as menu_router
from handlers.referral import router as referral_router
from handlers.learning import router as learning_router
from handlers.quiz import router as quiz_router
from handlers.support import router as support_router

# Будущие роутеры (раскомментируй по мере добавления)
# from handlers.lottery import router as lottery_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")

logger.info(f"Запуск бота | aiogram v{aiogram_version}")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Регистрация всех активных роутеров
dp.include_router(start_router)      # /start + рефералка
dp.include_router(lang_router)       # lang_
dp.include_router(profile_router)    # profile
dp.include_router(menu_router)       # основные меню
dp.include_router(referral_router)   # рефералка
dp.include_router(learning_router)   # уроки и курсы
dp.include_router(quiz_router)       # квиз
dp.include_router(support_router)    # поддержка и Stars

# Добавляй новые по мере реализации
# dp.include_router(lottery_router)

async def on_startup():
    logger.info("Бот запущен и готов к работе 🚀")


async def on_shutdown():
    logger.info("Бот останавливается...")
    await bot.session.close()


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    await dp.start_polling(
        bot,
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True
    )


if __name__ == "__main__":
    asyncio.run(main())
