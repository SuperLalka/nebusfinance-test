from typing import List, Union

from sqlalchemy import Row

from app.models import Building
from app.repository._base import BaseRepository


class BuildingRepository(BaseRepository):

    def __init__(self, *args, **kwargs):
        super(BuildingRepository, self).__init__(*args, **kwargs)
        self.model = Building

    @staticmethod
    def object_mapping(rows: Union[Row, List[Row]]):
        from app.schemas.building import BuildingOutput

        if isinstance(rows, list):
            return [BuildingOutput(**row.__dict__) for row in rows]
        return BuildingOutput(**rows.__dict__)
