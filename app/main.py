import asyncio

from aiogram import Bot, Dispatcher
from punq import Container

from bot.handlers.users import router as user_router
from bot.handlers.subscriptions import router as sub_router
from bot.handlers.servers import router as server_router
from bot.middlewares.mediator import MediatorMiddleware
from infra.depends.init import init_container


async def init_bot():


    container: Container = init_container()

    bot: Bot = container.resolve(Bot)
    
    dp: Dispatcher = Dispatcher()
    dp.include_router(user_router)
    dp.include_router(sub_router)
    dp.include_router(server_router)

    dp.update.middleware(MediatorMiddleware())
    

    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(init_bot())
