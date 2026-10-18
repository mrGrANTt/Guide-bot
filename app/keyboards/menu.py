from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎯 Пройти викторину",
                    callback_data="menu:quizzes",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧠 Изучить карточки",
                    callback_data="menu:learn",
                )
            ],
        ]
    )
