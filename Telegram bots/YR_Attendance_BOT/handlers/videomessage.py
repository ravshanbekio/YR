from aiogram import Router, F
from aiogram.types import Message
from credentials import GROUP_TOPIC_ID
from utils.db_query import get_user, create_user
from utils.attendance_service import AttendanceService
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
        await create_user(chat_id=chat_id, first_name=first_name, username=username)
    
    await attendance_service.process(chat_id=chat_id)