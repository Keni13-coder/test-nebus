from src.shared.database.base import get_session
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.security.security import verify_signature
from src.api.config.settings import settings


signature_header = APIKeyHeader(name="X-Signature")
session_dependency = Annotated[AsyncSession, Depends(get_session)]

async def verify_request_signature(
    signature: str = Depends(signature_header)
):
    """
    Проверяет подпись из заголовка X-Signature на соответствие секретному ключу
    """
    if not verify_signature(signature):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неверная подпись"
        )
    return True