import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context

# Importa o Base e os models para o Alembic saber quais tabelas criar
from app.db.base import Base
import app.db.models  # garante que Job (e futuros models) são registrados

# Importa as settings para pegar a DATABASE_URL do .env
from app.config import settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Diz ao Alembic quais tabelas monitorar para autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    # Modo offline: gera SQL sem conectar no banco
    # Útil para revisar o SQL antes de aplicar
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    # Modo online: conecta no banco e aplica as migrations
    # Usa engine async porque nosso projeto é todo async
    engine = create_async_engine(settings.DATABASE_URL, poolclass=pool.NullPool)

    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
            )
        )
        await conn.run_sync(lambda _: context.run_migrations())

    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    # asyncio.run() porque o Alembic não é async nativamente
    # precisamos "empurrar" a coroutine para o event loop
    asyncio.run(run_migrations_online())