import re
from aiogram import Router, F, Bot
from aiogram.types import Message, MessageReactionUpdated
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo

from credentials import PERMISSION_REQUEST_TOPIC_ID, BOT_TOKEN
from utils.scheduled_jobs import send_permission_reminder, scheduler
from utils.db_query import create_permission_request, update_permission_status, get_user_permission

permission_request_router = Router()
bot = Bot(token=BOT_TOKEN)

@permission_request_router.message(F.text.contains("@khakimov_yas"), F.message_thread_id==PERMISSION_REQUEST_TOPIC_ID)
async def handle_permission_request(message: Message):

    times = re.findall(r'(?:[01]?\d|2[0-3]):[0-5]\d', message.text)
    if not times:
        return await message.reply("Javob so'rash uchun boshlanish vaqtini kiritish shart! Masalan, 12:00 dan 14:00 gacha")
    
    start_time = datetime.strptime(times[0], "%H:%M").time()
    end_time = datetime.strptime(times[1], "%H:%M").time() if len(times) > 1 else None
    await create_permission_request(
        chat_id=message.from_user.id,
        start_time=start_time,
        end_time=end_time,
        request_date=datetime.today().date() + timedelta(days=1) if "ertaga" in message.text.lower() or "эртага" in message.text.lower() else datetime.today().date()
    )
    if end_time:
        tz = ZoneInfo("Asia/Tashkent")
        now = datetime.now(tz)
        end_datetime = datetime.combine(now.date(), end_time, tzinfo=tz)
        delay_seconds = (end_datetime - now).total_seconds()
        
        # Only schedule if end_time is in the future
        if delay_seconds > 0:
            # +10 minutes after end_time
            delay_seconds += 10 * 60

            scheduler.add_job(
                send_permission_reminder,
                'date',
                run_date=now + timedelta(seconds=delay_seconds),
                args=[message.from_user.id, message.from_user.first_name, message.from_user.username]
            )
    
# @permission_request_router.message_reaction()
# async def handle_reaction_update(reaction_update: MessageReactionUpdated):
#     chat_id = reaction_update.chat.id
#     message_id = reaction_update.message_id

#     message = await bot.get_message(chat_id=chat_id, message_id=message_id)

#     if message.message_thread_id == PERMISSION_REQUEST_TOPIC_ID:
#         user = reaction_update.user

#         if reaction_update.new_reaction:
#             if user.username == "temporaryadm":
#                 await update_permission_status(
#                     chat_id=user.id,
#                     day=datetime.today().date(),
#                     status='approved',
#                     from_status='pending'
#                 )

@permission_request_router.message(F.video_note, F.message_thread_id==PERMISSION_REQUEST_TOPIC_ID)
async def handle_video_note(message: Message):
    print("Video note received")
    user = message.from_user
    permission = await get_user_permission(chat_id=user.id)
    if permission and permission['end_time'] is not None:
        await message.reply("Video eslatma qabul qilindi. Rahmat!")
        await update_permission_status(
            chat_id=user.id,
            day=datetime.today().date(),
            status='completed',
            from_status='approved'
        )