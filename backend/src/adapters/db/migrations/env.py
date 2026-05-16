"""Alembic migration runtime configuration."""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from src.adapters.db.sqlalchemy_models import Base
from src.config import get_settings

config = context.config
target_metadata = Base.metadata


class AlembicConfigSectionError(RuntimeError):
    """Raised when Alembic cannot provide the active config section."""


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def get_database_url() -> str:
    """Return the database URL used by Alembic.

    Returns:
        SQLAlchemy database URL.

    Raises:
        pydantic.ValidationError: If settings are invalid.

    """
    return get_settings().database_url


def run_migrations_offline() -> None:
    """Run migrations without creating an Engine.

    Returns:
        None.

    Raises:
        alembic.util.exc.CommandError: If Alembic cannot configure the migration context.

    """
    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations with an Engine.

    Returns:
        None.

    Raises:
        sqlalchemy.exc.SQLAlchemyError: If database connection or migration execution fails.

    """
    section = config.get_section(config.config_ini_section)
    if section is None:
        raise AlembicConfigSectionError

    section["sqlalchemy.url"] = get_database_url()
    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
