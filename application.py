# application.py
import os
import threading

from flask import Flask
from aiogram import executor
from config import dp
from handlers.menu import register_handlers
from middlewares.spam import SpamMiddleware

# 1) Install your spam‐protection middleware
dp.middleware.setup(SpamMiddleware(max_messages=3, window_seconds=10.0))

# 2) Register all your handlers
register_handlers(dp)

# 3) Start the bot in a background thread
def start_bot():
    executor.start_polling(dp, skip_updates=True)

threading.Thread(target=start_bot, daemon=True).start()

# 4) Health‐check endpoint for Elastic Beanstalk
app = Flask(__name__)

@app.route("/", methods=["GET"])
def health_check():
    return "OK", 200

if __name__ == "__main__":
    # EB will set PORT; default to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
