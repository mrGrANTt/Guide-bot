from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.quiz import get_excursion_keyboard
from app.handlers.start import send_main_menu

router = Router()


@router.callback_query(F.data == "menu:quizzes")
async def show_quizzes(callback: CallbackQuery) -> None:
    await callback.answer()

    if callback.message:
        await callback.message.answer(
            "🧭 Выбери экскурсию:",
            reply_markup=get_excursion_keyboard(),
        )


@router.callback_query(F.data == "menu:statistics")
async def show_statistics(callback: CallbackQuery) -> None:
    await callback.answer()

    if callback.message:
        await callback.message.answer(
            "📊 Статистика станет доступна после подключения базы данных."
        )


@router.callback_query(F.data == "menu:home")
async def show_home(callback: CallbackQuery) -> None:
    await callback.answer()

    if callback.message:
        await send_main_menu(callback.message)


@router.callback_query(F.data.startswith("excursion:"))
async def select_excursion(callback: CallbackQuery) -> None:
    await callback.answer()

    excursions = {
        "excursion:architecture": "🏛️ Архитектура",
        "excursion:painting": "🎨 Живопись",
        "excursion:cinema": "🎬 Кино",
    }

    excursion_name = excursions.get(callback.data)

    if callback.message and excursion_name:
        await callback.message.answer(
            f"Ты выбрал экскурсию «{excursion_name}»!\n\n"
            "🚧 Вопросы добавим на следующем этапе."
        )