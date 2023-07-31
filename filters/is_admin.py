"""
Модуль с функцией фильтром, проверяющей пользователя, является ли
он администратором бота.
"""
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram.types.message import ContentType
from environs import Env


class ItIsAdmin(BaseFilter):
    def __init__(self: int):
        env = Env()
        env.read_env()

        self.admin_id: int = env("ADMIN_IDS")

    async def __call__(self, message: Message) -> bool:
        if message.from_user.id == self.admin_id:
            return True
        else:
            return False
