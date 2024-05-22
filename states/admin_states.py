from aiogram.dispatcher.filters.state import State, StatesGroup


class ManagerCategories(StatesGroup):
    adding = State()
    deleting = State()


class NewOrder(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()


class BotMailing(StatesGroup):
    text = State()
    state = State()
    photo = State()


class ChangeInfoText(StatesGroup):
    new_info_text = State()
