from typing import List

from fastapi import APIRouter, Body, Request

from app.routers.depends import SessionDep
from app.schemas.building import BuildingInput, BuildingOutput
from app.services.building import BuildingService

router = APIRouter(
    prefix="/buildings",
    tags=["buildings"]
)


@router.get("", response_model=List[BuildingOutput])
@router.get("/", response_model=List[BuildingOutput], include_in_schema=False)
async def get_buildings(
    request: Request,
    session: SessionDep
):
    return await BuildingService(session).get_all()


@router.post("", response_model=BuildingOutput)
@router.post("/", response_model=BuildingOutput, include_in_schema=False)
async def create_building(
    request: Request,
    session: SessionDep,
    building_data: BuildingInput = Body(...),
):
    return await BuildingService(session).create(building_data)


@router.delete("/{building_id}", status_code=204)
@router.delete("/{building_id}/", status_code=204, include_in_schema=False)
async def delete_building(
    request: Request,
    session: SessionDep,
    building_id: str,
):
    return await BuildingService(session).delete(building_id)
