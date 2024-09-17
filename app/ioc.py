from that_depends import BaseContainer, providers

from app.resources.db import create_sa_engine, create_session
from app.settings import Settings


class IOCContainer(BaseContainer):
    settings = providers.Singleton(Settings)

    database_engine = providers.Resource(create_sa_engine, settings=settings.cast)
    session = providers.Factory(create_session, engine=database_engine.cast)
