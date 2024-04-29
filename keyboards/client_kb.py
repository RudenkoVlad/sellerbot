from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add('Підбір товарів').add('Каталог').add('Кошик').add('Інфо')


item_btn_client = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='<--', callback_data='previous_item'),
                                                        InlineKeyboardButton(text='В кошик', callback_data='add_to_cart'),
                                                        InlineKeyboardButton(text='-->', callback_data='next_item'))