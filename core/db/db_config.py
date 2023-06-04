import uuid
from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session
from sqlalchemy.orm import declarative_base

from core.config import config

async_engine = create_async_engine(
    config.DB_URL,
    echo=True,
    pool_recycle=3600
)


async_sesison_factory = async_sessionmaker(async_engine)

session_factory: async_scoped_session = async_scoped_session(
    async_sesison_factory, scopefunc=current_task
)

async def get_async_session():
    async with session_factory() as session:
        session_id = str(uuid.uuid4())
        session.bind = async_engine.execution_options(
            stream_results=True
        ).params(session_id=session_id)
        yield session


Base = declarative_base()

Base.metadata.create_all(async_engine)