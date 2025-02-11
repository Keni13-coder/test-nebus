'''registred operations'''

from src.api.operations.base import OperationFactory
from src.api.operations.ogranizations.find import FindOrganization
from src.shared.queries.organization import OrganizationQuery, OrganizationQueryBuilder


def bootstrap() -> OperationFactory:
    factory = OperationFactory()
    factory.register(
        key='find_organization',
        operation_class=FindOrganization,
        dependencies={
            'query': OrganizationQuery(OrganizationQueryBuilder())
        }
    )
    return factory
