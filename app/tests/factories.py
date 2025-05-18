
import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker
from sqlalchemy.orm import Session

from app.config.database import engine
from app.models import Activity, Building, Organization

session = Session(engine)
fake = Faker()


class ActivityFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Activity
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'

    title = factory.Faker('bs', locale='ru_RU')


class BuildingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Building
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'

    id = factory.Faker('uuid4')
    address = factory.Faker('address', locale='ru_RU')
    coordinates = factory.LazyFunction(lambda: f"POINT({fake.latitude()} {fake.longitude()})")


class OrganizationFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Organization
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'

    id = factory.Faker('uuid4')
    name = factory.Faker('company', locale='ru_RU')
    phone_numbers = factory.LazyFunction(lambda: list([fake.phone_number(), fake.phone_number()]))

    building = factory.SubFactory(BuildingFactory)
