import uuid

from geoalchemy2 import Geography, WKBElement
from sqlalchemy import (
    inspect,
    String,
    UUID
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Building(Base):
    __tablename__ = "building"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address: Mapped[str] = mapped_column(String, nullable=False)
    coordinates: Mapped[WKBElement] = mapped_column(Geography('POINT'), unique=True)

    organizations: Mapped[list["Organization"]] = relationship("Organization", back_populates="building")


building = inspect(Building).local_table
