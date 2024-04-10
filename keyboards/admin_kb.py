from aiogram.types import ReplyKeyboardMarkup

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin.add('Каталог').add('Кошик').add('Інфо').add('Панель адміністратора')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Додати товар').add('Видалити товар').add('Зробити розсилку').add('Повернутися назад')