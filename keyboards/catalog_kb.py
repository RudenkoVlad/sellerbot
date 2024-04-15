from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import database as db


# async def show_catalog(message: types.Message):
#     categories = await db.get_all_categories()
#     if categories:
#         keyboard = InlineKeyboardMarkup(row_width=3)
#         for category in categories:
#             keyboard.add(InlineKeyboardButton(text=category[1], callback_data=str(category[0])))
#         await message.answer('Виберіть категорію:', reply_markup=keyboard)
#     else:
#         await message.answer('Немає доступних категорій.')


async def show_catalog(message: types.Message):
    categories = await db.get_all_categories()
    if categories:
        keyboard = InlineKeyboardMarkup(row_width=3)
        for i in range(0, len(categories), 3):
            row = []
            for j in range(3):
                if i + j < len(categories):
                    row.append(InlineKeyboardButton(text=categories[i + j][1], callback_data=str(categories[i + j][0])))
            keyboard.add(*row)
        await message.answer('Виберіть категорію:', reply_markup=keyboard)
    else:
        await message.answer('Немає доступних категорій.')


item_btn = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='<--', callback_data='previous_item'),
                                                 InlineKeyboardButton(text='В кошик', callback_data='add_to_cart'),
                                                 InlineKeyboardButton(text='-->', callback_data='next_item'))

manager_categories_buttons = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text='Додати категорію', callback_data='add_category'),
    InlineKeyboardButton(text='Видалити категорію', callback_data='delete_category'))