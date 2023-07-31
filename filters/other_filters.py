"""
Фильтры, которые не попали в другие файлы
"""
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram.types.message import ContentType
from aiogram.fsm.context import FSMContext
from typing import List, Any
from datetime import datetime


class ItIsUsername(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if ((message.content_type is ContentType.TEXT)
                and (message.text == '@')):
            return True
        else:
            return False


class ItIsPeriod(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if ((message.content_type is ContentType.TEXT) and
                (message.text.isdigit()) and (int(message.text) >= 0)):
            return True
        else:
            return False
