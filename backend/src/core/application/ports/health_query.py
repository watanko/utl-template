from abc import ABC, abstractmethod

from src.core.domain.entities import HealthStatus


class HealthQuery(ABC):
    """Behavior contract for reading service health.

    Attributes:
        None.
    """

    @abstractmethod
    def get_status(self) -> HealthStatus:
        """Return current service health.

        Returns:
            Current service health status.

        Raises:
            DomainError: If health status cannot be represented.
        """
