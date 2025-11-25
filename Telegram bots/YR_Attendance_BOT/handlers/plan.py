from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime, timezone, time, timedelta
from zoneinfo import ZoneInfo

from credentials import PLAN_TOPIC_ID
from utils.db_query import create_plan

plan_router = Router()

@plan_router.message(F.message_thread_id==PLAN_TOPIC_ID)
async def handle_plan(message: Message):
    today = None
    if datetime.now(ZoneInfo("Asia/Tashkent")).time() > time(8, 0) and datetime.now(ZoneInfo("Asia/Tashkent")).time() < time(16, 0):
        today = datetime.today().date()
    elif datetime.now(ZoneInfo("Asia/Tashkent")).time() > time(16, 0):
        today = datetime.today().date() + timedelta(days=1)
        
    await create_plan(chat_id=message.from_user.id, plan=message.text, day=today)