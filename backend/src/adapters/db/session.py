from collections.abc import Iterator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


class SessionFactory:
    """SQLAlchemy session factory.

    Attributes:
        engine: SQLAlchemy engine.
        maker: Configured sessionmaker.
    """

    def __init__(self, database_url: str) -> None:
        """Initialize the session factory.

        Args:
            database_url: SQLAlchemy database URL.

        Returns:
            None.
        """

        self.engine: Engine = create_engine(database_url)
        self.maker: sessionmaker[Session] = sessionmaker(bind=self.engine)

    def create(self) -> Iterator[Session]:
        """Create a database session context.

        Returns:
            Iterator yielding an open SQLAlchemy session.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: If session creation or close fails.
        """

        with self.maker() as session:
            yield session
