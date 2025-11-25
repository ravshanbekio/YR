from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext  

return_handler_router = Router()

@return_handler_router.message(F.text=="🏠 Bosh menyu")
async def return_handler(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💼 Vakansiyalar")],
            [KeyboardButton(text="ℹ️ Biz haqimizda")]
        ],
        resize_keyboard=True
    )
    await message.answer("🏠 Bosh menyu!", parse_mode="Markdown", reply_markup=keyboard)
    await state.set_state(None)