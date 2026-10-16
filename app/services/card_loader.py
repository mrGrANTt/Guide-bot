import json
from pathlib import Path


CARDS_DIR = Path(__file__).resolve().parents[2] / "data" / "cards"


def load_cards(district: str) -> list[dict]:
    file_path = CARDS_DIR / f"{district}.json"

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Файл карточек не найден: {file_path.name}"
        )

    with file_path.open("r", encoding="utf-8") as file:
        cards = json.load(file)

    if not isinstance(cards, list):
        raise ValueError("Файл карточек должен содержать JSON-массив.")

    for card in cards:
        if not isinstance(card, dict):
            raise ValueError("Каждая карточка должна быть объектом JSON.")

        for field in ("title", "text"):
            if not isinstance(card.get(field), str):
                raise ValueError(
                    f"В карточке отсутствует текстовое поле «{field}»."
                )

    return cards