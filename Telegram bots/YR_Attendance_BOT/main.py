import asyncio
import logging
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
from aiogram import Bot, Dispatcher
from datetime import datetime
from credentials import BOT_TOKEN, GROUP_TOPIC_ID
from handlers import start, videomessage, admin_panel
from utils.db_query import get_arrived_users, get_missing_users, get_remaining_users, get_delayed_times, update_delayed_times
from utils.storage import load_chat_ids

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
penalty_amount = 300000

scheduler = AsyncIOScheduler(timezone=timezone("Asia/Tashkent"))

dp.include_router(start.start_router)
dp.include_router(videomessage.videomessage_router)
dp.include_router(admin_panel.admin_panel_router)

async def arrived_users_message():
    chat_ids = await load_chat_ids()
    today = datetime.today().date()
    arrived_users_list = await get_arrived_users(day=today)
    missing_users_list = await get_missing_users(day=today)
    
    if not arrived_users_list:
        text = "*Hech kimga kelmadi*"    
    else:
        text = "\n".join([f"*{ordinal_number + 1}. {user['first_name'].rstrip()} - {user['arrival_time'].strftime("%H:%M")}*" for ordinal_number, user in enumerate(arrived_users_list)])
    missing_users_text = "\n".join([f"*{ordinal_number + 1}. {user['first_name'].rstrip()}*" for ordinal_number, user in enumerate(missing_users_list)]) if missing_users_list else "Hamma video tashladi"

    for chat_id in chat_ids:
        await bot.send_message(text=f"*Ishga kelganlar ro'yxati*: \n{text}", chat_id=chat_id, message_thread_id=GROUP_TOPIC_ID, parse_mode="Markdown")
        await bot.send_message(text=f"*Video tashlamaganlar ro'yxati:* \n{missing_users_text}", chat_id=chat_id, message_thread_id=GROUP_TOPIC_ID, parse_mode="Markdown")
        
async def remaining_users_message():
    chat_ids = await load_chat_ids()
    today = datetime.today().date()
    remaining_users_list = await get_remaining_users(day=today)
    
    if not remaining_users_list:
        text = "*Barcha xodimlar ketdi!*"
    else:
        users = "\n".join([f"*{ordinal_number + 1}. {user['first_name'].rstrip()}*" for ordinal_number, user in enumerate(remaining_users_list)])
        text = f"*Quyidagi xodimlar ishdan ketmadi (video tashlamadi):* \n{users}"
        
    for chat_id in chat_ids:
        await bot.send_message(text=text, chat_id=chat_id, message_thread_id=GROUP_TOPIC_ID, parse_mode="Markdown")

async def get_delayed_users():
    chat_ids = await load_chat_ids()
    get_users = await get_delayed_times()
    
    if not get_users:
        text = "*Oy davomida hech kim kech qolib kelmadi!*"
    else:
        delayed_text = "\n".join([f"*{ordinal_number + 1}. {user['first_name'].rstrip()} - {penalty_amount * user['number_of_late']} so'm* ({user['number_of_late']} marta kech qolgan)" for ordinal_number, user in enumerate(get_users)])
        text = f"*Oy davomida kech qolgan xodimlar ro'yxati va ularga belgilangan jarima miqdori:* \n{delayed_text}"
    
    for chat_id in chat_ids:
        await bot.send_message(text=text, chat_id=chat_id, message_thread_id=GROUP_TOPIC_ID, parse_mode="Markdown")
        await update_delayed_times()    

async def main():
    scheduler.add_job(arrived_users_message, "cron", hour=9, minute=0)
    scheduler.add_job(remaining_users_message, "cron", hour=23, minute=59)
    scheduler.add_job(get_delayed_users, "cron", day="1", hour=10, minute=40)
    scheduler.start()
    
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())