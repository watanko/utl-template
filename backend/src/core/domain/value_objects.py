from dataclasses import dataclass

from src.core.domain.exceptions import DomainValidationError


@dataclass(frozen=True, slots=True)
class ServiceName:
    """Validated service name.

    Attributes:
        value: Non-empty service name.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the service name.

        Returns:
            None.

        Raises:
            DomainValidationError: If the service name is blank.
        """

        if not self.value.strip():
            raise DomainValidationError("Service name must not be blank.")
