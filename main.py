from aiogram.utils import executor
from create_bot import dp
from handlers import client, other, admin
from database import database as db


async def on_startup(_):
    await db.db_start()
    try:
        print('Бот почав працювати!')
    except Exception as e:
        print(f'Помилка при запуску бота: {e}')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
