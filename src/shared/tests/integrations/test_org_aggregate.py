import pytest
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload

from src.shared.database.org_aggregate import OrgAggregate
from src.shared.schemas.organization import OrganizationI
from src.shared.models.organization import Organization, Phone
from src.shared.models.office import Office, Geo
from src.shared.models.work import Category, Work


@pytest.mark.asyncio(loop_scope="session")
async def test_org_aggregate(session):
    org_aggregate = OrgAggregate(session)
    org_id = await org_aggregate.create_organization(
        OrganizationI(
            title="Test Organization",
            office={
                "address": "Test Address",
                "geo": {"lon": 1.0, "lat": 1.0}
            },
            phones=[
                {"phone": "+79999999999"},
                {"phone": "+79999999998"}
            ],
            categories=[
                {"title": "Test Category", "path": "/test-parent/test-category"},
                {"title": "Test Category 2", "path": "/test-parent/test-category-2"}
            ]
        )
    )
    assert org_id is not None

    # Запрос основных данных организации
    stmt = (
        select(
            Organization.org_id,
            Organization.title.label("org_title"),
            Office.address,
            Geo.geog,
            func.array_agg(Phone.phone.distinct()).label("phones"),
            func.array_agg(Category.title.distinct()).label("category_titles"),
            func.array_agg(Category.path.distinct()).label("category_paths")
        )
        .select_from(Organization)
        .join(Office, Organization.org_id == Office.org_id)
        .join(Geo, Office.office_id == Geo.office_id)
        .join(Phone, Organization.org_id == Phone.org_id)
        .join(Work, Organization.org_id == Work.org_id)
        .join(Category, Work.category_id == Category.category_id)
        .group_by(
            Organization.org_id,
            Organization.title,
            Office.address,
            Geo.geog
        )
    )
    
    result = (await session.execute(stmt)).mappings().one()

    # Проверки
    assert result["org_title"] == "Test Organization"
    assert result["address"] == "Test Address"
    assert "+79999999999" in result["phones"]
    assert "+79999999998" in result["phones"]
    assert "Test Category" in result["category_titles"]
    assert "Test Category 2" in result["category_titles"]
    assert "/test-parent/test-category" in result["category_paths"]
    assert "/test-parent/test-category-2" in result["category_paths"]