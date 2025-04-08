from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from app.models import user, task  # Импортируем модели для работы с метаданными
from app.database import Base  # Базовый класс для метаданных
from alembic import context
import os

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Используем DATABASE_URL из переменных окружения
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

# Интерпретируем конфигурационный файл для Python логирования.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata  # Используем метаданные из базы

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    # Получаем URL подключения из конфигурационного файла alembic.ini
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # Здесь начинаются миграции
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # Создаем движок подключения на основе конфигурации
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Здесь выполняем миграции, используя подключение
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        # Начинаем транзакцию для миграции
        with context.begin_transaction():
            context.run_migrations()


# Определяем, в каком режиме работают миграции
if context.is_offline_mode():
    run_migrations_offline()  # Если оффлайн, запускаем offline
else:
    run_migrations_online()  # В противном случае используем online
