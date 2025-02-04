import logging
import typing

from sqlalchemy.ext import asyncio as sa

from app.settings import Settings


logger = logging.getLogger(__name__)


async def create_sa_engine(settings: Settings) -> typing.AsyncIterator[sa.AsyncEngine]:
    logger.debug("Initializing SQLAlchemy engine")
    engine = sa.create_async_engine(
        url=settings.db_dsn,
        echo=True,
        echo_pool=True,
        pool_size=settings.db_pool_size,
        pool_pre_ping=settings.db_pool_pre_ping,
        max_overflow=settings.db_max_overflow,
    )
    logger.debug("SQLAlchemy engine has been initialized")
    try:
        yield engine
    finally:
        await engine.dispose()
        logger.debug("SQLAlchemy engine has been cleaned up")


def create_session(engine: sa.AsyncEngine) -> sa.AsyncSession:
    return sa.AsyncSession(engine, expire_on_commit=False, autoflush=False)
