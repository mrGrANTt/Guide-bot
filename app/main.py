import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config import BOT_TOKEN
from app.handlers import (start_router, menu_router, quiz_router, cards_router)

from app.database.db import init_db, close_db

async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(quiz_router)
    dp.include_router(cards_router)

    try:
        logging.info("База данных запускается")
        await init_db()
        logging.info("Бот запускается")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await close_db()
        logging.info("Программа остановлена...")


if __name__ == "__main__":
    asyncio.run(main())
