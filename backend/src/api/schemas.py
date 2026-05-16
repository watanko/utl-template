"""HTTP API schemas."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """HTTP response schema for health checks.

    Attributes:
        service_id: Stable service identifier.
        name: Service display name.
        healthy: Whether the service is available.

    """

    model_config = ConfigDict(frozen=True)

    service_id: UUID
    name: str
    healthy: bool
