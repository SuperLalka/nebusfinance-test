from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, Request
from pydantic import UUID4

from app.repository.filters.organization import OrganizationFilter
from app.routers.depends import SessionDep
from app.schemas.organization import OrganizationInput, OrganizationOutput, OrganizationFilterDTO
from app.services.organization import OrganizationService

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"]
)


@router.get(
    "/{organization_id}",
    response_model=OrganizationOutput,
    summary="Get organization",
    description="Get organization by id"
)
@router.get("/{organization_id}/", response_model=OrganizationOutput, include_in_schema=False)
async def get_organization(
    request: Request,
    session: SessionDep,
    organization_id: UUID4,
):
    return await OrganizationService(session).get_by_id(organization_id)


def get_organization_filter():
    return OrganizationFilter


@router.get(
    "",
    response_model=List[OrganizationOutput],
    summary="Get list of organizations",
    description="Returns a list of all organizations in the database"
)
@router.get("/", response_model=List[OrganizationOutput], include_in_schema=False)
async def get_organizations(
    request: Request,
    session: SessionDep,
    organizations_filter=Depends(lambda: OrganizationFilter),
    filter_params=Depends(OrganizationFilterDTO),
):
    filter_params = filter_params.model_dump(exclude_unset=True)
    return await OrganizationService(
        session,
        model_filter=organizations_filter(**filter_params),
    ).get_all()


@router.post(
    "",
    response_model=OrganizationOutput,
    summary="Create organization",
    description="Create a organization entry with all the information, name, phone_numbers, building_id and activities"
)
@router.post("/", response_model=OrganizationOutput, include_in_schema=False)
async def create_organization(
    request: Request,
    session: SessionDep,
    organization: OrganizationInput,
    activities: Annotated[List[int], Body()]
):
    return await OrganizationService(session).create(
        organization,
        activities
    )


@router.delete(
    "/{organization_id}",
    summary="Delete organization",
    description="Delete a organization by id",
    status_code=204,
)
@router.delete("/{organization_id}/", status_code=204, include_in_schema=False)
async def delete_organization(
    request: Request,
    session: SessionDep,
    organization_id: UUID4,
):
    return await OrganizationService(session).delete(organization_id)
