from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_excursion_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏛️ Архитектура",
                    callback_data="excursion:architecture",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎨 Живопись",
                    callback_data="excursion:painting",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎬 Кино",
                    callback_data="excursion:cinema",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Главное меню",
                    callback_data="menu:home",
                )
            ],
        ]
    )


def get_excursion_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Выбрать другую экскурсию",
                    callback_data="menu:quizzes",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Главное меню",
                    callback_data="menu:home",
                )
            ],
        ]
    )
