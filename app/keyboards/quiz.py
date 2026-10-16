from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_excursion_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏛️ Нижегородский",
                    callback_data="excursion:nizhegorodsky",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏭 Автозаводской",
                    callback_data="excursion:avtozavodsky",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏩 Канавинский",
                    callback_data="excursion:kanavinsky",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚒️ Советский",
                    callback_data="excursion:sovetsky",
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

def get_answer_keyboard(
    answers: list[str],
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=answer,
                    callback_data=f"quiz:answer:{index}",
                )
            ]
            for index, answer in enumerate(answers)
        ]
    )


def get_correct_answer_keyboard(
        answers: list[str],
        correct: int,
        selected: int,
        is_last: bool = False,
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=('✅ ' if correct == index else ('🚫 ' if selected == index else '')) + answer,
                callback_data="quiz:ignore",
            )
        ]
        for index, answer in enumerate(answers)
    ]

    keyboard.append([
        InlineKeyboardButton(
            text=(
                "🏁 Завершить викторину"
                if is_last
                else "➡️ Следующий вопрос"
            ),
            callback_data="quiz:next"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

