from aiogram.fsm.state import State, StatesGroup


class Chat(StatesGroup):
    name = State()
    number = State()
    location = State()
    text=State()
    wait = State()