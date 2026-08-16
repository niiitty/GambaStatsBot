"""Helper functions to communicate with Postgres database."""

import asyncpg
from loguru import logger

from src.config import Config

_conn_pool: asyncpg.Pool | None = None


async def init_postgres(_) -> None:
    global _conn_pool
    try:
        logger.info("Initializing PostgreSQL connection pool...")

        _conn_pool = await asyncpg.create_pool(
            dsn=Config.get_env().database_url,
            min_size=1,
            max_size=10,
        )
        logger.info("PostgreSQL connection pool created successfully.")

    except Exception as e:
        logger.error(f"Error initializing PostgreSQL pool: {e}")
        raise
    try:
        async with _conn_pool.acquire() as conn:
            sql = """
            CREATE TABLE IF NOT EXISTS stats (
                user_id BIGINT NOT NULL,
                chat_id BIGINT NOT NULL,
                wins INTEGER NOT NULL DEFAULT 0,
                losses INTEGER NOT NULL DEFAULT 0,
                current_streak INTEGER NOT NULL DEFAULT 0,
                longest_streak INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (user_id, chat_id)
            );
            """
            async with conn.transaction():
                await conn.execute(sql)
            logger.info("Stats table ensured to exist")
    except Exception as e:
        logger.error(f"Error creating stats table: {e}")
        raise


async def get_postgres() -> asyncpg.Pool:
    global _conn_pool
    if not _conn_pool:
        logger.error("Connection pool is not initialized.")
        raise ConnectionError("PostgreSQL connection pool is not initialized.")
    return _conn_pool


async def close_postgres(_) -> None:
    global _conn_pool
    if _conn_pool:
        try:
            logger.info("Closing PostgreSQL connection pool...")
            await _conn_pool.close()
            _conn_pool = None
            logger.info("PostgreSQL connection pool closed successfully.")
        except Exception as e:
            logger.error(f"Error closing PostgreSQL connection pool: {e}")
            raise
    else:
        logger.warning("PostgreSQL connection pool was not initialized.")


async def execute(sql: str, *args) -> str:
    db_pool = await get_postgres()
    async with db_pool.acquire() as conn, conn.transaction():
        return await conn.execute(sql, *args)


async def insert(sql: str, *args) -> asyncpg.Record | None:
    db_pool = await get_postgres()
    async with db_pool.acquire() as conn, conn.transaction():
        return await conn.fetchrow(sql, *args)


async def query(sql: str, *args) -> list[asyncpg.Record]:
    db_pool = await get_postgres()
    async with db_pool.acquire() as conn, conn.transaction():
        return await conn.fetch(sql, *args)
