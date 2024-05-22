from aiogram.types import ReplyKeyboardMarkup

products_kb = ReplyKeyboardMarkup(resize_keyboard=True)
products_kb.add('Підбір товарів по ціні').add('Пошук по назві').add('Каталог').add('Повернутися назад')