from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_district_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏛️ Нижегородский",
                    callback_data="cards:district:nizhegorodsky",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏭 Автозаводской",
                    callback_data="cards:district:avtozavodsky",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏩 Канавинский",
                    callback_data="cards:district:kanavinsky",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚒️ Сормовский",
                    callback_data="cards:district:sormovsky",
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


def get_card_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="cards:prev",
                ),
                InlineKeyboardButton(
                    text="➡️ Вперёд",
                    callback_data="cards:next",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Главное меню",
                    callback_data="menu:home",
                )
            ],
        ]
    )