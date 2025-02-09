from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["test", "prod"] = "test"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    EXTERNAL_HOST: bool = False
    model_config = SettingsConfigDict(env_file=".env")
    POSTGRES_POOL_SIZE: int = 10
    POSTGRES_MAX_OVERFLOW: int = 20
    SRID_GEO: int = 4326
    
    @property
    def postgres_uri(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT if self.EXTERNAL_HOST else 5432}/{self.POSTGRES_DB}"
    

settings = Settings()