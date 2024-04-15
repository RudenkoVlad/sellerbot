from aiogram.types import ReplyKeyboardMarkup

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin.add('Каталог').add('Кошик').add('Інфо').add('Панель адміністратора')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
admin_panel.row('Додати категорію', 'Видалити категорію').row('Додати товар', 'Видалити товар').add(
    'Зробити розсилку').add('Повернутися назад')
