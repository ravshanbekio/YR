from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from credentials import GROUP_TOPIC_ID

start_router = Router()

@start_router.message(CommandStart(), F.message_thread_id==GROUP_TOPIC_ID)
async def start_handler(message: Message):
    text = "👋 Salom! Meni guruhga qo'shing va men ishga kelish va ketish "\
    "vaqtlarini hisoblab haftalik/oylik hisobot tayyorlab beraman"
    await message.answer(text)