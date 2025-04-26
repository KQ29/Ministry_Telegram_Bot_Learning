import time
from collections import deque
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler

class SpamMiddleware(BaseMiddleware):
    """
    Middleware to prevent users from sending more than `max_messages` in `window_seconds`.
    """
    def __init__(self, max_messages: int = 3, window_seconds: float = 10.0):
        super().__init__()
        self.max_messages = max_messages
        self.window_seconds = window_seconds
        # user_id -> deque of timestamps
        self._timestamps: dict[int, deque[float]] = {}

    async def on_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        now = time.time()
        dq = self._timestamps.get(user_id)
        if dq is None:
            dq = deque()
            self._timestamps[user_id] = dq

        # Remove timestamps older than window
        while dq and now - dq[0] > self.window_seconds:
            dq.popleft()

        # Add current timestamp
        dq.append(now)

        # If too many messages in window, cancel handling
        if len(dq) > self.max_messages:
            await message.answer("🚫 Iltimos, biroz sekinroq yozing—spamga yo‘l qo‘ymang!")
            raise CancelHandler()
