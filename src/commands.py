"""Command handler callback functions."""

from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from src.db import add_user, get_stats
from src.messages import (
    HELP_MESSAGE,
    BEGIN_TRACKING,
    ALREADY_TRACKING,
    stats_message,
    NO_STATS_YET,
)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        logger.warning("Message missing for help, ignoring.")
        return

    await message.reply_text(
        text=HELP_MESSAGE,
        parse_mode=ParseMode.HTML,
    )


async def begin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    if message is None or user is None or chat is None:
        logger.warning("Message, user, or chat missing for begin, ignoring.")
        return

    user_id = user.id
    chat_id = chat.id

    response: bool = await add_user(user_id, chat_id)
    if response:
        await message.reply_text(text=BEGIN_TRACKING, parse_mode=ParseMode.HTML)
    else:
        await message.reply_text(text=ALREADY_TRACKING, parse_mode=ParseMode.HTML)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    if message is None or user is None or chat is None:
        logger.warning("Message, user, or chat missing for stats, ignoring.")
        return

    user_id = user.id
    chat_id = chat.id

    if user.username is None or chat.title is None:
        return

    stats = await get_stats(user_id, chat_id)
    if stats:
        wins, losses, longest_streak = stats
        await message.reply_text(
            text=stats_message(
                username=user.username,
                chat_title=chat.title,
                wins=wins,
                losses=losses,
                longest_streak=longest_streak,
            ),
            parse_mode=ParseMode.HTML,
        )
    else:
        await message.reply_text(
            text=NO_STATS_YET,
            parse_mode=ParseMode.HTML,
        )
