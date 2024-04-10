from aiogram import types
from create_bot import dp


@dp.message_handler()
async def cmd_end(message: types.Message):
    await message.reply('Я тебе не розумію!')
