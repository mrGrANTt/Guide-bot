from pathlib import Path

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile, InputMediaPhoto

from app.keyboards.cards import (
    get_district_keyboard,
    get_card_keyboard,
)
from app.services.card_loader import load_cards
from app.states.cards_state import CardsState


router = Router()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CARDS_ASSETS_DIR = PROJECT_ROOT / "assets" / "questions"
REG_IMAGE = PROJECT_ROOT / "assets" / "select.png"

async def send_card(
    message: Message,
    state: FSMContext,
) -> None:
    data = await state.get_data()

    cards = data["cards"]
    card_index = data["card_index"]
    card = cards[card_index]

    text = (
        f"Карточка {card_index + 1} из {len(cards)}\n\n"
        f"<b>{card['title']}</b>\n\n"
        f"{card['text']}"
    )

    keyboard = get_card_keyboard()
    image_name = card.get("image")

    if image_name:
        image_path = CARDS_ASSETS_DIR / image_name

        if image_path.is_file():
            await message.edit_media(
                media=InputMediaPhoto(
                    media=FSInputFile(image_path),
                    caption=text,
                    parse_mode="HTML",
                ),
                reply_markup=keyboard,
            )
            return

    await message.edit_caption(
        caption=text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@router.callback_query(F.data == "menu:learn")
async def show_learn(callback: CallbackQuery) -> None:
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
            reply_markup=get_district_keyboard(),
        )
        await callback.message.delete()

@router.callback_query(F.data.startswith("cards:district:"))
async def select_district(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    district = callback.data.removeprefix("cards:district:")

    try:
        cards = load_cards(district)
    except (FileNotFoundError, ValueError) as error:
        if callback.message:
            await callback.message.answer(
                f"Не удалось загрузить карточки: {error}"
            )
        return

    if not cards:
        if callback.message:
            await callback.message.answer(
                "В этом районе пока нет карточек."
            )
        return

    await state.clear()
    await state.set_state(CardsState.viewing_cards)
    await state.update_data(
        district=district,
        district_name=district,
        cards=cards,
        card_index=0,
    )

    if callback.message:
        await send_card(callback.message, state)


@router.callback_query(
    F.data.in_({"cards:prev", "cards:next"})
)
async def navigate_cards(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if await state.get_state() != CardsState.viewing_cards.state:
        await callback.answer("Просмотр карточек завершён.")
        return

    data = await state.get_data()
    cards = data["cards"]
    card_index = data["card_index"]

    if callback.data == "cards:prev":
        new_index = card_index - 1
    else:
        new_index = card_index + 1

    if not 0 <= new_index < len(cards):
        message = (
            "Это первая карточка."
            if new_index < 0
            else "Это последняя карточка."
        )
        await callback.answer(message)
        return

    await callback.answer()

    await state.update_data(card_index=new_index)

    if callback.message:
        await send_card(callback.message, state)