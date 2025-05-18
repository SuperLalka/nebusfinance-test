import random
import re
import uuid

from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.repository.building import BuildingRepository
from app.tests.factories import BuildingFactory


async def test_get_all_buildings(client: TestClient, db: Session) -> None:
    buildings_num = random.randint(3, 6)
    [BuildingFactory.create() for _ in range(buildings_num)]

    response = client.get(f"{settings.API_V1_STR}/buildings/")
    assert response.status_code == 200

    content = response.json()
    assert len(content) == buildings_num


async def test_create_building(
        client: TestClient,
        faker: Faker,
        db: Session,
) -> None:
    data = {
        "address": faker.address(),
        "lat": str(faker.latitude()),
        "long": str(faker.longitude())
    }
    response = client.post(
        f"{settings.API_V1_STR}/buildings/",
        json=data,
    )
    assert response.status_code == 200

    content = response.json()
    assert "id" in content
    assert content["address"] == data["address"]
    assert "coordinates" in content
    assert re.search(r"^POINT", content["coordinates"])

    assert await BuildingRepository(db).exists_by_id(content['id'])


async def test_delete_building(client: TestClient, db: Session, building: BuildingFactory) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/buildings/{building.id}",
    )
    assert response.status_code == 204

    assert not await BuildingRepository(db).exists_by_id(building.id)


async def test_delete_building_not_found(client: TestClient) -> None:
    fake_building_id = uuid.uuid4()
    response = client.delete(
        f"{settings.API_V1_STR}/buildings/{fake_building_id}",
    )
    assert response.status_code == 404

    content = response.json()
    assert content["detail"] == "Object not found"
