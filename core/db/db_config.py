import uuid
from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import config

async_engine = create_async_engine(
    config.DB_URL,
    pool_recycle=3600
)


async_sesison_factory = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sesison_factory() as session:
        yield session


Base = declarative_base()