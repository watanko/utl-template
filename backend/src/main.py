from fastapi import FastAPI

from src.api.routers.health import router as health_router
from src.config import get_settings
from src.log_config import configure_logging


def create_app() -> FastAPI:
    """Create the FastAPI application.

    Returns:
        Configured FastAPI application.

    Raises:
        pydantic.ValidationError: If application settings are invalid.
        ValueError: If logging settings are invalid.
    """

    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(title=settings.app_name)
    app.include_router(health_router)
    return app


app = create_app()
