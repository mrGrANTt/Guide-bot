import json
import random
from pathlib import Path


QUIZZES_DIR = Path(__file__).resolve().parents[2] / "data" / "quizzes"


def load_questions(category: str) -> list[dict]:
    file_path = QUIZZES_DIR / f"{category}.json"

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Файл категории не найден: {category}.json"
        )

    with file_path.open("r", encoding="utf-8") as file:
        questions = json.load(file)

    if not isinstance(questions, list):
        raise ValueError("Файл с вопросами должен содержать JSON-массив.")

    return questions


def select_random_questions(
    category: str,
    count: int = 3,
) -> list[dict]:
    questions = load_questions(category)

    if len(questions) < count:
        raise ValueError(
            f"В категории «{category}» недостаточно вопросов."
        )

    return random.sample(questions, count)