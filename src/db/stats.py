from .connection import execute, query


async def add_user(user_id: int, chat_id: int):
    sql = """
        INSERT INTO stats
        (user_id, chat_id)
        VALUES ($1, $2)
        ON CONFLICT (user_id, chat_id) DO NOTHING
    """
    await execute(sql, user_id, chat_id)


async def add_win(user_id: int, chat_id: int):
    sql = """
        UPDATE stats
        SET wins = wins + 1
        WHERE user_id = $1 AND chat_id = $2
    """

    await execute(sql, user_id, chat_id)


async def add_loss(user_id: int, chat_id: int):
    sql = """
        UPDATE stats
        SET losses = losses + 1
        WHERE user_id = $1 AND chat_id = $2
    """

    await execute(sql, user_id, chat_id)


async def get_stats(user_id: int, chat_id: int):
    sql = """
        SELECT wins, losses
        FROM stats
        WHERE user_id = $1 AND chat_id = $2
    """

    return await query(sql, user_id, chat_id)
