
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Question, Answer


async def save_answer(
    session: AsyncSession,
    user_id: int,
    quiz_id: str,
    question_id: str,
    answer: str,
) -> str:
    result = await session.execute(
        select(Question).where(
            Question.quiz_id == quiz_id,
            Question.question_id == question_id,
        )
    )
    question = result.scalar_one_or_none()

    if question is None:
        question = Question(
            quiz_id=quiz_id,
            question_id=question_id,
        )
        session.add(question)

        try:
            await session.flush()
        except IntegrityError:
            await session.rollback()
            return "error"

    result = await session.execute(
        select(Answer.id).where(
            Answer.user_id == user_id,
            Answer.question_id == question.id,
        )
    )

    if result.scalar_one_or_none() is not None:
        await session.rollback()
        return "already_answered"

    session.add(
        Answer(
            user_id=user_id,
            question_id=question.id,
            answer=answer,
        )
    )
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        return "error"

    return "saved"

async def get_answers_by_quiz(
    session: AsyncSession,
    quiz_id: str,
) -> list[Answer]:
    """
    Получает список ответов для указанной викторины.

    Args:
        session: Асинхронная сессия SQLAlchemy.
        quiz_id: Идентификатор викторины.

    Returns:
        Список объектов Answer.
    """
    result = await session.scalars(
        select(Answer)
        .join(Question, Answer.question_id == Question.id)
        .where(Question.quiz_id == quiz_id)
    )

    return list(result.all())
