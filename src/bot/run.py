from aiogram import Bot, Dispatcher
from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import setup_dishka
from src.bot.ioc import BotProvider
import asyncio
from src.config import Config
from src.bot.handlers.users.main import router as main_router
from src.bot.logger import setup_logger_for_tg, logger

async def main() -> None:
    
    config = Config()
    await setup_logger_for_tg()

    bot_container: AsyncContainer = make_async_container(
        BotProvider(), context={Config: config}
    )
    dp: Dispatcher = await bot_container.get(Dispatcher)
    bot: Bot = await bot_container.get(Bot)
    dp.include_router(router=main_router)
    setup_dishka(router=dp, container=bot_container)
    
    logger.info('Бот запущен')

    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    asyncio.run(main())