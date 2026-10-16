import pytest
import pytest_asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from app.database.models import Base, Question, Answer
from app.database.requests import save_answer


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
