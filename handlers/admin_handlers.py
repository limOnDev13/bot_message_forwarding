"""
Модуль с хэндлерами, срабатывающими на действия пользователя,
если он является администратором бота.
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


@router.message(Command(commands='start'))
async def process_admin_start_command(message: Message):
    await message.answer(text=LEXICON_RU['start_admin'])


@router.message(Command(commands='help'))
async def process_admin_help_command(message: Message):
    await message.answer(text=LEXICON_RU['help_admin'])
