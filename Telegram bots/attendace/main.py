import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from credentials import BOT_TOKEN
from handlers import start, videomessage, admin_panel, commands
from utils.scheduled_jobs import arrived_users_message, remaining_users_message, get_delayed_users, send_duty_reminder, send_unpersistent_users, send_monthly_persistents, scheduler

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start.start_router)
dp.include_router(videomessage.videomessage_router)
dp.include_router(admin_panel.admin_panel_router)
dp.include_router(commands.commands_router)

async def main():
    scheduler.add_job(send_unpersistent_users, "cron", hour=8, minute=0)
    scheduler.add_job(arrived_users_message, "cron", hour=9, minute=1)
    scheduler.add_job(remaining_users_message, "cron", hour=22, minute=30)
    scheduler.add_job(send_duty_reminder, "cron", hour=21, minute=00)
    scheduler.add_job(get_delayed_users, "cron", day="last", hour=10, minute=40)
    scheduler.add_job(send_monthly_persistents, "cron", day="last", hour=10, minute=40)
    scheduler.start()
    
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())