from src.db import add_loss, add_win

_SLOT_MACHINE_WIN_VALUES = {
    1: ("bar", "bar", "bar"),
    22: ("grape", "grape", "grape"),
    43: ("lemon", "lemon", "lemon"),
    64: ("seven", "seven", "seven"),
}


def _is_win(spin_value: int) -> bool:
    """Check if spin is winning."""
    return spin_value in _SLOT_MACHINE_WIN_VALUES


async def _handle_win(user_id: int, chat_id: int) -> None:
    await add_win(user_id, chat_id)


async def _handle_loss(user_id: int, chat_id: int) -> None:
    await add_loss(user_id, chat_id)


async def handle_result(spin_value: int, user_id: int, chat_id: int) -> None:
    if _is_win(spin_value):
        await _handle_win(user_id, chat_id)
    else:
        await _handle_loss(user_id, chat_id)
