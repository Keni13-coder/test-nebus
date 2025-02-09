import pytest
from src.shared.queries.organization import OrganizationQueryBuilder

@pytest.fixture(scope="session")
async def builder():
    return OrganizationQueryBuilder()
