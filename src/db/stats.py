from asyncpg import Record

from .connection import execute, insert, query


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
    """Increment wins, update longest loss streak, and reset the current loss streak.

    Longest streak is the greater of the stored longest streak or the current streak before reset.
    """
    sql = """
        UPDATE stats
        SET wins = wins + 1,
            longest_streak = GREATEST(longest_streak, current_streak),
            current_streak = 0
        WHERE user_id = $1 AND chat_id = $2
    """

    await execute(sql, user_id, chat_id)


async def add_loss(user_id: int, chat_id: int) -> Record | None:
    """Increment losses and current losing streak.

    Returns:
        `Record` containing:
        - `loss_streak_message` (bool): True when current streak is 10, 20, 30, ... . False otherwise.
        - `current_streak` (int): Updated loss streak.
    """
    sql = """
        UPDATE stats
        SET losses = losses + 1, current_streak = current_streak + 1
        WHERE user_id = $1 AND chat_id = $2
        RETURNING (new.current_streak >= 10
              AND (new.current_streak - 10) % 10 = 0)
              AS loss_streak_message,
              new.current_streak AS current_streak
    """

    return await insert(sql, user_id, chat_id)


async def get_stats(user_id: int, chat_id: int) -> Record | None:
    """Get statistics for a user in a chat.

    Returns:
        `Record` containing:
        - `wins` (int)
        - `losses` (int)
        - `longest_streak` (int): the greater of current_streak and longest_streak.
    """
    sql = """
        SELECT wins, losses, GREATEST(current_streak, longest_streak)
        FROM stats
        WHERE user_id = $1 AND chat_id = $2
    """

    stats = await insert(sql, user_id, chat_id)
    return stats if stats else None


async def get_chat_stats(chat_id: int) -> list[Record]:
    """Get statistics for all users in a chat.

    Returns:
        `Record` containing:
        - `wins` (int)
        - `losses` (int)
    """
    sql = """
        SELECT wins, losses
        FROM STATS
        WHERE chat_id = $1
    """

    return await query(sql, chat_id)
