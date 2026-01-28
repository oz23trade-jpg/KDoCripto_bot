import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

from handlers.start import router as start_router
from handlers.language import router as lang_router
from handlers.profile import router as profile_router
from handlers.menu import router as menu_router
# добавь остальные handlers сюда

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Регистрация роутеров
dp.include_router(start_router)
dp.include_router(lang_router)
dp.include_router(profile_router)
dp.include_router(menu_router)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())