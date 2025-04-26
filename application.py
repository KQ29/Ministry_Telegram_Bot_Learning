# bot.py
from aiogram import executor
from config import dp
from handlers.menu import register_handlers
from middlewares.spam import SpamMiddleware

if __name__ == '__main__':
    # Prevent users from sending more than 3 messages in 10 seconds
    dp.middleware.setup(SpamMiddleware(max_messages=3, window_seconds=10.0))

    # Register all your handlers
    register_handlers(dp)

    # Start polling
    executor.start_polling(dp, skip_updates=True)
