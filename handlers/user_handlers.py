"""
Модуль с хэндлерами для пользователей с обычным статусом,
например, для тех, кто запустил бота в первый раз.
"""
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, Text, StateFilter, or_f
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types.message import ContentType
from typing import Any, List
from asyncpg import Record

from lexicon import LEXICON_RU


router: Router = Router()
