from pathlib import Path

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
    FSInputFile,
)

from app.keyboards.quiz import (
    get_answer_keyboard,
    get_correct_answer_keyboard,
    get_excursion_keyboard
)
from app.states.quiz_state import QuizState


router = Router()

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"


async def send_question(
    message: Message,
    state: FSMContext,
) -> None:
    data = await state.get_data()

    questions = data["questions"]
    question_index = data["question_index"]
    question = questions[question_index]

    question_number = question_index + 1
    text = (
        f"Вопрос {question_number}\n\n"
        f"{question['question']}"
    )

    keyboard = get_answer_keyboard(question["answers"])

    image_path = ASSETS_DIR / f"question_{question_number}.png"

    if image_path.is_file():
        await message.answer_photo(
            photo=FSInputFile(image_path),
            caption=text,
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            text,
            reply_markup=keyboard,
        )


@router.callback_query(F.data.startswith("quiz:ignore"))
async def ignore_input(
    callback: CallbackQuery,
) -> None:
    await callback.answer()



@router.callback_query(F.data.startswith("quiz:answer:"))
async def check_answer(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    if await state.get_state() != QuizState.answering.state:
        return

    data = await state.get_data()

    questions = data["questions"]
    question_index = data["question_index"]
    question = questions[question_index]

    answer_index = int(callback.data.rsplit(":", 1)[1])
    answers = question["answers"]
    correct = question["correct_answer"]

    if not 0 <= answer_index < len(answers):
        return

    await state.update_data(selected_answer=answer_index)

    keyboard = get_correct_answer_keyboard(
        answers=answers,
        correct=correct,
        selected=answer_index,
        is_last=question_index == len(questions) - 1,
    )

    result_text = (
        f"Правильный ответ: {answers[correct]}"
    )

    explanation = question.get("explanation", "")
    fact_text = f"\n\n💡 Факт: {explanation}" if explanation else ""

    text = (
        f"Вопрос {question_index + 1}\n\n"
        f"{question['question']}\n\n"
        f"{result_text}"
        f"{fact_text}"
    )

    if callback.message:
        answer_image_name = question.get("answer_image")
        answer_image_path = (
            ASSETS_DIR / 'questions' / answer_image_name
            if answer_image_name
            else None
        )

        if answer_image_path and answer_image_path.is_file():
            await callback.message.answer_photo(
                photo=FSInputFile(answer_image_path),
                caption=text,
                reply_markup=keyboard,
            )

            await callback.message.delete()

        elif callback.message.caption is not None:
            await callback.message.edit_caption(
                caption=text,
                reply_markup=keyboard,
            )

        else:
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard,
            )


@router.callback_query(F.data == "quiz:next")
async def next_question(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    if await state.get_state() != QuizState.answering.state:
        return

    data = await state.get_data()

    # Переход разрешён только после ответа
    if data.get("selected_answer") is None:
        return

    questions = data["questions"]
    question_index = data["question_index"]

    if question_index + 1 >= len(questions):
        await state.clear()

        if callback.message:
            await callback.message.answer(
                "🏁 Викторина завершена!\n\n"
                "Выбирай следующий район:",
                reply_markup=get_excursion_keyboard(),
            )
            await callback.message.delete()

        return

    next_index = question_index + 1

    await state.update_data(
        question_index=next_index,
        selected_answer=None,
    )

    if callback.message:
        await send_question(callback.message, state)
        await callback.message.delete()