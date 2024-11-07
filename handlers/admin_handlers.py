"""
Модуль с хэндлерами, срабатывающими на действия пользователя,
если он является администратором бота.
"""
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from lexicon import LEXICON_RU
from filters import ItIsPeriod, ItIsAdmin
from states import FSMFillingData
from services import services


router: Router = Router()
router.message.filter(ItIsAdmin())


@router.message(Command(commands='start'))
async def process_admin_start_command(message: Message):
    await message.answer(text=LEXICON_RU['start_admin'])


@router.message(Command(commands='help'))
async def process_admin_help_command(message: Message):
    await message.answer(text=LEXICON_RU['help_admin'])


# Хэндлер для обработки команды /cancel в не дефолтном состоянии
@router.message(~StateFilter(default_state), Command(commands='cancel'))
async def process_cancel_filling_data(message: Message, state: FSMContext):
    # Сбросим состояние до дефолтного
    await state.clear()
    # # Сообщим об этом пользователю
    await message.answer(text=LEXICON_RU['cancel_filling'])


# Хэндлер для обработки введенного текста в состоянии ввода текста сообщения
@router.message(StateFilter(FSMFillingData.fill_message), F.text)
async def process_input_message_text(message: Message, state: FSMContext):
    # Изменим состояние на ввод периода времени
    await state.set_state(FSMFillingData.fill_period)
    # Сохраним введеный текст в оперативной памяти
    await state.update_data(msg_text=message.text)
    # Попросим пользователя ввести период времени
    await message.answer(text=LEXICON_RU['fill_period'])


# Хэндлер для обработки введенного периода в днях в состоянии ввода периода
@router.message(StateFilter(FSMFillingData.fill_period), ItIsPeriod())
async def process_input_period(message: Message, state: FSMContext,
                               scheduler: AsyncIOScheduler):
    # Сохраним период в оперативную память
    period: int = int(message.text)
    await state.update_data(period=period)
    # Запланируем периодическую отправку сообщения
    await services.planning_send_message(state, scheduler)
    # Сбросим состояние до дефолтного
    await state.clear()


# Хэндлер для обработки введенного username
@router.message()
async def process_input_username(message: Message, state: FSMContext):
    # Изменим состояние на ввод текста сообщения
    await state.set_state(FSMFillingData.fill_message)
    # Сохраним username в оперативной памяти
    await state.update_data(username=message.text)
    # Попросим ввести текст сообщения
    await message.answer(text=LEXICON_RU['fill_message_text'])
