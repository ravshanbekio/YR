from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime
from zoneinfo import ZoneInfo
from credentials import GROUP_TOPIC_ID
from utils.db_query import get_user, create_user
from utils.services import AttendanceService
from utils.storage import save_chat_id

commands_router = Router()
attendance_service = AttendanceService()

@commands_router.message(Command("iarrived"), F.message_thread_id==GROUP_TOPIC_ID)
async def start_command_handler(message: Message):
    profile = message.from_user
    chat_id = profile.id
    first_name = profile.first_name
    username = profile.username
    await save_chat_id(message.chat.id)
    user = await get_user(chat_id=chat_id)
    if not user:
        await create_user(chat_id=chat_id, first_name=first_name, username=username)
    
    await attendance_service.process(chat_id=chat_id)
    await message.reply(f"*{message.from_user.first_name}, ishga kelgan sifatida davomatga belgilandingiz!*", parse_mode="Markdown")
    if datetime.now(ZoneInfo("Asia/Tashkent")).time() > '09:05:00':
        await message.reply("*Ishga kech qoldingiz, sizga 300 000 so'm jarima solinadi*", parse_mode="Markdown")

@commands_router.message(Command("ileft"), F.message_thread_id==GROUP_TOPIC_ID)
async def leave_command_handler(message: Message):
    if datetime.now(ZoneInfo("Asia/Tashkent")).time() < attendance_service.WORK_END:
        await message.reply(f"*{message.from_user.first_name}, ish vaqti tugashidan oldin ishdan ketish mumkin emas!*", parse_mode="Markdown")
        return
    
    profile = message.from_user
    chat_id = profile.id
    first_name = profile.first_name
    username = profile.username
    await save_chat_id(message.chat.id)
    user = await get_user(chat_id=chat_id)
    if not user:
        await create_user(chat_id=chat_id, first_name=first_name, username=username)
    
    await attendance_service.process(chat_id=chat_id)
    await message.reply(f"*{message.from_user.first_name}, ishdan ketgan sifatida davomatga belgilandingiz!*", parse_mode="Markdown")