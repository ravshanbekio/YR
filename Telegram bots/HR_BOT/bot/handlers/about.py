from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

about_router = Router()

@about_router.message(F.text=="ℹ️ Biz haqimizda")
async def handle_about(message: Message, state: FSMContext):
    logo = FSInputFile("yr-logo.png")
    text = "*Yangicha Rivoj*©️ - distributorlik firmasi. Biz asosan, oziq-ovqat, " \
    "kolbasa, ichimlik suvlari va sut mahsulotlarini yetkazib berish bilan shug'ullanadi."
    await message.answer_photo(logo, parse_mode="Markdown", caption=text)
    await state.set_state(None)