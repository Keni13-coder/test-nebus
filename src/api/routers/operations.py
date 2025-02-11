from fastapi import APIRouter, Depends, Query
from src.api.bootstrap import bootstrap
from src.api.utils.openapi import generate_union_openapi_schema
from src.shared.schemas.organization import OrganizationQueryI, OrganizationQueryO
from src.api.dependencies import session_dependency
from src.api.exceptoins.base import ServerException
from src.api.schemas.base import ErrorResponse
from typing import Annotated
from src.api.utils.query_parser import UnionQueryParser

router = APIRouter(
    prefix='/operations',
    tags=['Operations']
    )

factory = bootstrap()

@router.get(
    '/find/',
    responses={
        200: {
            'model': list[OrganizationQueryO],
            'description': 'Успешный поиск организаций'
        },
        400: {
            'model': ErrorResponse,
            'description': 'Ошибка валидации параметров запроса'
        },
        403: {
            'model': ErrorResponse,
            'description': 'Ошибка проверки подписи запроса'
        },
        500: {
            'model': ErrorResponse,
            'description': 'Внутренняя ошибка сервера'
        }
    }
)
async def find_organization(
    query: Annotated[OrganizationQueryI, Depends(UnionQueryParser.parse(OrganizationQueryI))],
    session: session_dependency
) -> list[OrganizationQueryO]:
    operation = factory['find_organization']
    return await operation(session, query)