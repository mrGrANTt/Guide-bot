from pathlib import Path

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from app.keyboards.menu import get_main_menu_keyboard

router = Router()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MENU_IMAGE = PROJECT_ROOT / "assets" / "menu.png"


async def send_main_menu(message: Message) -> None:
    if not MENU_IMAGE.is_file():
        await message.answer(
            "Не удалось найти изображение главного меню."
        )
        return

    photo = FSInputFile(MENU_IMAGE)

    await message.answer_photo(
        photo=photo,
        caption=(
            """Привет! Это «Бот Быстрый Нижний» — твой компактный путеводитель по искусству и архитектуре города.

Мы не будем грузить тебя скучными датами. Вместо этого мы покажем, как искусство Нижнего Новгорода на самом деле на нас влияет. За каждым зданием, памятником или скульптурой стоит конкретный замысел: как через архитектуру формировали образ города, внушали чувство гордости или причастности к истории.

Давай разберёмся, как город управляет нашим восприятием. Скорее выбирай формат: """
        ),
        reply_markup=get_main_menu_keyboard(),
    )


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await send_main_menu(message)
