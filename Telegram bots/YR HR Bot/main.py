import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher

from credentials import BOT_TOKEN
from handlers import start, about, vacancies

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start.start_router)
dp.include_router(about.about_router)
dp.include_router(vacancies.vacancies_router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())