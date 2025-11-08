from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from credentials import ADMIN_CHAT_ID, GROUP_TOPIC_ID

admin_panel_router = Router()

class UserCreationState(StatesGroup):
    chat_id = State()
    first_name = State()
    username = State()

@admin_panel_router.message(F.text=="/admin", F.message_thread_id==GROUP_TOPIC_ID)
async def admin_panel_handler(message: Message):
    text = "❌ Sizda yetarli huquqlar mavjud emas"
    if message.chat.id != int(ADMIN_CHAT_ID):
        return message.reply(text)
    
    text = "Admin panelga xush kelibsiz"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Xodim qo'shish")],
        ],
        resize_keyboard=True
    )
    await message.answer(text=text, reply_markup=keyboard)
    
@admin_panel_router.message(F.text=="➕ Xodim qo'shish", F.message_thread_id==GROUP_TOPIC_ID)
async def create_user_handler(message: Message, state: FSMContext):
    text = "Yangi Xodimni `chat id` raqamini kiriting:"
    await message.reply(text=text, parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserCreationState.chat_id)
    
@admin_panel_router.message(UserCreationState.chat_id)
async def chatid_handler(message: Message, state: FSMContext):
    await state.update_data(chat_id=message.text)
    text = "Ismni kiriting"
    await message.reply(text)
    await state.set_state(UserCreationState.first_name)

@admin_panel_router.message(UserCreationState.first_name)
async def first_name_handler(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    text = "Telegram `username` ni kiriting (ixtiyoriy)"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏭️ Yakunlash")],
        ],
        resize_keyboard=True
    )
    await message.answer(text=text, parse_mode="Markdown", reply_markup=keyboard)
    await state.set_state(UserCreationState.username)
    
@admin_panel_router.message(UserCreationState.username or F.text=="⏭️ Yakunlash")
async def username_handler(message:Message, state: FSMContext):
    text = "✅ Xodim muvaffaqiyatli qo'shildi"
    await message.answer(text)
    await state.set_state(None)