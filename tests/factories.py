from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from app import models


class MessageModelFactory(SQLAlchemyFactory[models.Message]):
    __model__ = models.Message
    id = None
