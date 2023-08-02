"""
Модуль с классами, отражающими возможные состояния пользователя.
"""
from aiogram.filters.state import StatesGroup, State


class FSMFillingData(StatesGroup):
    fill_message = State()
    fill_period = State()
