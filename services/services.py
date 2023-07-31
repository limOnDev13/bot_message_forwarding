"""
Модуль с реализацией бизнес-логики.
"""
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import Any
from datetime import datetime, timedelta


# Функция для отправки сообщения определенному пользователю. Эта функция будет
# добавляться в планировщик
async def _send_message(username: str, msg_text: str):
    bot: Bot = Bot.get_current()
    await bot.send_message(chat_id=username, text=msg_text)


async def planning_send_message(state: FSMContext, scheduler: AsyncIOScheduler):
    saved_info: dict[str, Any] = await state.get_data()
    username: str = saved_info['username']
    msg_text: str = saved_info['msg_text']
    period: int = saved_info['period']

    if period != 0:
        scheduler.add_job(_send_message, trigger='cron', day=f'*/{period}',
                          hour=str(datetime.now().hour),
                          minute=str(datetime.now().minute),
                          second=str(datetime.now().second + 10),
                          start_date=datetime.now() + timedelta(seconds=10),
                          args=[username, msg_text])
    else:
        scheduler.add_job(_send_message, trigger='cron',
                          second=f'*/10',
                          start_date=datetime.now() + timedelta(seconds=10),
                          args=[username, msg_text])

