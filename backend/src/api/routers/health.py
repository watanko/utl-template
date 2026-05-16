"""Health check HTTP routes."""

from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import provide_get_health
from src.api.schemas import HealthResponse
from src.core.application.usecases.get_health import GetHealth

router = APIRouter(tags=["health"])


@router.get("/health")
def get_health(use_case: Annotated[GetHealth, Depends(provide_get_health)]) -> HealthResponse:
    """Return service health.

    Args:
        use_case: Health check use case.

    Returns:
        HTTP health response.

    Raises:
        DomainError: If health status cannot be represented.

    """
    output = use_case.execute()
    return HealthResponse(
        service_id=output.service_id,
        name=output.name,
        healthy=output.healthy,
    )
