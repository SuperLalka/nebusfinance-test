from typing import List, Iterable
from uuid import uuid4

from faker import Faker
from sqlalchemy import Row
from sqlalchemy.orm import Session

from app.repository.organization import OrganizationRepository
from app.schemas.organization import OrganizationInput
from app.tests.factories import BuildingFactory

fake = Faker()


async def create_organization(
        db: Session,
        name: str = None,
        phone_numbers: List[str] = None,
        building_id: uuid4 = None,
        activities: Iterable[int] = None
) -> Row:
    organization = await OrganizationRepository(db).create(
        OrganizationInput(
            name=name or fake.name(),
            phone_numbers=phone_numbers or list([fake.phone_number(), fake.phone_number()]),
            building_id=building_id or getattr(BuildingFactory.create(), 'id')
        )
    )

    if activities:
        for activity_id in activities:
            await OrganizationRepository(db).add_organization_activity(organization.id, activity_id)

    return organization
