from typing import AsyncGenerator, Annotated
from contextlib import asynccontextmanager
from datetime import datetime

from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from sqlalchemy import text, NullPool

from src.shared.config.settings import settings


DATABASE_PARAMS = {
    "pool_pre_ping": True,
    "pool_size": settings.POSTGRES_POOL_SIZE,
    "max_overflow": settings.POSTGRES_MAX_OVERFLOW
    }

if settings.MODE.lower() == "test":
    DATABASE_PARAMS = {
        "poolclass": NullPool,   
    }


engine = create_async_engine(
    settings.postgres_uri,
    **DATABASE_PARAMS
)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


created_at = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())"),
    ),
]
is_active = Annotated[bool, mapped_column(default=True, doc="Активность")] 