from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def language_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(
        KeyboardButton("🇺🇿 O‘zbek"),
        KeyboardButton("🇷🇺 Русский"),
        KeyboardButton("🇬🇧 English")
    )
    return kb
