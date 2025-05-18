import random
import uuid

from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.repository.filters.organization import OrganizationFilter
from app.repository.organization import OrganizationRepository
from app.tests.factories import ActivityFactory, BuildingFactory
from app.tests.utils.organization import create_organization


async def test_get_all_organizations(client: TestClient, db: Session) -> None:
    organizations_num = random.randint(3, 6)
    [await create_organization(db) for _ in range(organizations_num)]

    response = client.get(f'{settings.API_V1_STR}/organizations/')
    assert response.status_code == 200

    content = response.json()
    assert len(content) == organizations_num


async def test_get_all_with_filter_organizations(db: Session, faker: Faker) -> None:
    control_activ = ActivityFactory.create()
    activities = [getattr(ActivityFactory.create(activity_id=control_activ.id), 'id') for _ in range(10)]

    coords_one = (53.900, 27.500)
    building_one = BuildingFactory.create(coordinates=f"POINT({coords_one[0]} {coords_one[1]})")
    coords_two = (54.100, 27.500)
    building_two = BuildingFactory.create(coordinates=f"POINT({coords_two[0]} {coords_two[1]})")
    coords_three = (54.300, 27.500)
    building_three = BuildingFactory.create(coordinates=f"POINT({coords_three[0]} {coords_three[1]})")

    control_org = await create_organization(
        db, building_id=building_one.id,
        activities=[activities[0], activities[1]]
    )
    await create_organization(
        db, building_id=building_two.id,
        activities=[activities[2], activities[3], activities[4]]
    )
    await create_organization(
        db, building_id=building_two.id,
        activities=[activities[3], activities[4], activities[5]]
    )
    await create_organization(
        db, building_id=building_three.id,
        activities=[activities[6], activities[7]]
    )

    # поиск организации по названию
    result = await OrganizationRepository(
        db,
        model_filter=OrganizationFilter(
            name=control_org.name,
        )
    ).get_all()
    assert len(result) == 1

    # список всех организаций находящихся в конкретном здании
    result = await OrganizationRepository(
        db,
        model_filter=OrganizationFilter(
            building_id=building_two.id,
        )
    ).get_all()
    assert len(result) == 2

    # список всех организаций, которые относятся к указанному виду деятельности
    result = await OrganizationRepository(
        db,
        model_filter=OrganizationFilter(
            activity_id=activities[3]
        )
    ).get_all()
    assert len(result) == 2

    # список всех организаций, которые относятся к указанной группе видов деятельности
    result = await OrganizationRepository(
        db,
        model_filter=OrganizationFilter(
            activity_group=control_activ.id
        )
    ).get_all()
    assert len(result) == 4

    # список организаций, которые находятся в заданном радиусе относительно указанной точки на карте
    result = await OrganizationRepository(
        db,
        model_filter=OrganizationFilter(
            within_radius_value=(f'POINT(53.880 27.500)', 100)
        )
    ).get_all()
    assert len(result) == 0

    result = await OrganizationRepository(
        db,
        model_filter=OrganizationFilter(
            within_radius_value=(f'POINT(53.880 27.500)', 5000)
        )
    ).get_all()
    assert len(result) == 1

    result = await OrganizationRepository(
        db,
        model_filter=OrganizationFilter(
            within_radius_value=(f'POINT(53.880 27.500)', 25000)
        )
    ).get_all()
    assert len(result) == 3

    result = await OrganizationRepository(
        db,
        model_filter=OrganizationFilter(
            within_radius_value=(f'POINT(53.880 27.500)', 50000)
        )
    ).get_all()
    assert len(result) == 4

    # список организаций, которые находятся в заданной прямоугольной области на карте
    rectangle_points = [
        '51.000 26.000',
        '51.000 28.000',
        '54.000 28.000',
        '54.000 26.000',
        '51.000 26.000',
    ]
    result = await OrganizationRepository(
        db,
        model_filter=OrganizationFilter(
            within_area_value=f"POLYGON(({','.join(rectangle_points)}))"
        )
    ).get_all()
    assert len(result) == 1

    rectangle_points = [
        '51.000 26.000',
        '51.000 28.000',
        '54.200 28.000',
        '54.200 26.000',
        '51.000 26.000',
    ]
    result = await OrganizationRepository(
        db,
        model_filter=OrganizationFilter(
            within_area_value=f"POLYGON(({','.join(rectangle_points)}))"
        )
    ).get_all()
    assert len(result) == 3


async def test_create_organization(client: TestClient, faker: Faker, db: Session) -> None:
    activities = [getattr(ActivityFactory.create(), 'id') for _ in range(6)]
    building = BuildingFactory.create()

    data = {
        'organization': {
            'name': faker.company(),
            'phone_numbers': [
                faker.phone_number(),
                faker.phone_number()
            ],
            'building_id': str(building.id),
        },
        'activities': faker.random_elements(activities, length=2, unique=True)
    }
    response = client.post(
        f'{settings.API_V1_STR}/organizations/',
        json=data,
    )
    assert response.status_code == 200

    content = response.json()
    assert 'id' in content
    assert content['name'] == data['organization']['name']
    assert content['phone_numbers'] == data['organization']['phone_numbers']
    assert content['building_id'] == data['organization']['building_id']

    assert await OrganizationRepository(db).exists_by_id(content['id'])


async def test_delete_organization(client: TestClient, db: Session) -> None:
    organization = await create_organization(db)
    response = client.delete(
        f'{settings.API_V1_STR}/organizations/{organization.id}',
    )
    assert response.status_code == 204

    assert not await OrganizationRepository(db).exists_by_id(organization.id)


async def test_delete_organization_not_found(client: TestClient) -> None:
    fake_organization_id = uuid.uuid4()
    response = client.delete(
        f'{settings.API_V1_STR}/organizations/{fake_organization_id}',
    )
    assert response.status_code == 404

    content = response.json()
    assert content['detail'] == 'Object not found'
