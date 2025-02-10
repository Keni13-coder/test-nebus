from typing import Protocol, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from src.shared.schemas.organization import (
    OrganizationQueryI,
    OrgIdQuery,
    OrgTitleQuery,
    CategoryPathQuery,
    CategoryTitleQuery,
    OfficeAddressQuery,
    GeoRadiusQuery,
    GeoBoxQuery
)

class BaseQuery(Protocol):
    _model: DeclarativeMeta
    
    async def find(self, session: AsyncSession, **kwargs) -> Any:
        ...
        

class QueryBuilder(Protocol):
        
    async def _get_by_id(self, query: OrgIdQuery):
        ...
        
    async def _get_by_title(self, query: OrgTitleQuery):
        ...
    
    async def _get_by_category_path(self, query: CategoryPathQuery):
        ...
        
    async def _get_by_category_title(self, query: CategoryTitleQuery):
        ...
    
    async def _get_by_office_address(self, query: OfficeAddressQuery):
        ...
    
    async def _get_by_geo_radius(self, query: GeoRadiusQuery):
        ...
    
    async def _get_by_geo_box(self, query: GeoBoxQuery):
        ...

    async def __call__(self, query: OrganizationQueryI):
        ...