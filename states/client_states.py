from aiogram.dispatcher.filters.state import State, StatesGroup


class SearchPrice(StatesGroup):
    waiting_category = State()
    waiting_price_range = State()


class SearchName(StatesGroup):
    waiting_category = State()
    waiting_name = State()


class DeleteItemFromCart(StatesGroup):
    item_id = State()
