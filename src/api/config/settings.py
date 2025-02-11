from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    PROJECT_NAME: str = "API"
    API_VERSION: str = "/api/v1"
    SECRET_KEY: str
    
    
    CORS_HEADERS: list[str] = Field(
        default=[
            "Content-Type",
            "Set-Cookie",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin",
            "Authorization",
        ],
        title="Допустимые заголовки",
    )
    
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000"],
        title="Допустимые сервера для подключения",
    )
    
    CORS_METHODS: list[str] = Field(
        default=["GET"],
        title="Допустимые http методы",
    )


settings = Settings()