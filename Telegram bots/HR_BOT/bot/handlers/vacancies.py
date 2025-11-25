import asyncio
from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.inline import skip_button
from api.vacancy import get_vacancies, get_vacancy, save_answer
from api.user import get_user, create_user

vacancies_router = Router()

EXCLUDE_BUTTONS = ["🏠 Bosh menyu",]

vacancies = asyncio.run(get_vacancies())
user_questions = {}
user_answers = {}
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
    keyboard.keyboard.append([KeyboardButton(text="🏠 Bosh menyu")])
    await message.answer("👇 O'zingizga mos vakansiyani tanlang:", reply_markup=keyboard)

@vacancies_router.message(F.text.not_in(EXCLUDE_BUTTONS), ~StateFilter(ApplicationState.waiting_for_answer))
async def handle_vacancy(message: Message, state: FSMContext):
    get_vacancy_data = await get_vacancy(data=message.text)
    if not get_vacancy_data:
        return message.answer("Vakansiya topilmadi")
    
    if not get_vacancy_data['questions']:
        return message.answer("Ushbu vakansiyada hech qanday savol mavjud emas!")

    response = "*Vakansiya haqida ma'lumot:* \n" \
    f"*Sarlavha:* *{get_vacancy_data['title']}* \n" \
    f"*To'liq ma'lumot:* {get_vacancy_data['description'] if get_vacancy_data['description'] is not None else "Mavjud emas"} \n\n" \
    "Vakansiyaga topshirish uchun quyidagi savollarga javob berishingiz so'raladi👇"

    await message.answer(response, parse_mode="Markdown")

    user_questions[message.chat.id] = sorted(get_vacancy_data['questions'], key=lambda q: q["id"])
    user_index[message.chat.id] = 0
    
    await ask_next_question(message, state, get_vacancy_data['id'])

async def ask_next_question(message: Message, state: FSMContext, vacancy_id: int):
    chat_id = message.chat.id
    index = user_index.get(chat_id, 0)
    questions = user_questions.get(chat_id)

    await state.update_data(vacancy_id=vacancy_id)

    if not questions or index >= len(questions):
        user = await get_user(chat_id=chat_id)
        if not user:
            await create_user(chat_id=chat_id, full_name=message.chat.first_name, username=message.chat.username, phone_number=None)

        # Saving the answer logic
        for answer in user_answers.get(chat_id, []):
            await save_answer(chat_id=chat_id, vacancy_id=vacancy_id, question_id=answer['question_id'], answer=answer['answer'])
        
        user_questions.pop(chat_id, None)
        user_index.pop(chat_id, None)
        user_answers.pop(chat_id, None)
        await state.clear()
        return await message.answer("✅ *Sizning ma'lumotlaringiz ko'rib chiqish uchun yuborildi. \nMa'lumotlaringiz ko'rib chiqilib, sizga xabar beriladi*", parse_mode="Markdown")
    
    q = questions[index]
    text = f"📝 {q['title']}"
    is_required = q.get("is_required", True)

    if not is_required:
        await message.answer(text, reply_markup=skip_button())
    else:
        await message.answer(text)

    await state.set_state(ApplicationState.waiting_for_answer)
    await state.update_data(current_question=q)

@vacancies_router.message(ApplicationState.waiting_for_answer, F.text.not_in(EXCLUDE_BUTTONS))
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    q = data.get("current_question")
    vacancy_id = data.get("vacancy_id")

    if not q:
        return await message.answer("❌ Xatolik, iltimos keyinroq urinib ko'ring!")
    qtype = q.get("question_type")

    # Validate type
    if qtype == "tekst" and not message.text:
        return await message.answer("Iltimos, matn yuboring")
    if qtype == "fayl" and not (message.document or message.voice or message.video_note):
        return await message.answer("❌ Matn yuborish mumkin emas")
    
    # Saving the answers to the local variable
    user_answers.setdefault(message.chat.id, []).append({
        "question_id": q["id"],
        "answer": message.text
    })

    chat_id = message.chat.id
    user_index[chat_id] += 1
    await ask_next_question(message, state, vacancy_id)

@vacancies_router.callback_query(F.data == "skip_question")
async def skip_question(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    vacancy_id = await data.get("vacancy_id")
    chat_id = callback.message.chat.id
    user_index[chat_id] += 1
    await callback.message.edit_text("⏩ Savol o'tkazib yuborildi.")
    await ask_next_question(callback.message, state, vacancy_id)