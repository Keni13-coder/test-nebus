from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["test", "prod"] = "test"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    PGBOUNCER_HOST: str = "my-pgbouncer"
    PGBOUNCER_PORT: int = 6432
    EXTERNAL_HOST: bool = False
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    POSTGRES_POOL_SIZE: int = 10
    POSTGRES_MAX_OVERFLOW: int = 20
    SRID_GEO: int = 4326
    
    @property
    def postgres_uri(self) -> str:
        # Используем pgbouncer для приложения
        host = self.PGBOUNCER_HOST if not self.EXTERNAL_HOST else self.POSTGRES_HOST
        port = self.PGBOUNCER_PORT if not self.EXTERNAL_HOST else self.POSTGRES_PORT
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{host}:{port}/{self.POSTGRES_DB}"
    

settings = Settings()