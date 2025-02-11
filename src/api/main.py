from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import operations
from src.api.config.settings import settings
from src.api.dependencies import verify_request_signature



def create_app():
    fastapi_app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_VERSION}/openapi.json",
        dependencies=[Depends(verify_request_signature)]
    )

    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,  # Allows all origins
        allow_credentials=True,
        allow_methods=settings.CORS_METHODS,  # Allows all methods
        allow_headers=settings.CORS_HEADERS,  # Allows all headers
    )
    fastapi_app.include_router(
        operations.router,
        prefix=settings.API_VERSION,
    )

    return fastapi_app


app = create_app()