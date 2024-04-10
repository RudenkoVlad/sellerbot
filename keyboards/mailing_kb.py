from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_mailing = InlineKeyboardMarkup(row_width=2)
kb_mailing.add(InlineKeyboardButton(text='Додати фото', callback_data='add_photo'),
               InlineKeyboardButton(text='Далі', callback_data='next'),
               InlineKeyboardButton(text='Відмінити', callback_data='cancel'))

btn_next_and_cancel = InlineKeyboardMarkup(row_width=2)
btn_next_and_cancel.add(InlineKeyboardButton(text='Далі', callback_data='next'),
                        InlineKeyboardButton(text='Відміна', callback_data='cancel'))

btn_cancel = InlineKeyboardMarkup(row_width=2)
btn_cancel.add(InlineKeyboardButton(text='Відмінити', callback_data='cancel'))