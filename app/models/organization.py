import uuid

from sqlalchemy import (
    func,
    inspect,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    UUID,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import ARRAY, DATETIME

from app.config.database import Base


OrganizationActivityAssociation = Table(
    'org_activity',
    Base.metadata,
    Column('activity_id', Integer, ForeignKey('activity.id', ondelete="CASCADE")),
    Column('organization_id', UUID, ForeignKey('organization.id', ondelete="CASCADE")),
    UniqueConstraint("activity_id", "organization_id", name="org_activity_un"),
)


class Activity(Base):
    __tablename__ = "activity"
    __table_args__ = (
        UniqueConstraint("title", "activity_id", name="activity_child_title_un"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)

    activity_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("activity.id", ondelete="SET NULL"),
        nullable=True
    )

    organizations: Mapped[list["Organization"]] = relationship(
        'Organization',
        secondary=OrganizationActivityAssociation,
        back_populates='activities'
    )


class Organization(Base):
    __tablename__ = "organization"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone_numbers: Mapped[ARRAY] = mapped_column(ARRAY(String), default=list)

    created_at: Mapped[DATETIME] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DATETIME] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    activities: Mapped[list["Activity"]] = relationship(
        'Activity',
        secondary=OrganizationActivityAssociation,
        back_populates='organizations'
    )

    building_id: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("building.id", ondelete="SET NULL"),
    )
    building: Mapped["Building"] = relationship("Building", back_populates="organizations")


activity = inspect(Activity).local_table
organization = inspect(Organization).local_table
