import random

from faker import Faker
from sqlalchemy.orm import Session

from app.repository.organization import OrganizationRepository
from app.schemas.organization import OrganizationInput, OrganizationUpdate
from app.tests.factories import BuildingFactory, OrganizationFactory
from app.tests.utils.organization import create_organization


async def test_create_organization(db: Session, faker: Faker, building: BuildingFactory) -> None:
    new_organization_data = {
        'name': faker.company(),
        'phone_numbers': [
            faker.phone_number(),
            faker.phone_number()
        ],
        'building_id': building.id,
    }

    organization_in = OrganizationInput(**new_organization_data)
    organization = await OrganizationRepository(db).create(organization_in)

    assert organization.name == new_organization_data['name']
    assert organization.building_id == new_organization_data['building_id']
    assert organization.phone_numbers == new_organization_data['phone_numbers']


async def test_exists_by_id_organization(db: Session, organization: OrganizationFactory) -> None:
    assert await OrganizationRepository(db).exists_by_id(organization.id)


async def test_is_exists_organization(db: Session, organization: OrganizationFactory) -> None:
    assert await OrganizationRepository(db).is_exists()


async def test_get_all_organizations(db: Session) -> None:
    organizations_num = random.randint(3, 6)
    [await create_organization(db) for _ in range(organizations_num)]

    organizations = await OrganizationRepository(db).get_all()
    assert len(organizations) == organizations_num


async def test_get_by_id_organization(db: Session, organization: OrganizationFactory) -> None:
    organization_obj = await OrganizationRepository(db).get_by_id(organization.id)

    assert organization_obj.id == organization.id
    assert organization_obj.name == organization.name


async def test_update_organization(db: Session, faker: Faker, building: BuildingFactory) -> None:
    organization = await create_organization(db)

    new_organization_data = {
        'name': faker.company(),
        'phone_numbers': [
            faker.phone_number(),
            faker.phone_number()
        ],
        'building_id': building.id,
    }
    organization_in = OrganizationUpdate(**new_organization_data)

    assert organization.name != organization_in.name
    assert organization.phone_numbers != organization_in.phone_numbers
    assert organization.building_id != organization_in.building_id

    await OrganizationRepository(db).update(organization, organization_in)

    assert organization.name == organization_in.name
    assert organization.phone_numbers == organization_in.phone_numbers
    assert organization.building_id == organization_in.building_id


async def test_delete_organization(db: Session) -> None:
    organization = await create_organization(db)
    await OrganizationRepository(db).delete(organization)

    assert not await OrganizationRepository(db).exists_by_id(organization.id)
