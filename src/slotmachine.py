"""Handlers and logic for the slot machine."""

from telegram import Update
from telegram.ext import ContextTypes

from src.db import add_loss, add_win

_SLOT_MACHINE_WIN_VALUES = {
    1: ("bar", "bar", "bar"),
    22: ("grape", "grape", "grape"),
    43: ("lemon", "lemon", "lemon"),
    64: ("seven", "seven", "seven"),
}


async def check_spin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    user_id = user.id
    chat_id = chat.id

    await handle_result(message.dice.value, user_id, chat_id)


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
