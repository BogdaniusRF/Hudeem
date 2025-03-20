import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
#from redis import from_url
from app.user import user
from app.admin import admin
from app.database.models import async_main

#Redis
import redis.asyncio as aioredis
from aiogram.fsm.storage.redis import RedisStorage

#Postgres
from app.database.models import async_main



async def main():
    # REDIS ##
    redis = await aioredis.from_url(f'redis://localhost:6379/0')  # //localhost:6379/0 - ноль после "/0" - это БД под бот hudeem
    # REDIS ##
    
    load_dotenv()
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    #dp = Dispatcher() # - обычный диспетчер с внутренней памятью redis
    
    # REDIS ##
    dp = Dispatcher(storage=RedisStorage(redis))  # - диспетчер с памятью
    # REDIS ##

    dp.include_routers(user,admin)
    dp.startup.register(on_startup)
    await dp.start_polling(bot) # пришли ли какие то запросы или обновления


async def on_startup(dispatcher: Dispatcher):  # когда бот будет стартовать - всегда будут создаваться таблицы
    await async_main()  # когда бот будет стартовать - всегда будут создаваться таблицы


if __name__ == '__main__':
    try:
        asyncio.run(main())


    except KeyboardInterrupt:
        pass
