from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

info_change_btn = InlineKeyboardMarkup().add(InlineKeyboardButton('Змінити інфо', callback_data='change_info'))