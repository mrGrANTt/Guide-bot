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
            "👋 Добро пожаловать в мир искусства!\n\n"
            "Здесь ты можешь проходить интерактивные "
            "экскурсии, проверять свои знания и узнавать "
            "интересные факты о влиянии искусства на человека.\n\n"
            "Выбирай викторину или изучи карточки!"
        ),
        reply_markup=get_main_menu_keyboard(),
    )


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await send_main_menu(message)
