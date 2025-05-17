from typing import List

from fastapi import HTTPException

from sqlalchemy import Row
from sqlalchemy.orm import Session

from app.repository.organization import OrganizationRepository
from app.schemas.organization import OrganizationInput
from app.services._base import BaseService


class OrganizationService(BaseService):

    def __init__(self, session: Session, *args, **kwargs):
        super(OrganizationService, self).__init__(session, *args, **kwargs)
        self.repository = OrganizationRepository(session, model_filter=kwargs.get('model_filter'))

    async def create(self, data: OrganizationInput, activities: List[int]) -> Row:
        from app.repository.activity import ActivityRepository
        from app.repository.building import BuildingRepository

        for activity_id in activities:
            if not await ActivityRepository(self.session).exists_by_id(activity_id):
                raise HTTPException(status_code=400, detail="Activity type does not exist.")

        if not await BuildingRepository(self.session).exists_by_id(data.building_id):
            raise HTTPException(status_code=400, detail="Building does not exist.")

        organization = await self.repository.create(data)

        for activity_id in activities:
            await self.repository.add_organization_activity(organization.id, activity_id)

        return organization
