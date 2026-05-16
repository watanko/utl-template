"""Domain exceptions."""


class DomainError(Exception):
    """Base class for domain errors.

    Attributes:
        args: Error message values inherited from Exception.

    """


class DomainValidationError(DomainError):
    """Raised when domain value validation fails.

    Attributes:
        args: Error message values inherited from Exception.

    """


class BlankServiceNameError(DomainValidationError):
    """Raised when a service name is blank."""
