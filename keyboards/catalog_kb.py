from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

catalog_list = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='Телевізори', callback_data='TV'),
                                                     InlineKeyboardButton(text='Телефони', callback_data='phone'),
                                                     InlineKeyboardButton(text='Планшети', callback_data='tablet'),
                                                     InlineKeyboardButton(text='Ноутбуки', callback_data='laptop'),
                                                     InlineKeyboardButton(text='Приставки', callback_data='console'),
                                                     InlineKeyboardButton(text='Монітори', callback_data='monitor'))


item_btn = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='<--', callback_data='previous_item'),
                                                 InlineKeyboardButton(text='В кошик', callback_data='add_to_cart'),
                                                 InlineKeyboardButton(text='-->', callback_data='next_item'))
