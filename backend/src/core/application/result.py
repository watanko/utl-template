from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True, slots=True)
class Ok[T]:
    """Container for a successful external operation.

    Attributes:
        value: Successful result value.
    """

    value: T


@final
@dataclass(frozen=True, slots=True)
class Err[E]:
    """Container for a failed external operation.

    Attributes:
        error: Error value.
    """

    error: E


type Result[T, E] = Ok[T] | Err[E]
