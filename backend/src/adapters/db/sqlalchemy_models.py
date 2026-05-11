from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models.

    Attributes:
        metadata: SQLAlchemy table metadata inherited from DeclarativeBase.
    """
