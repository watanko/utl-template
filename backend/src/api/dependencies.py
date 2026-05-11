from src.adapters.external.health_query import StaticHealthQuery
from src.config import get_settings
from src.core.application.ports.health_query import HealthQuery
from src.core.application.usecases.get_health import GetHealth


def provide_health_query() -> HealthQuery:
    """Provide the health query implementation.

    Returns:
        Health query port implementation.

    Raises:
        pydantic.ValidationError: If settings are invalid.
    """

    settings = get_settings()
    return StaticHealthQuery(service_name=settings.app_name)


def provide_get_health() -> GetHealth:
    """Provide the health check use case.

    Returns:
        Configured health check use case.

    Raises:
        pydantic.ValidationError: If settings are invalid.
    """

    return GetHealth(health_query=provide_health_query())
