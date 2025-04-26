# handlers/menu.py
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import json
import asyncio

# Supported languages and prompts
VALID_LANGUAGES = ["🇺🇿 O‘zbek", "🇷🇺 Русский", "🇬🇧 English"]
LANGUAGE_PROMPTS = {
    "uz": "Quyidagilardan birini tanlang:",
    "ru": "Выберите тему:",
    "en": "Please choose a topic:"
}

# Prompts for IT subcategory selection per language
IT_VARIANT_PROMPTS = {
    "uz": "Quyidagi yo‘nalishlardan birini tanlang:",
    "ru": "Выберите один из следующих языков:",
    "en": "Please choose one of the following languages:"
}

# Topics per language
topics = {
    "uz": ["💻 IT va dasturlash", "🇬🇧 Ingliz tili", "🎨 Grafik dizayn"],
    "ru": ["💻 IT и программирование", "🇬🇧 Английский язык", "🎨 Графический дизайн"],
    "en": ["💻 IT & Programming", "🇬🇧 English Language", "🎨 Graphic Design"]
}

# Map displayed topics to internal keys
topic_keys = {
    "💻 IT va dasturlash": "IT",
    "💻 IT и программирование": "IT",
    "💻 IT & Programming": "IT",
    "🇬🇧 Ingliz tili": "English",
    "🇬🇧 Английский язык": "English",
    "🇬🇧 English Language": "English"
}

# In-memory user language preferences
user_language = {}


def get_language_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for lang in VALID_LANGUAGES:
        kb.add(KeyboardButton(lang))
    return kb


def get_topic_keyboard(lang_code: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for topic in topics.get(lang_code, []):
        kb.add(KeyboardButton(topic))
    return kb


def get_it_variants_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for course in ["Python", "JavaScript (JS)", "Java", "C++", "C#", "Ruby"]:
        kb.add(KeyboardButton(course))
    return kb


async def start_handler(message: types.Message):
    await message.answer(
        "🇺🇿 Tilni tanlang / Выберите язык / Choose your language:",
        reply_markup=get_language_keyboard()
    )


async def language_handler(message: types.Message):
    text = message.text
    if text not in VALID_LANGUAGES:
        return

    user_id = message.from_user.id
    if text == "🇺🇿 O‘zbek":
        lang_code, confirm = "uz", "✅ Til o‘zbek tiliga o‘zgartirildi."
    elif text == "🇷🇺 Русский":
        lang_code, confirm = "ru", "✅ Язык переключён на русский."
    else:
        lang_code, confirm = "en", "✅ Language set to English."

    user_language[user_id] = lang_code
    await message.answer(confirm)
    await message.answer(LANGUAGE_PROMPTS[lang_code], reply_markup=get_topic_keyboard(lang_code))


async def topic_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_language:
        await message.answer("Iltimos, avval tilni tanlang: /start yoki /choose_language")
        return

    text = message.text
    lang_code = user_language[user_id]

    # Main topic (non-IT)
    if text in topic_keys and topic_keys[text] != "IT":
        course_key = topic_keys[text]
        with open("data/courses.json", encoding="utf-8") as f:
            data = json.load(f)
        entries = data.get(course_key, {}).get(lang_code, [])
        if not entries:
            await message.answer("Bu til uchun darslar hozircha mavjud emas.")
            return

        # Send header
        headers = {
            "uz": f"📚 {text} darslari:",
            "ru": f"📚 Курсы по теме: {text}",
            "en": f"📚 Courses for: {text}"
        }
        await message.answer(headers[lang_code])

        # Send each course with delay
        for c in entries:
            await message.answer(
                f"🎥 {c['title']}\n"
                f"🔗 {c['link']}\n"
                f"📝 {c['description']}"
            )
            await asyncio.sleep(1.5)
        return

    # IT subcategory selection
    if text in topic_keys and topic_keys[text] == "IT":
        prompt = IT_VARIANT_PROMPTS[lang_code]
        await message.answer(prompt, reply_markup=get_it_variants_keyboard())
        return

    # IT subcategory details + courses
    try:
        with open("data/it_languages.json", encoding="utf-8") as f:
            it_data = json.load(f)
        key = text.replace(" (JS)", "")
        info = it_data.get(key, {}).get(lang_code)
        if not info:
            return

        labels = {
            "uz": ("📝 Tavsif:", "🔧 Qayerda ishlatiladi:", "🚀 Loyiha misollari:"),
            "ru": ("📝 Описание:", "🔧 Где используется:", "🚀 Примеры проектов:"),
            "en": ("📝 Description:", "🔧 Used in:", "🚀 Project examples:")
        }[lang_code]

        # Send info blocks
        await message.answer(f"💡 {key}")
        await message.answer(f"{labels[0]}\n{info['description']}")
        await message.answer(f"{labels[1]}\n{info['usage']}")
        await message.answer(f"{labels[2]}\n{info['projects']}")

        # Send each course with delay
        courses = info.get("courses", [])
        if courses:
            list_label = {
                "uz": "📚 Kurslar ro‘yxati:",
                "ru": "📚 Список курсов:",
                "en": "📚 Course list:"
            }[lang_code]
            await message.answer(list_label)
            for c in courses:
                await message.answer(
                    f"- {c['title']}\n"
                    f"  {c['description']}\n"
                    f"  {c['link']}"
                )
                await asyncio.sleep(1.5)
    except Exception:
        await message.answer("Ma'lumotni olishda xatolik yuz berdi.")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start", "choose_language"])
    dp.register_message_handler(language_handler, lambda m: m.text in VALID_LANGUAGES)
    dp.register_message_handler(topic_handler)
