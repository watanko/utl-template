"""Application configuration schema."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application environment variable schema.

    Attributes:
        app_name: Public service name used in logs and API metadata.
        app_env: Runtime environment name.
        database_url: SQLAlchemy database URL.
        jwt_secret: Secret key used for JWT signing.
        log_level: Structlog log level.

    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
    )

    app_name: str = Field(
        default="utl-template",
        description="Public service name used in logs and API metadata.",
    )
    app_env: Literal["local", "test", "staging", "production"] = Field(
        default="local",
        description="Runtime environment name.",
    )
    database_url: str = Field(
        default="sqlite:///./local.db",
        description="SQLAlchemy database URL.",
    )
    jwt_secret: SecretStr = Field(
        default=SecretStr("replace-me-local-only"),
        description="Secret key used for JWT signing.",
    )
    log_level: str = Field(
        default="INFO",
        description="Structlog log level.",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings.

    Returns:
        Cached settings instance.

    Raises:
        pydantic.ValidationError: If environment variables are invalid.

    """
    return Settings()
