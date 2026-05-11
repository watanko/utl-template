from uuid import UUID

from src.core.application.ports.health_query import HealthQuery
from src.core.domain.entities import HealthStatus


class StaticHealthQuery(HealthQuery):
    """In-memory health query implementation.

    Attributes:
        service_name: Service display name.
    """

    def __init__(self, service_name: str) -> None:
        """Initialize the query.

        Args:
            service_name: Service display name.

        Returns:
            None.
        """

        self.service_name = service_name

    def get_status(self) -> HealthStatus:
        """Return static service health.

        Returns:
            Current service health status.

        Raises:
            DomainValidationError: If the configured service name is invalid.
        """

        return HealthStatus(
            service_id=UUID("00000000-0000-4000-8000-000000000001"),
            name=self.service_name,
            healthy=True,
        )
