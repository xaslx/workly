from loguru import logger
import aiosqlite
import datetime
from pytz import timezone


async def log_to_sqlite(message):

    record = message.record
    level = record['level'].name
    log_message = record['message']

    msk_timezone = timezone('Europe/Moscow')
    current_time = datetime.datetime.now(msk_timezone).strftime('%Y-%m-%d %H:%M:%S')
    
    async with aiosqlite.connect('logs.db') as db:
        await db.execute(
            'CREATE TABLE IF NOT EXISTS logs (time TEXT, level TEXT, message TEXT)'
        )
        await db.execute(
            'INSERT INTO logs (time, level, message) VALUES (?, ?, ?)',
            (current_time, level, log_message)
        )
        await db.commit()

logger.add(log_to_sqlite, format='{message}', enqueue=True, serialize=True)