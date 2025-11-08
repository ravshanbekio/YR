import random
from aiogram import Router, F
from aiogram.types import Message
from datetime import timedelta, datetime, time
from zoneinfo import ZoneInfo
from credentials import GROUP_TOPIC_ID, PERSISTENTS_TOPIC_ID
from utils.db_query import get_user, create_user, create_morning_activity, check_attendance, update_user_penalty
from utils.services import AttendanceService
from utils.storage import save_chat_id

videomessage_router = Router()
attendance_service = AttendanceService()

@videomessage_router.message(F.video_note, F.message_thread_id==GROUP_TOPIC_ID)
async def videomessage_handler(message: Message):
    profile = message.from_user
    chat_id = profile.id
    first_name = profile.first_name
    username = profile.username
    await save_chat_id(message.chat.id)
    user = await get_user(chat_id=chat_id)
    if not user:
        user = await create_user(chat_id=chat_id, first_name=first_name, username=username)
    
    checkAttendance = await check_attendance(chat_id=chat_id, day=message.date.date())
    if not checkAttendance:
        text = [
            "👏 Bo'larkanu xojaka!",
            "👏 E qoyil!",
            "Hammadan erta keldingiz! Kuningiz hayrli bo'lsin! 😊",
        ]
        print(checkAttendance)
        #await message.reply(text=random.choice(text), parse_mode="Markdown")

    await attendance_service.process(chat_id=chat_id)
    if datetime.now(ZoneInfo("Asia/Tashkent")).time() > time(9, 1) and datetime.now(ZoneInfo("Asia/Tashkent")).time() < time(12, 0):
        penalties_amount = (user['number_of_late'] + 1) * 300000
        await message.reply("*Ishga kech qoldingiz, sizga 300 000 so'm jarima solinadi*", parse_mode="Markdown")
        await message.answer(f"Sizning jarimalaringiz summasi *{penalties_amount}* so'mga yetdi", parse_mode="Markdown")
        await update_user_penalty(chat_id=chat_id, penalty=user['number_of_late'] + 1)

@videomessage_router.message(F.video_note, F.message_thread_id==PERSISTENTS_TOPIC_ID)
async def videomessage_persistents_handler(message: Message):
    await save_chat_id(message.chat.id)
    user = await get_user(chat_id=message.from_user.id)
    if not user:
        await create_user(chat_id=message.from_user.id, first_name=message.from_user.first_name, username=message.from_user.username)

    date = message.date + timedelta(hours=5)
    await create_morning_activity(chat_id=message.from_user.id, activity_time=date)