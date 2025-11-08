from aiogram import Bot
from pytz import timezone
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random
from credentials import GROUP_TOPIC_ID, DUTY_TOPIC_ID, PERSISTENTS_TOPIC_ID, BOT_TOKEN
from utils.db_query import get_arrived_users, get_missing_users, get_remaining_users, get_delayed_times, update_delayed_times, get_unpersistent_users, get_persistent_users
from utils.storage import load_chat_ids
from utils.services import get_tomorrow_duty, START_DATE

bot = Bot(token=BOT_TOKEN)
scheduler = AsyncIOScheduler(timezone=timezone("Asia/Tashkent"))
penalty_amount = 300000  # Penalty amount in local currency

async def arrived_users_message():
    chat_ids = await load_chat_ids()
    today = datetime.today().date()
    weekday = today.weekday()
    arrived_users_list = await get_arrived_users(day=today)
    missing_users_list = await get_missing_users(day=today)
    
    if not arrived_users_list:
        text = "*Hech kimga kelmadi*"
    else:
        text = "\n".join([f"*{ordinal_number + 1}. {user['first_name'].rstrip()} - {user['arrival_time'].strftime("%H:%M")}*" for ordinal_number, user in enumerate(arrived_users_list)])
    missing_users_text = "\n".join([f"*{ordinal_number + 1}. {user['first_name'].rstrip()}*" for ordinal_number, user in enumerate(missing_users_list)]) if missing_users_list else "Alhamdulillah, hamma keldi!"

    for chat_id in chat_ids:
        await bot.send_message(text=f"Kech qolganlarga jarima yozib qo'yildi! \n*Bugungi ishga kelganlar ro'yxati*: \n{text}", chat_id=chat_id, message_thread_id=GROUP_TOPIC_ID, parse_mode="Markdown")

        if weekday == 6:  # Sunday
            print("Bugun yakshanba - video tashlamaganlar ro'yxati yuborilmadi.")
            rest_texts = [
                "Yakshanba, dam olish kuningiz maroqli o'tsin!",
                "Yaxshi dam - mehnatga hamdam! Charchoqlarni chiqaring, yangi haftaga yangi energiya bilan kirishing!",
                "Bugun yakshanba, hech qanday qo'shimcha e'lonlar yo'q! Mazza qil ukam )",
                "Qolganlar dam olyapti. Siz ishlayapsizmi? Siqilmang, keyingi hafta dam olasiz. \nUngacha ishni bosing!"
            ]
            await bot.send_message(text=random.choice(rest_texts), chat_id=chat_id, message_thread_id=GROUP_TOPIC_ID, parse_mode="Markdown")
        else:
            await bot.send_message(text=f"*Video tashlamaganlar ro'yxati:* \n{missing_users_text}\n\n*✨ Kuningiz hayrli va barokatli o'tsin!*", chat_id=chat_id, message_thread_id=GROUP_TOPIC_ID, parse_mode="Markdown")
        
async def remaining_users_message():
    chat_ids = await load_chat_ids()
    today = datetime.today().date()
    remaining_users_list = await get_remaining_users(day=today)
    
    if not remaining_users_list:
        text = "*Barcha xodimlar ketdi!*"
    else:
        users = "\n".join([f"*{ordinal_number + 1}. {user['first_name'].rstrip()}*" for ordinal_number, user in enumerate(remaining_users_list)])
        text = f"*Quyidagi xodimlar ishdan ketmadi (video tashlamadi):* \n{users}"
        
    leaving_texts = [
        "Bo'ldi endi, uyga bor. Uydegilar kutyapti! 🏠",
        "Ishingiz yakunlangan bo'lsa, ish joyingizni tark eting va video tashlashni unutmang! 📹",
    ]
    for chat_id in chat_ids:
        await bot.send_message(text=text, chat_id=chat_id, message_thread_id=GROUP_TOPIC_ID, parse_mode="Markdown")
        if remaining_users_list:
            await bot.send_message(text=random.choice(leaving_texts), chat_id=chat_id, message_thread_id=GROUP_TOPIC_ID, parse_mode="Markdown")

async def get_delayed_users():
    chat_ids = await load_chat_ids()
    get_users = await get_delayed_times()
    
    if not get_users:
        text = "*Oy davomida hech kim kech qolib kelmadi!* \n👏 Qoyil"
    else:
        delayed_text = "\n".join([f"*{ordinal_number + 1}. {user['first_name'].rstrip()} - {penalty_amount * user['number_of_late']} so'm* ({user['number_of_late']} marta kech qolgan)" for ordinal_number, user in enumerate(get_users)])
        text = f"*Oy davomida kech qolgan xodimlar ro'yxati va ularga belgilangan jarima miqdori:* \n{delayed_text}"
    
    for chat_id in chat_ids:
        await bot.send_message(text=text, chat_id=chat_id, message_thread_id=GROUP_TOPIC_ID, parse_mode="Markdown")
        await update_delayed_times()

async def send_duty_reminder():
    """Send reminder message to all chat IDs."""
    duty_person = get_tomorrow_duty(START_DATE)
    if not duty_person:
        print("Tomorrow is Sunday — no duty reminder sent.")
        return

    text = f"🕘 *Eslatma!*\nErtangi navbatchi: *{duty_person}*"
    chat_ids = await load_chat_ids()

    for chat_id in chat_ids:
        await bot.send_message(
            chat_id=chat_id,
            message_thread_id=DUTY_TOPIC_ID,
            text=text,
            parse_mode="Markdown"
        )

async def send_unpersistent_users():
    chat_ids = await load_chat_ids()
    unpersistent_users = await get_unpersistent_users()
    
    if not unpersistent_users:
        text = "*Hamma qat'iyatli!* \n👏 Qoyil"
    else:
        unpersistent_text = "\n".join([f"*{ordinal_number + 1}. {user['first_name'].rstrip()}*" for ordinal_number, user in enumerate(unpersistent_users)])
        text = f"*Quyidagi xodimlar tongda tura olishmadi* \n{unpersistent_text} \n\n*Tongda uyg'onish - bu muvaffaqiyatning kalitidir! Ertaga yanada qat'iyatli bo'ling!*"
    
    for chat_id in chat_ids:
        await bot.send_message(text=text, chat_id=chat_id, message_thread_id=PERSISTENTS_TOPIC_ID, parse_mode="Markdown")

async def send_monthly_persistents():
    chat_ids = await load_chat_ids()
    persistent_users = await get_persistent_users()
    
    if not persistent_users:
        text = "*Bu oy hech kim qat'iyatli bo'la olmadi!*"
    else:
        text = "\n".join([f"*{ordinal_number + 1}. {user['first_name'].rstrip()} - {user['total_days']} kun*" for ordinal_number, user in enumerate(persistent_users)])

    for chat_id in chat_ids:
        await bot.send_message(text=f"*Bu oy eng qat'iyatli xodimlar ro'yxati*: \n{text}", chat_id=chat_id, message_thread_id=PERSISTENTS_TOPIC_ID, parse_mode="Markdown")