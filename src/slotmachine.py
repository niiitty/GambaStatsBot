"""Handlers and logic for the slot machine."""

from dataclasses import dataclass

from loguru import logger
from telegram import Update
from telegram.constants import ParseMode

from src.db import add_loss, add_win
from src.messages import loss_streak_message

_SLOT_MACHINE_WIN_VALUES = {
    1: ("bar", "bar", "bar"),
    22: ("grape", "grape", "grape"),
    43: ("lemon", "lemon", "lemon"),
    64: ("seven", "seven", "seven"),
}


@dataclass
class SpinResult:
    won: bool
    message: str | None = None


async def check_spin(update: Update, _) -> None:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot = update.get_bot()
    if (
        message is None
        or message.dice is None
        or user is None
        or user.username is None
        or chat is None
    ):
        logger.warning("Message, user, or chat missing for check_spin, ignoring.")
        return

    result: SpinResult = await handle_result(
        spin_value=message.dice.value,
        user_id=user.id,
        chat_id=chat.id,
        username=user.username,
    )

    if not result.won:
        if result.message is None:
            return
        await bot.send_message(
            chat_id=chat.id,
            text=result.message,
            parse_mode=ParseMode.HTML,
        )


async def handle_result(
    spin_value: int, user_id: int, chat_id: int, username: str
) -> SpinResult:
    if _is_win(spin_value):
        return await _handle_win(user_id=user_id, chat_id=chat_id)
    return await _handle_loss(user_id=user_id, chat_id=chat_id, username=username)


def _is_win(spin_value: int) -> bool:
    """Check if spin is winning."""
    return spin_value in _SLOT_MACHINE_WIN_VALUES


async def _handle_win(user_id: int, chat_id: int) -> SpinResult:
    await add_win(user_id=user_id, chat_id=chat_id)
    return SpinResult(won=True)


async def _handle_loss(user_id: int, chat_id: int, username: str) -> SpinResult:
    result = await add_loss(user_id=user_id, chat_id=chat_id)
    if result is None:
        return SpinResult(won=False)

    if result["loss_streak_message"]:
        current_streak: int = result["current_streak"]
        return SpinResult(
            won=False,
            message=loss_streak_message(
                username=username, current_streak=current_streak
            ),
        )

    return SpinResult(won=False)
