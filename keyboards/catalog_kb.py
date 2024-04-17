from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def create_keyboard_catalog(categories):
    keyboard = InlineKeyboardMarkup(row_width=3)

    for i in range(0, len(categories), 3):
        row = []
        for j in range(3):
            if i + j < len(categories):
                row.append(InlineKeyboardButton(text=categories[i + j][1], callback_data=str(categories[i + j][0])))
        keyboard.add(*row)
    return keyboard
