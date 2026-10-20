from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.database.requests import *
from app.services.statistics_service import get_question_statistics


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
                    text="⚒️ Сормовский",
                    callback_data="excursion:sormovsky",
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


async def get_correct_answer_keyboard(
        user_id: int,
        selected: int,
        is_last: bool = False,
        question = {},
) -> InlineKeyboardMarkup:
    correct = question["correct_answer"]
    quiz_id = question["id"][:-6]
    question_id = question["id"][-5:]
    answer = str(selected)
    result = await save_answer(
        user_id=user_id,
        answer=answer,
        quiz_id=quiz_id,
        question_id=question_id
    )
    if result == "error":
        raise RuntimeError("Не удалось сохранить ответ")


    other_answers = await get_question_statistics(quiz_id, question_id)
    all_answers = sum(other_answers.values())
    keyboard = [
    [
        InlineKeyboardButton(
            text=(
                f'{"✅ " if correct == index else ("🚫 " if selected == index else "")}'
                f'{int(100 * other_answers.get(str(index), 0) / all_answers) if all_answers else 0}% '
                f'{answer_text}'
            ),
            callback_data="quiz:ignore",
        )
    ]
    for index, answer_text in enumerate(question["answers"])
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

