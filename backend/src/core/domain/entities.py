from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class HealthStatus:
    """Service health entity.

    Attributes:
        service_id: Stable service identifier.
        name: Service display name.
        healthy: Whether the service is available.
    """

    service_id: UUID
    name: str
    healthy: bool
