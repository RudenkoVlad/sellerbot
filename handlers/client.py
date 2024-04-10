import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from create_bot import dp, bot
from keyboards.admin_kb import kb_admin
from keyboards.client_kb import kb_client
from keyboards.catalog_kb import catalog_list, item_btn

from database import database as db


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.add_user(message.from_user.id)

    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вітаю, Ви увійшли як адмін!', reply_markup=kb_admin)
    else:
        await message.answer(
            f"Привіт, {message.from_user.first_name} ({message.from_user.id})! Вітаю в нашому магазині.",
            reply_markup=kb_client)


# ----------------------------------------------------------------------------------------------------------------------


@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await message.answer('Виберіть категорію, щоб побачити товари: ', reply_markup=catalog_list)





@dp.callback_query_handler(text='cancel')
async def cancel(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, "Операцію скасовано.")


# ----------------------------------------------------------------------------------------------------------------------


@dp.message_handler(text='Кошик')
async def basket(message: types.Message):
    await message.answer('Кошик пустий!')


# ----------------------------------------------------------------------------------------------------------------------


@dp.message_handler(text='Інфо')
async def info(message: types.Message):
    await message.answer('Автор бота: @BJLAD_IK')
