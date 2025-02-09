import pytest
from src.shared.config.settings import settings
from src.shared.database.base import get_session
from sqlalchemy import text


@pytest.fixture(scope="module")
async def session():
    async with get_session() as session:
        yield session
        # Очистка таблиц после выполнения тестов
        
    async with get_session() as session:
        tables = ['offices', 'geo', 'organizations', 'phones', 'works', 'categories']
        for table in tables:
            await session.execute(text(f'TRUNCATE TABLE {table} CASCADE'))
        await session.commit()
        