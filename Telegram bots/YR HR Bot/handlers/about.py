from aiogram import Router, F
from aiogram.types import Message, FSInputFile

about_router = Router()

@about_router.message(F.text=="ℹ️ Biz haqimizda")
async def handle_about(message: Message):
    logo = FSInputFile("logo.png")
    text = "*{company_name}*©️ - distributorlik firmasi. Biz asosan, oziq-ovqat, " \
    "kolbasa, ichimlik suvlari va sut mahsulotlarini yetkazib berish bilan shug'ullanadi."
    await message.answer_photo(logo, parse_mode="Markdown", caption=text)