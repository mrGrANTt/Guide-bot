from pathlib import Path
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from app.keyboards.quiz import get_excursion_keyboard
from app.handlers.start import send_main_menu
from app.services.quiz_loader import select_random_questions
from app.handlers.quiz import send_question
from app.states.quiz_state import QuizState

router = Router()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REG_IMAGE = PROJECT_ROOT / "assets" / "select.png"

@router.callback_query(F.data == "menu:quizzes")
async def show_quizzes(callback: CallbackQuery) -> None:
    await callback.answer()

    if not REG_IMAGE.is_file():
        await callback.message.answer(
            "Не удалось найти изображение выбора района."
        )
        return

    photo = FSInputFile(REG_IMAGE)

    if callback.message:
        await callback.message.answer_photo(
            photo=photo,
            caption="📚 Выбери район Нижнего Новгорода:",
            reply_markup=get_excursion_keyboard(),
        )


@router.callback_query(F.data == "menu:home")
async def show_home(callback: CallbackQuery) -> None:
    await callback.answer()

    if callback.message:
        await send_main_menu(callback.message)


@router.callback_query(F.data.startswith("excursion:"))
async def select_excursion(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    category = callback.data.removeprefix("excursion:")

    try:
        questions = select_random_questions(category, count=3)
    except (FileNotFoundError, ValueError) as error:
        if callback.message:
            await callback.message.answer(
                f"Не удалось начать опрос: {error}"
            )
        return

    await state.clear()
    await state.set_state(QuizState.answering)
    await state.update_data(
        category=category,
        questions=questions,
        question_index=0,
    )

    if callback.message:
        await send_question(callback.message, state)
