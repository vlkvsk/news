from aiogram.dispatcher.filters.state import State, StatesGroup

class post(StatesGroup):
    id = State()
    post = State()