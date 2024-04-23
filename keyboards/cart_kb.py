from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cart_btn = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Прибрати товар', callback_data='delete_item_from_cart'),
                                                 InlineKeyboardButton('Очистити кошик', callback_data='clear_cart'),
                                                 InlineKeyboardButton('Сплатити', callback_data='to_pay'))