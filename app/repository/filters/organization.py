
from sqlalchemy import and_, or_, func, exists
from sqlalchemy.orm import aliased

from app.models import (
    Activity,
    Building,
    Organization,
    organization
)
from app.repository.filters._base import join, TO_JOIN


class OrganizationFilter:
    orm_class = Organization

    def __init__(self, **fields):
        self.fields = fields
        self.aliases = {}
        self.aliases["activities"] = aliased(Activity)
        self.aliases["building"] = aliased(Building)

    def filter_by_name(self, value: str):
        return self.orm_class.name.icontains(value)

    def filter_by_building_id(self, value: str):
        return self.orm_class.building_id == value

    # список организаций которые относятся к одной деятельности
    @join("activities")
    def filter_by_activity_id(self, value: id):
        return self.aliases["activities"].id == value

    # список организаций которые относятся к общей группе деятельности
    @join("activities")
    def filter_by_activity_group(self, value: id):
        return exists().where(
            or_(
                self.aliases["activities"].id == value,
                self.aliases["activities"].activity_id == value,
                and_(
                    Activity.activity_id == value,
                    self.aliases["activities"].activity_id == Activity.id,
                )
            )
        )

    # список организаций которые находятся в заданном радиусе относительно указанной точки на карте
    @join("building")
    def filter_by_within_radius_value(self, value: tuple):
        return func.ST_DWithin(
            self.aliases["building"].coordinates,
            value[0],
            value[1],
            use_spheroid=False
        )

    # список организаций которые находятся в заданной прямоугольной области на карте
    @join("building")
    def filter_by_within_area_value(self, value: str):
        return func.ST_Intersects(
            value,
            self.aliases["building"].coordinates
        )

    def _join(self, base_query):
        joined_tables = set()
        for func_name, field in TO_JOIN:

            field_name = func_name.replace("filter_by_", "")

            if (
                field_name not in self.fields
                or self.fields[field_name] is None
                or field in joined_tables
            ):
                continue

            base_query = base_query.outerjoin(
                self.aliases[field], getattr(Organization, field)
            )

            joined_tables.add(field)

        return base_query

    def __call__(self, base_query, operator=and_):
        query = []
        base_query = self._join(base_query)

        for name, value in self.fields.items():
            if value is None:
                continue
            method_name = f"filter_by_{name}"

            if hasattr(self, method_name):
                method_name = f"filter_by_{name}"
                filter_method = getattr(self, method_name)
                expression = filter_method(value)

                if expression is not None:
                    query.append(expression)
            elif hasattr(organization.c, name):
                query.append(getattr(organization.c, name) == value)

        return base_query.where(operator(*query))
