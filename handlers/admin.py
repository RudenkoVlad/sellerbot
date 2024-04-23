from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import os
from create_bot import dp
from handlers.client import show_items_in_categories, item_data
from keyboards.admin_kb import admin_panel, kb_admin
from keyboards.catalog_kb import create_keyboard_catalog
from aiogram.dispatcher.filters import Text
from database import database as db
from keyboards.mailing_kb import kb_mailing, btn_next_and_cancel, btn_cancel
from asyncio import sleep


@dp.message_handler(text='Панель адміністратора')
async def admin_btn(message: types.Message):

    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Що потрібно зробити адмін?', reply_markup=admin_panel)
    else:
        await message.reply('Вам не доступна панель адміністрування')
    # print(item_id)
    # print(category_id)


# ----------------------------------------------------------------------------------------------------------------------
class ManagerCategories(StatesGroup):
    adding = State()
    deleting = State()


@dp.message_handler(text='Додати категорію')
async def add_category(message: types.Message):
    await ManagerCategories.adding.set()
    await message.reply('Введіть назву нової категорії: ')


@dp.message_handler(text='Видалити категорію')
async def delete_category(message: types.Message):
    await ManagerCategories.deleting.set()
    categories = await db.get_all_categories()
    keyboard = await create_keyboard_catalog(categories)
    await message.answer('Виберіть категорію, яку потрібно видалити: ', reply_markup=keyboard)


@dp.message_handler(state=ManagerCategories.adding)
async def process_add_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category_name'] = message.text
    await db.add_category(data['category_name'])
    categories = await db.get_all_categories()
    keyboard = await create_keyboard_catalog(categories)
    await message.answer('Категорія успішно додана. Тепер каталог виглядає так: ', reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(lambda callback_query: True, state=ManagerCategories.deleting)
async def process_delete_category_callback(callback_query: types.CallbackQuery, state: FSMContext):
    category_id_del = callback_query.data
    await db.delete_categories(category_id_del)
    categories = await db.get_all_categories()
    keyboard = await create_keyboard_catalog(categories)
    await callback_query.message.answer('Категорія успішно видалена. Тепер каталог виглядає так:', reply_markup=keyboard)
    await state.finish()

# ----------------------------------------------------------------------------------------------------------------------


class NewOrder(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()


@dp.message_handler(text='Додати товар')
async def add_item(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await NewOrder.type.set()
        categories = await db.get_all_categories()
        keyboard = await create_keyboard_catalog(categories)
        await message.answer('Виберіть до якої категорії належить ваш товар: ', reply_markup=keyboard)
    else:
        await message.reply('Додавати товар може тільки адміністратор')


@dp.message_handler(state="*", commands='відмінити')
@dp.message_handler(Text(equals='відмінити', ignore_case=True), state="*")
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Ок")


@dp.callback_query_handler(state=NewOrder.type)
async def add_item_type(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = call.data
    await call.message.answer('Напишіть назву товару')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.name)
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Опишіть товар')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer('Задайте ціну товара')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.price)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Відправте фото товара')
    await NewOrder.next()


@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    await message.reply('Це не фото!')


@dp.message_handler(content_types=['photo'], state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        item_info = f"Item category: {data['category']}\n"
        item_info += f"Item Name: {data['name']}\n"
        item_info += f"Item Description: {data['desc']}\n"
        item_info += f"Item Price: {data['price']}\n"
        item_info += f"Item Photo: {data['photo']}"

    await db.add_item(state)
    await message.answer(f'Товар успішно створений!\n\n{item_info}', reply_markup=admin_panel)
    await state.finish()

# ----------------------------------------------------------------------------------------------------------------------


@dp.callback_query_handler(text='delete_item')
async def delete_item_callback(callback_query: types.CallbackQuery):
    if callback_query.from_user.id == int(os.getenv('ADMIN_ID')):
        # item_id = int(callback_query.message.caption.split('ID: ')[1].split('\n')[0])
        await db.delete_item(item_data["item_id"])

        # if callback_query.message.chat.id in current_category_messages:
        #     await bot.delete_message(callback_query.message.chat.id,
        #                              current_category_messages[callback_query.message.chat.id])
        #     del current_category_messages[callback_query.message.chat.id]

        # category = callback_query.message.caption.split('Category: ')[1].split('\n')[0]

        await show_items_in_categories(callback_query.message, item_data["category_id"])
    else:
        await callback_query.answer('Вам не доступне видалення товарів')


# ----------------------------------------------------------------------------------------------------------------------
class BotMailing(StatesGroup):
    text = State()
    state = State()
    photo = State()


@dp.message_handler(text='Зробити розсилку')
async def start_mailing(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Введіть текст розсилки:')
        await BotMailing.text.set()
    else:
        await message.reply('Вам не доступна розсилка')


@dp.message_handler(state=BotMailing.text)
async def mailing_text(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(text=answer)
    await message.answer(text=answer, reply_markup=kb_mailing)
    await BotMailing.state.set()


@dp.callback_query_handler(text='next', state=BotMailing.state)
async def start(call: types.CallbackQuery, state: FSMContext):
    users = await db.get_user()
    data = await state.get_data()
    text = data.get('text')
    await state.finish()

    for user_id, active_status in users:
        # if user == 539544748:  # !!!
        try:
            if active_status != 1:
                await db.set_active(user_id, 1)
            await dp.bot.send_message(chat_id=user_id, text=text)
            await sleep(0.33)
        except:
            await db.set_active(user_id, 0)

    await call.message.answer('Розсилка виконана.', reply_markup=admin_panel)


@dp.callback_query_handler(text='add_photo', state=BotMailing.state)
async def add_photo(call: types.CallbackQuery):
    await call.message.answer('Відправте фото')
    await BotMailing.photo.set()


@dp.message_handler(state=BotMailing.photo, content_types=types.ContentType.PHOTO)
async def mailing_text(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await message.answer_photo(photo=photo, caption=text, reply_markup=btn_next_and_cancel)


@dp.callback_query_handler(text='next', state=BotMailing.photo)
async def start(call: types.CallbackQuery, state: FSMContext):
    users = await db.get_user()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await state.finish()

    for user_id, active_status in users:
        # if user == 539544748:  # !!!
        try:
            if active_status != 1:
                await db.set_active(user_id, 1)  # Змінити статус активності на 1
            await dp.bot.send_photo(chat_id=user_id, photo=photo, caption=text)
            await sleep(0.33)
        except:
            await db.set_active(user_id, 0)

    await call.message.answer('Розсилка виконана.', reply_markup=admin_panel)


@dp.message_handler(state=BotMailing.photo)
async def no_photo(message: types.Message):
    await message.answer_photo('Відправте фото!!!', reply_markup=btn_cancel)


@dp.callback_query_handler(text='cancel', state=[BotMailing.text, BotMailing.photo, BotMailing.state])
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Розсилка скасована.', reply_markup=admin_panel)


# ----------------------------------------------------------------------------------------------------------------------


@dp.message_handler(text='Повернутися назад')
async def back_to_kb_admin(message: types.Message):
    await message.answer('Повернення до головної клавіатури', reply_markup=kb_admin)
