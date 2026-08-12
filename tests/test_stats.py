import pytest

import src.db.stats as stats


@pytest.mark.asyncio
async def test_add_user_executes_insert_statement(mocker):
    execute_mock = mocker.patch("src.db.stats.insert", new_callable=mocker.AsyncMock)

    await stats.add_user(1, 2)

    execute_mock.assert_awaited_once()
    sql = execute_mock.call_args.args[0]
    assert "INSERT INTO stats" in sql
    assert "(user_id, chat_id)" in sql
    assert "ON CONFLICT (user_id, chat_id) DO NOTHING" in sql
    assert execute_mock.call_args.args[1:] == (1, 2)


@pytest.mark.asyncio
async def test_add_win_executes_update_statement(mocker):
    execute_mock = mocker.patch("src.db.stats.execute", new_callable=mocker.AsyncMock)

    await stats.add_win(3, 4)

    execute_mock.assert_awaited_once()
    sql = execute_mock.call_args.args[0]
    assert "UPDATE stats" in sql
    assert "SET wins = wins + 1" in sql
    assert "WHERE user_id = $1 AND chat_id = $2" in sql
    assert execute_mock.call_args.args[1:] == (3, 4)


@pytest.mark.asyncio
async def test_add_loss_executes_update_statement(mocker):
    execute_mock = mocker.patch("src.db.stats.insert", new_callable=mocker.AsyncMock)

    await stats.add_loss(5, 6)

    execute_mock.assert_awaited_once()
    sql = execute_mock.call_args.args[0]
    assert "UPDATE stats" in sql
    assert "SET losses = losses + 1" in sql
    assert "WHERE user_id = $1 AND chat_id = $2" in sql
    assert execute_mock.call_args.args[1:] == (5, 6)


@pytest.mark.asyncio
async def test_get_stats_queries_stats_for_user_and_chat(mocker):
    insert_result = [(7, 8)]
    insert_mock = mocker.patch(
        "src.db.stats.insert",
        new_callable=mocker.AsyncMock,
        return_value=insert_result,
    )

    result = await stats.get_stats(9, 10)

    assert result == insert_result
    insert_mock.assert_awaited_once()
    sql = insert_mock.call_args.args[0]
    assert "SELECT wins, losses" in sql
    assert "FROM stats" in sql
    assert "WHERE user_id = $1 AND chat_id = $2" in sql
    assert insert_mock.call_args.args[1:] == (9, 10)


@pytest.mark.asyncio
async def test_get_chat_stats_returns_every_user(mocker):
    query_result = []
    query_mock = mocker.patch(
        "src.db.stats.query", new_callable=mocker.AsyncMock, return_value=query_result
    )

    await stats.get_chat_stats(chat_id=123)
    query_mock.assert_called_once()
