import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from app.database.models import Base


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
