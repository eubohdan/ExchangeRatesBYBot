import logging
import asyncio
import datetime
from aiogram import Dispatcher
import redis
from aiogram.fsm.storage.redis import RedisStorage

import getvalues
from create_bot import bot, redis
import database as db
import commands


async def on_start() -> None:
    # await bot.send_message(config.admin_id, '✅Бот запущен.', disable_notification=True)
    # await redis.close()
    pass


async def on_finish() -> None:
    # await bot.send_message(config.admin_id, '⚠Бот остановлен.', disable_notification=True)
    await redis.close()


dp = Dispatcher(storage=RedisStorage(redis=redis))
dp.startup.register(on_start)
dp.shutdown.register(on_finish)


async def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    db.start_db()
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    cur_list_today = getvalues.refresh_db(city='minsk', day='')
    cur_list_yesterday = getvalues.refresh_db(city='minsk', day=yesterday.strftime("%d-%m-%Y"))
    await getvalues.add_to_redis(cur_list_today, cur_list_yesterday)
    await dp.start_polling(bot)


commands.register(dp)

if __name__ == "__main__":
    asyncio.run(main())

