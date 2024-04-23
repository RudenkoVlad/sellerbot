from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin.add('Каталог').add('Кошик').add('Інфо').add('Панель адміністратора')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
admin_panel.row('Додати категорію', 'Видалити категорію').row('Додати товар', 'Видалити товар').add(
    'Зробити розсилку').add('Повернутися назад')

item_btn_admin = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text='<--', callback_data='previous_item'),
                                                       InlineKeyboardButton(text='В кошик', callback_data='add_to_cart'),
                                                       InlineKeyboardButton(text='-->', callback_data='next_item'),
                                                       InlineKeyboardButton(text='Видалити товар', callback_data='delete_item'))