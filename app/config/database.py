
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

from .settings import settings

engine = create_engine(settings.POSTGRES_CONNECTION_STRING)

Base = declarative_base()


def init_db(session: Session) -> None:
    Base.metadata.create_all(engine)


def drop_db(session: Session) -> None:
    Base.metadata.drop_all(engine)
