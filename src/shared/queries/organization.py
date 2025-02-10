from typing import Any, Dict, Type
from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseQuery
from src.shared.models.organization import Organization, Phone
from src.shared.models.work import Work, Category
from src.shared.models.office import Office, Geo

from src.shared.schemas.organization import (
    OrganizationQueryI,
    OrganizationQueryO,
    OrgIdQuery,
    OrgTitleQuery,
    CategoryPathQuery,
    CategoryTitleQuery,
    OfficeAddressQuery,
    GeoRadiusQuery,
    GeoBoxQuery
    )
from sqlalchemy import select, func, or_

from .base import QueryBuilder
from inspect import signature, getmembers, ismethod
from src.shared.config.settings import settings
from geoalchemy2.shape import from_shape
from shapely.geometry import Point, box


class OrganizationQueryBuilder(QueryBuilder):
    
    def __init__(self):
        self._query_handlers: Dict[Type[OrganizationQueryI], str] = {}
        self._register_handlers()
    
    def _register_handlers(self):
        for method_name, method in getmembers(self, predicate=lambda x: ismethod(x) and x.__name__.startswith('_get_by_')):
            sig = signature(method)
            if 'query' in sig.parameters:
                param_type = sig.parameters['query'].annotation
                self._query_handlers[param_type] = method_name
    
    def _base_query(self):
        """
        Базовый запрос с общей структурой
        """
        return (
            select(
                Organization.title.label('org_title'),
                func.array_agg(Phone.phone.distinct()).label('phones'),
                Office.address.label('office_address'),
                func.array_agg(Category.title.distinct()).label('categories_titles')
            )
            .select_from(Organization)
            .join(Phone, Organization.org_id == Phone.org_id)
            .join(Office, Organization.org_id == Office.org_id)
            .join(Work, Organization.org_id == Work.org_id)
            .join(Category, Work.category_id == Category.category_id)
            .group_by(Organization.title, Office.address)
        )
    
    async def _get_by_id(self, query: OrgIdQuery):
        '''
        Поиск организации по id
        Returns:
            seleceted organization by schema OrganizationQueryO
        '''
        return self._base_query().where(Organization.org_id == query.org_id)
    
    async def _get_by_title(self, query: OrgTitleQuery):
        '''
        Поиск организации по названию
        Returns:
            seleceted organization by schema OrganizationQueryO
        '''
        return self._base_query().where(Organization.title.ilike(f"%{query.org_title}%"))
    
    async def _get_by_category_path(self, query: CategoryPathQuery):
        '''
        Поиск организации по пути категории
        Returns:
            seleceted organization by schema OrganizationQueryO
        '''
        return self._base_query().where(
            or_(
                Category.path == query.category_path,
                Category.path.like(f"{query.category_path}/%")
            )
        )

    async def _get_by_category_title(self, query: CategoryTitleQuery):
        '''
        Поиск организации по названию категории
        Returns:
            seleceted organization by schema OrganizationQueryO
        '''
        return self._base_query().where(Category.title.ilike(f"%{query.category_title}%"))
    
    async def _get_by_office_address(self, query: OfficeAddressQuery):
        '''
        Поиск организации по адресу офиса
        Returns:
            seleceted organization by schema OrganizationQueryO
        '''
        return self._base_query().where(Office.address.ilike(f"%{query.office_address}%"))
    
    async def _get_by_geo_radius(self, query: GeoRadiusQuery):
        '''
        Поиск организации по радиусу
        Returns:
            seleceted organization by schema OrganizationQueryO
        '''
        point = Point(query.geo.lon, query.geo.lat)
        return (
            self._base_query()
            .join(Geo, Office.office_id == Geo.office_id)
            .where(
                Geo.geog.ST_DWithin(
                    from_shape(point, srid=settings.SRID_GEO),
                    query.radius
                )
            )
        )
    
    async def _get_by_geo_box(self, query: GeoBoxQuery):
        '''
        Поиск организации по гео-боксу
        Returns:
            seleceted organization by schema OrganizationQueryO
        '''
        bbox = box(
            query.min_lon,
            query.min_lat,
            query.max_lon,
            query.max_lat
        )
        return (
            self._base_query()
            .join(Geo, Office.office_id == Geo.office_id)
            .where(
                Geo.geog.ST_Intersects(
                    from_shape(bbox, srid=settings.SRID_GEO)
                )
            )
        )
        
    async def __call__(self, query: OrganizationQueryI):
        query_type = type(query)
        if query_type not in self._query_handlers:
            raise ValueError(f"Unknown query type: {query_type}")
            
        handler_name = self._query_handlers[query_type]
        handler = getattr(self, handler_name)
        
        return await handler(query)

class OrganizationQuery(BaseQuery):
    _model = Organization
    
    def __init__(self, builder: QueryBuilder):
        self._builder = builder
    

    async def find(self, session: AsyncSession, **kwargs) -> list[OrganizationQueryO]:
        stmt = await self._builder(**kwargs)
        result = await session.execute(stmt)
        rows = result.mappings().all()
        return [OrganizationQueryO.model_validate(row) for row in rows]
    
    