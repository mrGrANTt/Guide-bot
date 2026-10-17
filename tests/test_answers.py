import pytest
import pytest_asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from app.database.models import Base, Question, Answer
from app.database.requests import save_answer, get_answers_by_quiz, has_user_answered


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:"
    )

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    SessionFactory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

    async with SessionFactory() as db_session:
        yield db_session

    await engine.dispose()


@pytest.mark.asyncio
async def test_save_answer_creates_question(session):
    """Вопрос отсутствует в БД: создать вопрос и сохранить ответ."""

    result = await save_answer(
        session=session,
        user_id=12345,
        quiz_id="general",
        question_id="q001",
        answer="b",
    )

    assert result == "saved"

    questions = await session.execute(select(Question))
    questions = questions.scalars().all()

    answers = await session.execute(select(Answer))
    answers = answers.scalars().all()

    assert len(questions) == 1
    assert questions[0].quiz_id == "general"
    assert questions[0].question_id == "q001"

    assert len(answers) == 1
    assert answers[0].user_id == 12345
    assert answers[0].answer == "b"


@pytest.mark.asyncio
async def test_duplicate_answer_is_rejected(session):
    """Нельзя дважды ответить на один вопрос."""

    first = await save_answer(
        session, 12345, "general", "q001", "b"
    )

    second = await save_answer(
        session, 12345, "general", "q001", "a"
    )

    assert first == "saved"
    assert second == "already_answered"

    result = await session.execute(select(Answer))
    answers = result.scalars().all()

    assert len(answers) == 1
    assert answers[0].answer == "b"


@pytest.mark.asyncio
async def test_different_users_can_answer(session):
    """Разные пользователи могут отвечать на один вопрос."""

    first = await save_answer(
        session, 12345, "general", "q001", "b"
    )

    second = await save_answer(
        session, 67890, "general", "q001", "a"
    )

    assert first == "saved"
    assert second == "saved"

    result = await session.execute(select(Answer))
    answers = result.scalars().all()

    assert len(answers) == 2




@pytest.mark.asyncio
async def test_get_answers_by_quiz_returns_saved_answers(session):
    """Возвращаются все сохранённые ответы указанной викторины."""

    await save_answer(session, 12345, "general", "q001", "b")
    await save_answer(session, 67890, "general", "q001", "a")
    await save_answer(session, 12345, "general", "q002", "c")

    answers = await get_answers_by_quiz(
        session=session,
        quiz_id="general",
    )

    actual = set()

    for answer in answers:
        question = await session.get(
            Question,
            answer.question_id,
        )

        assert question is not None

        actual.add(
            (
                answer.user_id,
                question.question_id,
                answer.answer,
            )
        )

    expected = {
        (12345, "q001", "b"),
        (67890, "q001", "a"),
        (12345, "q002", "c"),
    }

    assert actual == expected


@pytest.mark.asyncio
async def test_get_answers_by_quiz_filters_other_quizzes(session):
    """Ответы других викторин не попадают в результат."""

    await save_answer(session, 12345, "general", "q001", "b")
    await save_answer(session, 12345, "science", "q001", "c")

    answers = await get_answers_by_quiz(
        session=session,
        quiz_id="general",
    )

    assert len(answers) == 1
    assert answers[0].user_id == 12345
    assert answers[0].answer == "b"

    question = await session.get(
        Question,
        answers[0].question_id,
    )

    assert question is not None
    assert question.question_id == "q001"
    assert question.quiz_id == "general"


@pytest.mark.asyncio
async def test_get_answers_by_quiz_returns_empty_list(session):
    """Если ответов нет, возвращается пустой список."""

    answers = await get_answers_by_quiz(
        session=session,
        quiz_id="unknown",
    )

    assert answers == []


@pytest.mark.asyncio
async def test_has_user_answered_returns_true(session):
    """Возвращает True, если пользователь уже ответил на вопрос."""
    await save_answer(session, 12345, "general", "q001", "a")

    result = await has_user_answered(
        session,
        user_id=12345,
        quiz_id="general",
        question_id="q001",
    )

    assert result is True


@pytest.mark.asyncio
async def test_has_user_answered_returns_false(session):
    """Возвращает False, если пользователь ещё не отвечал."""
    result = await has_user_answered(
        session,
        user_id=12345,
        quiz_id="general",
        question_id="q001",
    )

    assert result is False


@pytest.mark.asyncio
async def test_has_user_answered_different_question(session):
    """Ответ на другой вопрос не должен учитываться."""
    await save_answer(session, 12345, "general", "q001", "a")

    result = await has_user_answered(
        session,
        user_id=12345,
        quiz_id="general",
        question_id="q002",
    )

    assert result is False


@pytest.mark.asyncio
async def test_has_user_answered_different_user(session):
    """Ответ другого пользователя не должен учитываться."""
    await save_answer(session, 12345, "general", "q001", "a")

    result = await has_user_answered(
        session,
        user_id=67890,
        quiz_id="general",
        question_id="q001",
    )

    assert result is False


@pytest.mark.asyncio
async def test_has_user_answered_different_quiz(session):
    """Ответ на вопрос другой викторины не должен учитываться."""
    await save_answer(session, 12345, "general", "q001", "a")

    result = await has_user_answered(
        session,
        user_id=12345,
        quiz_id="history",
        question_id="q001",
    )

    assert result is False

