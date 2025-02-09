import pytest

from src.shared.queries.organization import OrganizationQueryBuilder
from src.shared.schemas.organization import (
    GeoI,
    OrganizationQueryI,
    OrgIdQuery,
    OrgTitleQuery,
    CategoryPathQuery,
    CategoryTitleQuery,
    OfficeAddressQuery,
    GeoRadiusQuery,
    GeoBoxQuery
)

@pytest.mark.parametrize("query", [
    OrgIdQuery(org_id=1),
    OrgTitleQuery(org_title="Test Organization"),
    CategoryPathQuery(category_path="Test Category Path"),
    CategoryTitleQuery(category_title="Test Category Title"),
    OfficeAddressQuery(office_address="Test Office Address"),
    GeoRadiusQuery(geo=GeoI(lon=1, lat=1), radius=1),
    GeoBoxQuery(min_lon=1, min_lat=1, max_lon=2, max_lat=2)
])
async def test_organization_query_builder(builder: OrganizationQueryBuilder, query: OrganizationQueryI):
    result = await builder(query)
    assert result is not None

