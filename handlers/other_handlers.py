"""
Модуль с хэндлерами, которые не попали в ругие модули с хэндлерами
"""
from aiogram import Router
from aiogram.filters import Command, CommandStart, Text, StateFilter, or_f
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types.message import ContentType
from typing import Any, List
from asyncpg import Record

from lexicon import LEXICON_RU


router: Router = Router()



