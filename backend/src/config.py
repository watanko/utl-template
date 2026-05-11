from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        app_name: Public service name used in logs and API metadata.
        app_env: Runtime environment name.
        database_url: SQLAlchemy database URL.
        log_level: Structlog log level.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = Field(default="utl-template")
    app_env: Literal["local", "test", "staging", "production"] = Field(default="local")
    database_url: str = Field(default="sqlite:///./local.db")
    log_level: str = Field(default="INFO")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings.

    Returns:
        Cached settings instance.

    Raises:
        pydantic.ValidationError: If environment variables are invalid.
    """

    return Settings()
