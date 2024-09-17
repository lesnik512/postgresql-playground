import asyncio
import typing

import sqlalchemy as sa

from app import ioc, models
from tests import factories


if typing.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def update_message(message_id: int, updates: dict[str, typing.Any]) -> None:
    session: AsyncSession = await ioc.IOCContainer.session()
    async with session:
        await session.execute(sa.update(models.Message).where(models.Message.id == message_id).values(**updates))
        await session.commit()


async def test_concurrent_updates() -> None:
    session = await ioc.IOCContainer.session()
    async with session:
        factories.MessageModelFactory.__async_session__ = session
        dialog_id = 999
        messages = await factories.MessageModelFactory.create_batch_async(
            size=10,
            dialog_id=dialog_id,
            is_delivered=False,
            is_read=False,
            is_failed=False,
        )

    async with asyncio.TaskGroup() as tg:
        for message in messages:
            tg.create_task(update_message(message.id, {"is_delivered": True}))
            tg.create_task(update_message(message.id, {"is_read": True}))
            tg.create_task(update_message(message.id, {"is_failed": True}))

    session: AsyncSession = await ioc.IOCContainer.session()
    async with session:
        result = await session.scalars(sa.select(models.Message).where(models.Message.dialog_id == dialog_id))
        messages_in_db = result.all()
        assert all(x.is_delivered and x.is_read and x.is_failed for x in messages_in_db)
