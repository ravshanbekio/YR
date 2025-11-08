import asyncio
from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.inline import skip_button
from api.vacancy import get_vacancies, get_vacancy

vacancies_router = Router()

vacancies = asyncio.run(get_vacancies())
user_questions = {}
user_index = {}

class ApplicationState(StatesGroup):
    waiting_for_answer = State()

@vacancies_router.message(F.text=="💼 Vakansiyalar")
async def handle_vacancies(message: Message):
    vacancies = await get_vacancies()

    if not vacancies:
        return message.answer("❌ Hozircha ochiq vakansiyalar mavjud emas")
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=vacancy["title"])] for vacancy in vacancies
        ],
        resize_keyboard=True, 
        one_time_keyboard=True
    )
    await message.answer("👇 O'zingizga mos vakansiyani tanlang:", reply_markup=keyboard)

@vacancies_router.message(F.text.in_([vacancy['title'] for vacancy in vacancies]))
async def handle_vacancy(message: Message, state: FSMContext):
    get_vacancy_data = await get_vacancy(data=message.text)
    if not get_vacancy_data:
        return message.answer("Vakansiya topilmadi")

    response = "*Vakansiya haqida ma'lumot:* \n" \
    f"*Sarlavha:* *{get_vacancy_data['title']}* \n" \
    f"*To'liq ma'lumot:* {get_vacancy_data['description'] if get_vacancy_data['description'] is not None else "Mavjud emas"} \n\n" \
    "Vakansiyaga topshirish uchun quyidagi savollarga javob berishingiz so'raladi👇"

    await message.answer(response, parse_mode="Markdown")

    user_questions[message.chat.id] = sorted(get_vacancy_data['questions'], key=lambda q: q["id"])
    user_index[message.chat.id] = 0

    await ask_next_question(message, state)

async def ask_next_question(message: Message, state: FSMContext):
    chat_id = message.chat.id
    index = user_index.get(chat_id, 0)
    questions = user_questions.get(chat_id)

    if index >= len(questions):
        print(index)
        print(questions)
        await state.clear()
        await message.answer("Siz barcha savollarga javob berdingiz")

    q = questions[index]
    text = f"📝 {q['title']}"
    is_required = q.get("is_required", True)
    qtype = q.get("question_type", "text")

    if not is_required:
        await message.answer(text, reply_markup=skip_button())
    else:
        await message.answer(text)

    await state.set_state(ApplicationState.waiting_for_answer)
    await state.update_data(current_question=q)

@vacancies_router.message(ApplicationState.waiting_for_answer)
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    q = data.get("current_question")

    if not q:
        return await message.answer("❌ Xatolik, iltimos keyinroq urinib ko'ring!")

    qtype = q.get("question_type")

    # Validate type
    if qtype == "tekst" and not message.text:
        return await message.answer("Iltimos, matn yuboring")
    if qtype == "fayl" and not (message.document or message.voice or message.video_note):
        return await message.answer("❌ Matn yuborish mumkin emas")

    # Save answer (you can send it to backend here)
    await message.answer("✅ Answer saved!")

    chat_id = message.chat.id
    user_index[chat_id] += 1
    print(user_index)
    await ask_next_question(message, state)

@vacancies_router.callback_query(F.data == "skip_question")
async def skip_question(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    user_index[chat_id] += 1
    await callback.message.edit_text("⏩ Skipped.")
    await ask_next_question(callback.message, state)