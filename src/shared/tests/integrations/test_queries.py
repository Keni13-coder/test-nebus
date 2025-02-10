import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.queries.organization import OrganizationQuery, OrganizationQueryBuilder
from src.shared.database.org_aggregate import OrgAggregate
from src.shared.schemas.organization import (
    OrganizationI,
    OrganizationQueryO,
    OrgIdQuery,
    OrgTitleQuery,
    CategoryPathQuery,
    CategoryTitleQuery,
    OfficeAddressQuery,
    GeoRadiusQuery,
    GeoBoxQuery,
    GeoI
)

TEST_DATA = {
    "organization": {
        "title": "Test Organization",
        "office": {
            "address": "Test Address",
            "geo": {"lon": 1.0, "lat": 1.0}
        },
        "phones": [
            {"phone": "+79999999999"},
            {"phone": "+79999999998"}
        ],
        "categories": [
            {"title": "Test Category", "path": "/test-parent/test-category"},
            {"title": "Test Category 2", "path": "/test-parent/test-category-2"}
        ]
    },
    "organization2": {
        "title": "Another Organization",
        "office": {
            "address": "Test Address",
            "geo": {"lon": 1.001, "lat": 1.001}
        },
        "phones": [
            {"phone": "+79999999997"},
            {"phone": "+79999999996"}
        ],
        "categories": [
            {"title": "Test Category", "path": "/test-parent/test-category"},
            {"title": "Another Category", "path": "/test-parent/another-category"}
        ]
    },
    "expected": {
        "org_title": "Test Organization",
        "office_address": "Test Address",
        "phones": ["+79999999999", "+79999999998"],
        "categories_titles": ["Test Category", "Test Category 2"]
    },
    "expected2": {
        "org_title": "Another Organization",
        "office_address": "Another Address",
        "phones": ["+79999999997", "+79999999996"],
        "categories_titles": ["Test Category", "Another Category"]
    }
}

@pytest.fixture(scope="module")
async def org_query():
    """Фикстура для создания OrganizationQuery"""
    builder = OrganizationQueryBuilder()
    return OrganizationQuery(builder)

@pytest.fixture(scope="module")
async def test_data(session: AsyncSession):
    """Фикстура для создания тестовых данных"""
    org_aggregate = OrgAggregate(session)
    org_id = await org_aggregate.create_organization(
        OrganizationI(**TEST_DATA["organization"])
    )
    org_id2 = await org_aggregate.create_organization(
        OrganizationI(**TEST_DATA["organization2"])
    )
    return org_id


@pytest.mark.asyncio(loop_scope="module")
async def test_find_by_id(session: AsyncSession, org_query, test_data):
    """Тест поиска организации по ID"""
    result = await org_query.find(
        session,
        query=OrgIdQuery(org_id=test_data)
    )
    assert len(result) == 1
    assert result[0].org_title == TEST_DATA["expected"]["org_title"]
    assert set(result[0].phones) == set(TEST_DATA["expected"]["phones"])
    assert result[0].office_address == TEST_DATA["expected"]["office_address"]
    assert set(result[0].categories_titles) == set(TEST_DATA["expected"]["categories_titles"])


@pytest.mark.asyncio(loop_scope="module")
async def test_find_by_title(session: AsyncSession, org_query, test_data):
    """Тест поиска организации по title"""
    result = await org_query.find(
        session,
        query=OrgTitleQuery(org_title=TEST_DATA["organization"]["title"])
    )
    assert len(result) == 1
    assert result[0].org_title == TEST_DATA["expected"]["org_title"]
    assert set(result[0].phones) == set(TEST_DATA["expected"]["phones"])
    assert result[0].office_address == TEST_DATA["expected"]["office_address"]
    assert set(result[0].categories_titles) == set(TEST_DATA["expected"]["categories_titles"])


@pytest.mark.asyncio(loop_scope="module")
@pytest.mark.parametrize(
    "query, expected_count", 
    [
        (CategoryPathQuery(category_path='/test-parent'), 2),
        (CategoryTitleQuery(category_title=TEST_DATA["organization"]["categories"][0]["title"]), 2),
        (OfficeAddressQuery(office_address=TEST_DATA["organization"]["office"]["address"]), 2),
        (GeoRadiusQuery(
            geo=GeoI(
                lon=TEST_DATA["organization"]["office"]["geo"]["lon"],
                lat=TEST_DATA["organization"]["office"]["geo"]["lat"]),
            radius=1000
            ), 2),
        (GeoBoxQuery(
            min_lon=TEST_DATA["organization"]["office"]["geo"]["lon"] - 0.1,
            min_lat=TEST_DATA["organization"]["office"]["geo"]["lat"] - 0.1,
            max_lon=TEST_DATA["organization"]["office"]["geo"]["lon"] + 0.1,
            max_lat=TEST_DATA["organization"]["office"]["geo"]["lat"] + 0.1),
        2),
    ]
)
async def test_find_all(session: AsyncSession, org_query, query, expected_count):
    """Тест поиска всех организаций"""
    result = await org_query.find(session, query=query)
    assert isinstance(result, list)
    assert len(result) == expected_count

