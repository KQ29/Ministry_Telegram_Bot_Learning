from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
if not API_TOKEN:
    raise RuntimeError("Missing TELEGRAM_API_TOKEN env var")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())