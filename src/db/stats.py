from asyncpg import Record

from .connection import execute, query, insert


async def add_user(user_id: int, chat_id: int) -> bool:
    """Start tracking user's spins in given chat.

    Args:
        user_id (int): id of user
        chat_id (int): id of chat

    Returns:
        Boolean: True if user was added successfully, False if the user was already registered.
    """
    sql = """
        INSERT INTO stats (user_id, chat_id)
        VALUES ($1, $2)
        ON CONFLICT (user_id, chat_id) DO NOTHING
        RETURNING user_id
    """
    result = await insert(sql, user_id, chat_id)
    return bool(result)


async def add_win(user_id: int, chat_id: int) -> None:
    sql = """
        UPDATE stats
        SET wins = wins + 1
        WHERE user_id = $1 AND chat_id = $2
    """

    await execute(sql, user_id, chat_id)


async def add_loss(user_id: int, chat_id: int) -> None:
    sql = """
        UPDATE stats
        SET losses = losses + 1
        WHERE user_id = $1 AND chat_id = $2
    """

    await execute(sql, user_id, chat_id)


async def get_stats(user_id: int, chat_id: int) -> Record | None:
    sql = """
        SELECT wins, losses
        FROM stats
        WHERE user_id = $1 AND chat_id = $2
    """

    stats = await query(sql, user_id, chat_id)
    return stats if stats else None
