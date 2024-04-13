import os

from aiogram import types
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
current_category_messages = {}


@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await message.answer('Виберіть категорію, щоб побачити товари: ', reply_markup=catalog_list)


async def show_item(message: types.Message, item):
    item_info = f"ID: {item[0]}\n"
    item_info += f"Category: {item[1]}\n"
    item_info += f"Name: {item[2]}\n"
    item_info += f"Description: {item[3]}\n"
    item_info += f"Price: {item[4]}\n"
    item_info += f"Photo: {item[5]}"

    if message.chat.id in current_category_messages:
        await bot.edit_message_media(chat_id=message.chat.id, message_id=current_category_messages[message.chat.id],
                                     media=types.InputMediaPhoto(media=item[5], caption=item_info),
                                     reply_markup=item_btn)
    else:
        sent_message = await bot.send_photo(chat_id=message.chat.id, photo=item[5], caption=item_info,
                                            reply_markup=item_btn)
        current_category_messages[message.chat.id] = sent_message.message_id


@dp.callback_query_handler(lambda query: query.data in ['TV', 'phone', 'tablet', 'laptop', 'console', 'monitor'])
async def show_category_items(callback_query: types.CallbackQuery):
    category = callback_query.data
    items = await db.get_items_by_category(category)

    if items:
        await show_item(callback_query.message, items[0])
    else:
        await bot.send_message(callback_query.from_user.id, "No items found in this category.")


@dp.callback_query_handler(text=['previous_item', 'next_item'])
async def navigate_items(callback_query: types.CallbackQuery):
    item_id = int(callback_query.message.caption.split('ID: ')[1].split('\n')[0])
    category = callback_query.message.caption.split('Category: ')[1].split('\n')[0]
    items = await db.get_items_by_category(category)

    current_index = next((index for index, item in enumerate(items) if item[0] == item_id), None)

    if current_index is not None:
        if callback_query.data == 'previous_item' and current_index > 0:
            await show_item(callback_query.message, items[current_index - 1])
        elif callback_query.data == 'next_item' and current_index < len(items) - 1:
            await show_item(callback_query.message, items[current_index + 1])


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
