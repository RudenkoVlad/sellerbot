import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from keyboards.admin_kb import kb_admin, item_btn_admin
from keyboards.client_kb import kb_client, item_btn_client
from keyboards.catalog_kb import create_keyboard_catalog
from keyboards.cart_kb import cart_btn

from database import database as db

save_id = None


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    global save_id
    save_id = message.from_user.id

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
    global current_category_messages
    current_category_messages = {}

    await show_catalog(message)


async def show_catalog(message: types.Message):
    categories = await db.get_all_categories()

    if categories:
        keyboard = await create_keyboard_catalog(categories)
        await message.answer('Виберіть категорію, щоб побачити товар: ', reply_markup=keyboard)
    else:
        await message.answer('Немає доступних категорій')

item_data = {
    "item_id": None,
    "category_id": None
}


async def show_item(message: types.Message, item):
    global item_data
    item_data["item_id"] = item[0]
    item_data["category_id"] = item[1]

    # item_info = f"ID: {item[0]}\n"
    # item_info += f"Category: {item[1]}\n"
    item_info = f"Name: {item[2]}\n"
    item_info += f"Description: {item[3]}\n"
    item_info += f"Price: {item[4]}\n"
    # item_info += f"Photo: {item[5]}"

    keyboard = item_btn_admin if save_id == int(os.getenv('ADMIN_ID')) else item_btn_client

    if message.chat.id in current_category_messages:
        await bot.edit_message_media(chat_id=message.chat.id, message_id=current_category_messages[message.chat.id],
                                     media=types.InputMediaPhoto(media=item[5], caption=item_info),
                                     reply_markup=keyboard)
    else:
        sent_message = await bot.send_photo(chat_id=message.chat.id, photo=item[5], caption=item_info,
                                            reply_markup=keyboard)
        current_category_messages[message.chat.id] = sent_message.message_id


async def show_items_in_categories(message: types.Message, category: str):
    items = await db.get_items_by_category(category)

    if items:
        await show_item(message, items[0])
    else:
        if message.chat.id in current_category_messages:
            await bot.delete_message(message.chat.id,
                                     current_category_messages[message.chat.id])
            del current_category_messages[message.chat.id]
        # await message.answer('В цій категорії товарів не знайдено')


@dp.callback_query_handler(lambda query: query.data.isdigit())
async def show_category_items(callback_query: types.CallbackQuery):
    category = callback_query.data
    await show_items_in_categories(callback_query.message, category)


@dp.callback_query_handler(text=['previous_item', 'next_item'])
async def navigate_items(callback_query: types.CallbackQuery):
    # item_id = int(callback_query.message.caption.split('ID: ')[1].split('\n')[0])
    # category = callback_query.message.caption.split('Category: ')[1].split('\n')[0]
    items = await db.get_items_by_category( item_data["category_id"])

    current_index = next((index for index, item in enumerate(items) if item[0] == item_data["item_id"]), None)

    if current_index is not None:
        if callback_query.data == 'previous_item' and current_index > 0:
            await show_item(callback_query.message, items[current_index - 1])
        elif callback_query.data == 'next_item' and current_index < len(items) - 1:
            await show_item(callback_query.message, items[current_index + 1])


@dp.callback_query_handler(text='add_to_cart')
async def add_item_to_cart(callback_query: types.CallbackQuery):
    cart_items = await db.get_items_in_cart(save_id)

    if item_data["item_id"] in cart_items:
        await callback_query.answer('Товар вже знаходиться в кошику')
    else:
        await db.add_to_cart(save_id, item_data["item_id"])
        await callback_query.answer('Товар додано до кошика')


@dp.callback_query_handler(text='cancel')
async def cancel(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, "Операцію скасовано.")


# ----------------------------------------------------------------------------------------------------------------------
async def display_basket(message: types.Message):
    summa = 0
    cart_items = await db.get_items_in_cart(save_id)

    if not cart_items:
        await message.answer('Кошик пустий!')
    else:
        response = "Ваш кошик:\n"
        for item_id in cart_items:
            item = await db.get_item(item_id)
            response += f"ID: {item_id}, Назва: {item[2]}\nЦіна: {item[4]}\n\n"
            summa += int(item[4])
        response += f"Всього: {summa}"
        await message.answer(response, reply_markup=cart_btn)


@dp.message_handler(text='Кошик')
async def basket(message: types.Message):
    await display_basket(message)


@dp.callback_query_handler(text='clear_cart')
async def clear_cart(callback_query: types.CallbackQuery):
    await db.delete_items_from_cart(save_id)
    await callback_query.answer('Кошик очищено')


class DeleteItemFromCart(StatesGroup):
    item_id = State()


@dp.callback_query_handler(text='delete_item_from_cart')
async def delete_item_query(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Введіть ID товару, який ви хочете видалити з кошика:')
    await DeleteItemFromCart.item_id.set()


@dp.message_handler(state=DeleteItemFromCart.item_id)
async def delete_item(message: types.Message, state: FSMContext):
    item_id = int(message.text)
    await db.delete_item_from_cart(save_id, item_id)
    await message.answer(f'Товар з ID {item_id} був видалений з кошика')
    await state.finish()
    await display_basket(message)


@dp.callback_query_handler(text='to_pay')
async def to_pay(callback_query: types.CallbackQuery):
    await callback_query.answer('Оплата знаходиться в розробці')

# ----------------------------------------------------------------------------------------------------------------------


@dp.message_handler(text='Інфо')
async def info(message: types.Message):
    await message.answer('Автор бота: @BJLAD_IK')
