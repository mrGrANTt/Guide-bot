import pytest

from app.database.requests import save_answer
from app.services.statistics_service import get_question_statistics
from app.database.models import Base, Question, Answer


@pytest.mark.asyncio
async def test_get_question_statistics(session):
    """Возвращает количество ответов для каждого варианта."""
    await save_answer(session, 12345, "general", "q001", "a")
    await save_answer(session, 12346, "general", "q001", "b")
    await save_answer(session, 12347, "general", "q001", "b")
    await save_answer(session, 12348, "general", "q001", "c")

    stats = await get_question_statistics(
        session=session,
        quiz_id="general",
        question_id="q001",
    )

    assert stats == {
        "a": 1,
        "b": 2,
        "c": 1,
    }


@pytest.mark.asyncio
async def test_get_question_statistics_filters_question(session):
    """Не учитывает ответы на другие вопросы."""
    await save_answer(session, 12345, "general", "q001", "a")
    await save_answer(session, 12346, "general", "q001", "b")
    await save_answer(session, 12347, "general", "q002", "b")

    stats = await get_question_statistics(
        session=session,
        quiz_id="general",
        question_id="q001",
    )

    assert stats == {
        "a": 1,
        "b": 1,
    }


@pytest.mark.asyncio
async def test_get_question_statistics_filters_quiz(session):
    """Не учитывает ответы на вопросы из других викторин."""
    await save_answer(session, 12345, "general", "q001", "a")
    await save_answer(session, 12346, "history", "q001", "b")

    stats = await get_question_statistics(
        session=session,
        quiz_id="general",
        question_id="q001",
    )

    assert stats == {
        "a": 1,
    }


@pytest.mark.asyncio
async def test_get_question_statistics_no_answers(session):
    """Возвращает пустой словарь, если ответов нет."""
    stats = await get_question_statistics(
        session=session,
        quiz_id="general",
        question_id="q001",
    )

    assert stats == {}
