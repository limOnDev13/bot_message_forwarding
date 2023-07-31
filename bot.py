import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types.message import ContentType
from aiogram.filters import Command
import asyncpg
from asyncpg.pool import Pool
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from keyboards import set_main_menu
from config_data import Config, load_config
from handlers import other_handlers, user_handlers
from handlers.buy_premium import order, send_pre_checkout_query, successful_payment
from middlewares import DataBaseMiddleware, SchedulerMiddleware


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')

    config: Config = load_config(None)
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)

    # Вывод кнопки меню
    await set_main_menu(bot)

    # Настройка пула подключений к бд
    pool_connect: Pool = await asyncpg.create_pool(host=config.con_pool.db.host,
                                                   port=config.con_pool.db.port,
                                                   database=config.con_pool.db.db_name,
                                                   user=config.con_pool.user.user,
                                                   password=config.con_pool.user.password
                                                   )

    # Работа с планировщиком выполнения заданий
    scheduler: AsyncIOScheduler = AsyncIOScheduler()
    scheduler.start()

    # Регистрируем мидлвари
    dp.update.middleware.register(DataBaseMiddleware(pool_connect))
    dp.update.middleware.register(SchedulerMiddleware(scheduler))

    # Регистрируем хэндлеры для оплаты премиума
    dp.message.register(order, Command(commands=['premium']))
    dp.pre_checkout_query.register(send_pre_checkout_query)
    dp.message.register(successful_payment,
                        F.content_type.in_({ContentType.SUCCESSFUL_PAYMENT}))

    # Регистрируем роутеры
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

