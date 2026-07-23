import pytest
import asyncpg
from src.db import database


@pytest.fixture(autouse=True)
def reset_pool_state():
    """Ensure the module-level global doesn't leak between tests."""
    database._conn_pool = None
    yield
    database._conn_pool = None


@pytest.fixture
def fake_conn(mocker):
    """A fake connection supporting async context-managed transactions."""
    conn = mocker.AsyncMock(spec=asyncpg.Connection)
    conn.transaction.return_value.__aenter__ = mocker.AsyncMock(return_value=None)
    conn.transaction.return_value.__aexit__ = mocker.AsyncMock(return_value=None)
    return conn


@pytest.fixture
def fake_pool(mocker, fake_conn):
    """A fake pool whose .acquire() yields fake_conn via async context manager."""
    pool = mocker.AsyncMock(spec=asyncpg.Pool)
    pool.acquire.return_value.__aenter__ = mocker.AsyncMock(return_value=fake_conn)
    pool.acquire.return_value.__aexit__ = mocker.AsyncMock(return_value=None)
    return pool


@pytest.mark.asyncio
async def test_init_postgres_creates_pool(mocker, fake_pool):
    create_pool_mock = mocker.patch(
        "src.db.database.asyncpg.create_pool",
        new_callable=mocker.AsyncMock,
        return_value=fake_pool,
    )
    mocker.patch(
        "src.db.database.Config.get_env",
        return_value=mocker.Mock(database_url="postgres://test"),
    )

    await database.init_postgres(application=mocker.Mock())
    
    create_pool_mock.assert_awaited_once_with(
        dsn="postgres://test", min_size=1, max_size=10
    )

    assert database._conn_pool is fake_pool


@pytest.mark.asyncio
async def test_init_postgres_logs_exception_on_initialization(mocker):   
    error_mock = mocker.patch("src.db.database.logger.error")
    mocker.patch("src.db.database.asyncpg.create_pool", side_effect=Exception("boom"))
    mocker.patch("src.db.database.Config.get_env", return_value=mocker.Mock(database_url="postgres://test"))

    with pytest.raises(Exception):
        await database.init_postgres(application=mocker.Mock())
    
    error_mock.assert_called_once()
    assert database._conn_pool is None
    assert "Error initializing PostgreSQL pool: boom" in error_mock.call_args.args[0]


@pytest.mark.asyncio
async def test_init_postgres_creates_stats_table(mocker, fake_pool, fake_conn):
    mocker.patch("src.db.database.asyncpg.create_pool", new_callable=mocker.AsyncMock, return_value=fake_pool)
    mocker.patch("src.db.database.Config.get_env", return_value=mocker.Mock(database_url="postgres://fake"))

    await database.init_postgres(application=mocker.Mock())

    fake_conn.execute.assert_awaited_once()
    executed_sql = fake_conn.execute.call_args[0][0]
    assert "CREATE TABLE IF NOT EXISTS stats" in executed_sql


@pytest.mark.asyncio
async def test_init_postgres_logs_exception_on_creating_stats_table(mocker, fake_pool, fake_conn):
    mocker.patch("src.db.database.asyncpg.create_pool", new_callable=mocker.AsyncMock, return_value=fake_pool)
    mocker.patch("src.db.database.Config.get_env", return_value=mocker.Mock(database_url="postgres://fake"))
    fake_pool.acquire.return_value.__aenter__.side_effect = Exception("boom")
    error_mock = mocker.patch("src.db.database.logger.error")

    with pytest.raises(Exception):
        await database.init_postgres(application=mocker.Mock())

    error_mock.assert_called_once()
    assert "Error creating stats table: boom" in error_mock.call_args.args[0]


@pytest.mark.asyncio
async def test_get_postgres_raises_when_conn_pool_uninitialized(mocker):
    database._conn_pool = None
    error_mock = mocker.patch("src.db.database.logger.error")

    with pytest.raises(ConnectionError):
        await database.get_postgres()

    error_mock.assert_called_once()
    assert "Connection pool is not initialized." in error_mock.call_args.args[0]


@pytest.mark.asyncio
async def test_get_postgres_returns_conn_pool_when_initialized(fake_pool):
    database._conn_pool = fake_pool
    assert await database.get_postgres() == fake_pool


@pytest.mark.asyncio
async def test_close_postgres_closes(fake_pool):
    database._conn_pool = fake_pool

    await database.close_postgres(application=None)

    fake_pool.close.assert_awaited_once()
    assert database._conn_pool is None


@pytest.mark.asyncio
async def test_close_postgres_raises_and_logs_on_error(mocker, fake_pool):
    database._conn_pool = fake_pool
    fake_pool.close = mocker.AsyncMock(side_effect=Exception("boom"))
    error_mock = mocker.patch("src.db.database.logger.error")

    with pytest.raises(Exception):
        await database.close_postgres(application=mocker.Mock())

    error_mock.assert_called_once()
    assert "Error closing PostgreSQL connection pool: boom" in error_mock.call_args.args[0]


@pytest.mark.asyncio
async def test_close_postgres_logs_when_conn_pool_uninitialized(mocker):
    database._conn_pool = None
    warning_mock = mocker.patch("src.db.database.logger.warning")

    await database.close_postgres(application=mocker.Mock())

    warning_mock.assert_called_once()
