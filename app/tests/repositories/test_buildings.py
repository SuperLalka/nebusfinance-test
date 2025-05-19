import random

from faker import Faker
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import Session

from app.repository.building import BuildingRepository
from app.schemas.building import BuildingInput, BuildingUpdate
from app.tests.factories import BuildingFactory
from app.tests.utils.building import create_building


async def test_create_building(db: Session, faker: Faker) -> None:
    new_building_data = {
        "address": faker.address(),
        "lat": faker.latitude(),
        "long": faker.longitude()
    }

    building_in = BuildingInput(**new_building_data)
    building = await BuildingRepository(db).create(building_in)
    assert building.address == new_building_data['address']
    assert to_shape(building.coordinates).wkt == f"POINT ({new_building_data['lat']} {new_building_data['long']})"


async def test_exists_by_id_building(db: Session, building: BuildingFactory) -> None:
    assert await BuildingRepository(db).exists_by_id(building.id)


async def test_is_exists_building(db: Session, building: BuildingFactory) -> None:
    assert await BuildingRepository(db).is_exists()


async def test_get_all_buildings(db: Session) -> None:
    buildings_num = random.randint(3, 6)
    [BuildingFactory.create() for _ in range(buildings_num)]

    buildings = await BuildingRepository(db).get_all()
    assert len(buildings) == buildings_num


async def test_get_by_id_building(db: Session, building: BuildingFactory) -> None:
    building_obj = await BuildingRepository(db).get_by_id(building.id)

    assert building_obj.id == building.id
    assert building_obj.address == building.address
    assert building_obj.coordinates == building.coordinates


async def test_update_building(db: Session, faker: Faker) -> None:
    building = await create_building(db)

    new_building_data = {
        "address": faker.address(),
        "coordinates": f"POINT ({faker.latitude()} {faker.longitude()})",
    }
    building_update = BuildingUpdate(**new_building_data)

    assert building.address != building_update.address
    assert to_shape(building.coordinates).wkt != building_update.coordinates

    await BuildingRepository(db).update(building, building_update)

    assert building.address == building_update.address
    assert to_shape(building.coordinates).wkt == building_update.coordinates


async def test_delete_building(db: Session) -> None:
    building = await create_building(db)

    await BuildingRepository(db).delete(building)

    assert not await BuildingRepository(db).exists_by_id(building.id)
