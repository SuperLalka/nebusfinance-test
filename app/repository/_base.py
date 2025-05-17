from typing import Any, Optional, Type, Sequence

from sqlalchemy import select, Row
from sqlalchemy.orm import Session

from app.repository.filters._base import BaseFilter


class BaseRepository:

    def __init__(
        self,
        session: Session = None,
        model: Type[Row] = None,
        model_filter: Type[BaseFilter] = None
    ):
        self.session = session
        self.model = model
        self.model_filter = model_filter

    @staticmethod
    def object_mapping(rows: Sequence[Row]):
        raise NotImplementedError()

    @property
    def base_query(self):
        query = select(self.model)

        if self.model_filter:
            query = self.model_filter(query)
        return query

    async def create(self, data: Any) -> Row:
        db_object = self.model(**data.model_dump())
        self.session.add(db_object)
        self.session.commit()
        self.session.refresh(db_object)
        return db_object

    async def exists_by_id(self, _id: Any) -> bool:
        return self.session.query(self.model).filter(self.model.id == _id).first() is not None

    async def is_exists(self) -> bool:
        result = self.session.execute(self.base_query).scalar()
        return bool(result)

    async def get_all(self) -> Sequence[Row]:
        results = self.session.execute(self.base_query.distinct()).scalars()
        return results.all()

    async def get_by_id(self, _id: Any) -> Optional[Row]:
        result = self.session.query(self.model).filter(self.model.id == _id).first()
        return result

    async def update(self, obj: Row, data: Any) -> Row:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(obj, key, value)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    async def delete(self, obj: Row) -> bool:
        self.session.delete(obj)
        self.session.commit()
        return True

    async def count(self):
        return self.session.execute(self.base_query).scalar()
