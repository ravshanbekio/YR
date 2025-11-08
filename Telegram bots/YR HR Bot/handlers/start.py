from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

start_router = Router()

@start_router.message(CommandStart())
async def handle_start(message: Message):
    text = "👋 Assalomu aleykum! " \
    "*{company_name}*©️ kompaniyasining HR botiga xush kelibsiz. \n" \
    "Ushbu bot orqali, kompaniyamizdagi ochiq vakansiyalarga topshirishingiz mumkin. \n\n" \
    "*Quyidagi menyulardan birini tanlang👇*"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💼 Vakansiyalar")],
            [KeyboardButton(text="ℹ️ Biz haqimizda")]
        ],
        resize_keyboard=True
    )
    await message.answer(text=text, parse_mode="Markdown", reply_markup=keyboard)