import pytest
from src.shared.models.organization import Organization, Phone
from src.shared.models.office import Office, Geo
from src.shared.models.work import Category, Work
from sqlalchemy.dialects.postgresql import insert
from geoalchemy2.shape import from_shape
from shapely.geometry import Point, box
from sqlalchemy import select
from src.shared.config.settings import settings

data = {'organization': None, 'phone': None, 'office': None, 'geo': None, 'category': None, 'work': None}

@pytest.mark.asyncio(loop_scope="session")
async def test_create_organization(session):
    stmt = insert(Organization).values(title="Test Organization").returning(Organization.org_id)
    result = await session.execute(stmt)
    await session.commit()
    data['organization'] = result.scalar_one()
    assert (await session.execute(select(Organization).filter(Organization.org_id == data['organization']))).scalar_one()


@pytest.mark.asyncio(loop_scope="session")
async def test_create_phone(session):
    stmt = insert(Phone).values(org_id=data['organization'], phone="1234567890").returning(Phone.phone_id)
    result = await session.execute(stmt)
    await session.commit()
    data['phone'] = result.scalar_one()
    assert (await session.execute(select(Phone).filter(Phone.phone_id == data['phone']))).scalar_one()


@pytest.mark.asyncio(loop_scope="session")
async def test_create_office(session):
    stmt = insert(Office).values(org_id=data['organization'], address="Test Address").returning(Office.office_id)
    result = await session.execute(stmt)
    await session.commit()
    data['office'] = result.scalar_one()
    assert (await session.execute(select(Office).filter(Office.office_id == data['office']))).scalar_one()


@pytest.mark.asyncio(loop_scope="session")
async def test_create_geo(session):
    point = Point(123.456, 78.901)
    stmt = insert(Geo).values(office_id=data['office'], geog=from_shape(point, srid=settings.SRID_GEO)).returning(Geo.geo_id)
    result = await session.execute(stmt)
    await session.commit()
    data['geo'] = result.scalar_one()
    assert (await session.execute(select(Geo).filter(Geo.geo_id == data['geo']))).scalar_one()


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category(session):
    stmt = insert(Category).values(title="Test Category", path="/test-parent/test-category").returning(Category.category_id)
    result = await session.execute(stmt)
    await session.commit()
    data['category'] = result.scalar_one()
    assert (await session.execute(select(Category).filter(Category.title == "Test Category"))).scalar_one()


@pytest.mark.asyncio(loop_scope="session")
async def test_create_work(session):
    stmt = insert(Work).values(category_id=data['category'], org_id=data['organization']).returning(Work.work_id)
    result = await session.execute(stmt)
    await session.commit()
    data['work'] = result.scalar_one()
    assert (await session.execute(select(Work).filter(Work.category_id == data['category'], Work.org_id == data['organization']))).scalar_one()
