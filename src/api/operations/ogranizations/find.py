from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.api.operations.base import Operation
from src.api.exceptoins.base import ServerException
from src.shared.schemas.organization import OrganizationQueryI, OrganizationQueryO
from src.shared.queries.organization import OrganizationQuery


class FindOrganization(Operation):
    
    def __init__(self, query: OrganizationQuery):
        self._query = query
        
    async def __call__(
        self,
        session: AsyncSession,
        query: OrganizationQueryI
        ) -> list[OrganizationQueryO]:
        try:
            async with session as s:
                return await self._query.find(s, query=query)
        except SQLAlchemyError as e:
            raise ServerException(str(e)) from e
