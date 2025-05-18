from typing import Generator

import pytest
from fastapi.testclient import TestClient
from pytest_factoryboy import register
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.config.database import engine, init_db, drop_db
from app.main import app
from .factories import ActivityFactory, BuildingFactory, OrganizationFactory
from ..models import Building, Organization


@pytest.fixture(scope="session", autouse=True)
def db_init() -> None:
    with Session(engine) as session:
        init_db(session)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

        statement = delete(Organization)
        session.execute(statement)
        statement = delete(Building)
        session.execute(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


register(ActivityFactory)
register(BuildingFactory)
register(OrganizationFactory)
