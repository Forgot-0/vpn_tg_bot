import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from bot.handlers.users import router as user_router
from bot.handlers.subscriptions import router as sub_router
from bot.middlewares.mediator import MediatorMiddleware


async def main():
    

    bot: Bot = Bot(
        token='5208514073:AAE4tGvLhsCeWAaR1Cuv8C30YSScqvuyuXk',
        default=DefaultBotProperties(parse_mode='HTML'),
    )
    dp: Dispatcher = Dispatcher()

    dp.include_router(user_router)
    dp.include_router(sub_router)
    dp.update.middleware(MediatorMiddleware())

    
    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
   