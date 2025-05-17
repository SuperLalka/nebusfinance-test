from typing import List, Union

from sqlalchemy import Row
from sqlalchemy.dialects.postgresql import insert as postgres_insert

from app.models import Organization, OrganizationActivityAssociation
from app.repository._base import BaseRepository


class OrganizationRepository(BaseRepository):

    def __init__(self, *args, **kwargs):
        super(OrganizationRepository, self).__init__(*args, **kwargs)
        self.model = Organization

    @staticmethod
    def object_mapping(rows: Union[Row, List[Row]]):
        from app.schemas.organization import OrganizationOutput

        if isinstance(rows, list):
            return [OrganizationOutput(**row.__dict__) for row in rows]
        return OrganizationOutput(**rows.__dict__)

    async def add_organization_activity(self, organization_id: str, activity_id: int) -> None:
        query = (
            postgres_insert(OrganizationActivityAssociation)
            .values(**{
                "activity_id": activity_id,
                "organization_id": organization_id
            })
            .on_conflict_do_nothing()
        )
        self.session.execute(query)
        self.session.commit()
