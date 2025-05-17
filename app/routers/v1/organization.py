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


@router.get("/{organization_id}", response_model=OrganizationOutput)
@router.get("/{organization_id}/", response_model=OrganizationOutput, include_in_schema=False)
async def get_organization(
    request: Request,
    session: SessionDep,
    organization_id: UUID4,
):
    return await OrganizationService(session).get_by_id(organization_id)


def get_organization_filter():
    return OrganizationFilter


@router.get("", response_model=List[OrganizationOutput])
@router.get("/", response_model=List[OrganizationOutput], include_in_schema=False)
async def get_organizations(
    request: Request,
    session: SessionDep,
    organizations_filter=Depends(lambda: OrganizationFilter),
    filter_params=Depends(OrganizationFilterDTO),
):
    filter_params = filter_params.dict(exclude_unset=True)
    return await OrganizationService(
        session,
        model_filter=organizations_filter(**filter_params),
    ).get_all()


@router.post("", response_model=OrganizationOutput)
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


@router.delete("/{organization_id}", status_code=204)
@router.delete("/{organization_id}/", status_code=204, include_in_schema=False)
async def delete_organization(
    request: Request,
    session: SessionDep,
    organization_id: UUID4,
):
    return await OrganizationService(session).delete(organization_id)
