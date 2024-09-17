import typing

import sqlalchemy as sa
from sqlalchemy import orm


class Base(orm.DeclarativeBase):
    pass


METADATA: typing.Final = Base.metadata


class Message(Base):
    __tablename__ = "messages"

    id: orm.Mapped[typing.Annotated[int, orm.mapped_column(sa.BigInteger, primary_key=True)]]
    dialog_id: orm.Mapped[typing.Annotated[int, orm.mapped_column(sa.BigInteger, nullable=False)]]
    is_delivered: orm.Mapped[typing.Annotated[bool, orm.mapped_column(sa.Boolean, nullable=False)]]
    is_read: orm.Mapped[typing.Annotated[bool, orm.mapped_column(sa.Boolean, nullable=False)]]
    is_failed: orm.Mapped[typing.Annotated[bool, orm.mapped_column(sa.Boolean, nullable=False)]]
