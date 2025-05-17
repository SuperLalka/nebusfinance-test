from typing import Optional

from geoalchemy2.shape import to_shape
from pydantic import BaseModel, Field, UUID4, computed_field, field_validator
from pydantic_extra_types.coordinate import Latitude, Longitude


class BuildingBase(BaseModel):
    address: str


class BuildingInput(BuildingBase):
    lat: Optional[Latitude] = Field(exclude=True)
    long: Optional[Longitude] = Field(exclude=True)

    @computed_field
    @property
    def coordinates(self) -> str:
        return f"POINT({self.lat} {self.long})"


class BuildingOutput(BuildingBase):
    id: UUID4
    coordinates: str

    @field_validator("coordinates", mode="before")
    def turn_coordinates_into_wkt(cls, value):
        return to_shape(value).wkt
