from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def language_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    # each add() call creates a new row:
    kb.add(KeyboardButton("🇺🇿 O‘zbek"))
    kb.add(KeyboardButton("🇷🇺 Русский"))
    kb.add(KeyboardButton("🇬🇧 English"))
    return kb