import datetime
from typing import List, Optional

from fastapi import HTTPException
from typing_extensions import Self

from pydantic import BaseModel, UUID4, model_validator


class OrganizationBase(BaseModel):
    name: str
    phone_numbers: List[str] = []

    building_id: UUID4


class OrganizationInput(OrganizationBase):
    pass


class OrganizationOutput(OrganizationBase):
    id: UUID4

    created_at: datetime.datetime
    updated_at: datetime.datetime


class OrganizationUpdate(OrganizationBase):
    pass


class OrganizationFilterDTO(BaseModel):
    activity_id: Optional[str] = None
    activity_group: Optional[str] = None
    building_id: Optional[UUID4] = None
    name: Optional[str] = None

    within_radius_point: Optional[str] = None
    within_radius_distance: Optional[int] = None
    within_radius_value: Optional[tuple] = None

    within_area_points: Optional[str] = None
    within_area_value: Optional[str] = None

    @model_validator(mode='after')
    def validate(self) -> Self:
        if any([self.within_radius_point, self.within_radius_distance]):
            if not all([self.within_radius_point, self.within_radius_distance]):
                raise HTTPException(
                    status_code=400,
                    detail="within_radius_point and within_radius_distance must be specified."
                )
            lat, long = self.within_radius_point.split(',')
            self.within_radius_value = (f'POINT({lat} {long})', self.within_radius_distance)

        if self.within_area_points:
            self.within_area_value = f'POLYGON(({self.within_area_points}))'

        return self
