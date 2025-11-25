from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import CommandStart

from credentials import ADMIN_CHAT_ID

start_router = Router()

@start_router.message(CommandStart())
async def handle_start(message: Message):
    text = "👋 Assalomu aleykum! " \
    "*Yangicha Rivoj*©️ kompaniyasining HR botiga xush kelibsiz. \n" \
    "Ushbu bot orqali, kompaniyamizdagi ochiq vakansiyalarga topshirishingiz mumkin. \n\n" \
    "*Quyidagi menyulardan birini tanlang👇*"

    if message.chat.id != ADMIN_CHAT_ID:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="💼 Vakansiyalar")],
                [KeyboardButton(text="ℹ️ Biz haqimizda")]
            ],
            resize_keyboard=True
        )
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📃 Admin panel", web_app=WebAppInfo(url="https://hr.yangicharivoj.uz/"))]
            ],
            resize_keyboard=True
        )
    await message.answer(text=text, parse_mode="Markdown", reply_markup=keyboard)