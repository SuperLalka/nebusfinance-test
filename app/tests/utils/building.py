
from faker import Faker
from sqlalchemy import Row
from sqlalchemy.orm import Session

from app.repository.building import BuildingRepository
from app.schemas.building import BuildingInput

fake = Faker()


async def create_building(
        db: Session,
        address: str = None,
) -> Row:
    return await BuildingRepository(db).create(
        BuildingInput(
            address=address or fake.address(),
            lat=fake.latitude(),
            long=fake.longitude()
        )
    )
