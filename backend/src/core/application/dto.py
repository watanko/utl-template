"""Application data transfer objects."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class HealthCheckOutput:
    """Health check use-case output.

    Attributes:
        service_id: Stable service identifier.
        name: Service display name.
        healthy: Whether the service is available.

    """

    service_id: UUID
    name: str
    healthy: bool
