from aiogram.fsm.state import State, StatesGroup


class CardsState(StatesGroup):
    viewing_cards = State()