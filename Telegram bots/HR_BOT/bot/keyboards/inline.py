from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def skip_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="O'tkazib yuborish ➡️", callback_data="skip_question")]
    ])
