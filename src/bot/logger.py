from loguru import logger
import aiosqlite
import datetime
from pytz import timezone


async def setup_logger_for_tg():
    
    logger.remove()
    logger.add(
        sink=log_to_sqlite,
        format='{message}',
        level='DEBUG',
        backtrace=True,
        diagnose=True
    )


async def log_to_sqlite(message):
    record = message.record
    level = record['level'].name
    log_message = record['message']

    msk_timezone = timezone('Europe/Moscow')
    current_time = datetime.datetime.now(msk_timezone).strftime('%Y-%m-%d %H:%M:%S')
    
    async with aiosqlite.connect('logs_bot.db') as db:
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS logs 
            (time TEXT, level TEXT, message TEXT)'''
        )
        await db.execute(
            'INSERT INTO logs (time, level, message) VALUES (?, ?, ?)',
            (current_time, level, log_message)
        )
        await db.commit()