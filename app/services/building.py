
from sqlalchemy.orm import Session

from app.repository.building import BuildingRepository
from app.services._base import BaseService


class BuildingService(BaseService):

    def __init__(self, session: Session, *args, **kwargs):
        super(BuildingService, self).__init__(session, *args, **kwargs)
        self.repository = BuildingRepository(session)
