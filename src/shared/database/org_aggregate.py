from src.shared.models.organization import Organization, Phone
from src.shared.models.office import Office, Geo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from src.shared.config.settings import settings
from src.shared.models.work import Category, Work
from src.shared.schemas.organization import OrganizationI


class OrgAggregate:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_organization(self, data: OrganizationI):
        try:
            stmt_org = insert(Organization).values(title=data.title).returning(Organization.org_id)
            org_id = (await self.session.execute(stmt_org)).scalar_one()
            
            stmt_phones = insert(Phone).values([{"org_id": org_id, "phone": phone.phone} for phone in data.phones])
            await self.session.execute(stmt_phones)
            
            address = data.office.address
            stmt_office = insert(Office).values([{"org_id": org_id, "address": address}]).returning(Office.office_id)
            office_id = (await self.session.execute(stmt_office)).scalar_one()
            
            geo = data.office.geo
            stmt_geo = insert(Geo).values(office_id=office_id, geog=from_shape(Point(geo.lon, geo.lat), srid=settings.SRID_GEO))
            await self.session.execute(stmt_geo)
            
            stmt_categories = insert(Category).values(
                [{"title": category.title, "path": category.path} for category in data.categories]
            ).returning(Category.category_id)
            category_ids = (await self.session.execute(stmt_categories)).scalars().all()
            
            stmt_works = insert(Work).values(
                [{"org_id": org_id, "category_id": category_id} for category_id in category_ids]
            )
            await self.session.execute(stmt_works)
            await self.session.commit()
            return org_id
        
        except Exception as e:
            await self.session.rollback()
            raise e

        
