from src.core.application.dto import HealthCheckOutput
from src.core.application.ports.health_query import HealthQuery


class GetHealth:
    """Use case for retrieving service health.

    Attributes:
        health_query: Port used to read service health.
    """

    def __init__(self, health_query: HealthQuery) -> None:
        """Initialize the use case.

        Args:
            health_query: Port used to read service health.

        Returns:
            None.
        """

        self.health_query = health_query

    def execute(self) -> HealthCheckOutput:
        """Run the health check.

        Returns:
            Health check output DTO.

        Raises:
            DomainError: If the health status is invalid.
        """

        status = self.health_query.get_status()
        return HealthCheckOutput(
            service_id=status.service_id,
            name=status.name,
            healthy=status.healthy,
        )
