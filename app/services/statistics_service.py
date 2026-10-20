# Расчёт статистики ответов и результатов.
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Base, Question, Answer


async def get_question_statistics(
    session: AsyncSession,
    quiz_id: str,
    question_id: str,
) -> dict[str, int]:
    """
    Получает статистику ответов на конкретный вопрос.

    Args:
        session: Асинхронная сессия SQLAlchemy.
        quiz_id: Идентификатор викторины.
        question_id: Идентификатор вопроса.

    Returns:
        Словарь с количеством пользователей для каждого варианта ответа.
    """
    result = await session.execute(
        select(
            Answer.answer,
            func.count(Answer.id),
        )
        .join(Question, Answer.question_id == Question.id)
        .where(
            Question.quiz_id == quiz_id,
            Question.question_id == question_id,
        )
        .group_by(Answer.answer)
    )

    return {
        answer: count
        for answer, count in result.all()
    }
