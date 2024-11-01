from aiogram.dispatcher.filters.state import State, StatesGroup

class code(StatesGroup):
    q1 = State()

class get_word(StatesGroup):
    q1 = State()

class add_town(StatesGroup):
    town_text = State()

class add_region(StatesGroup):
    region_text = State()