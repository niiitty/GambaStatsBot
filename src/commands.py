"""Command handler callback functions."""

from collections.abc import Sequence

from asyncpg import Record
from loguru import logger
from telegram import Chat, Update
from telegram.constants import ParseMode

from src.db import add_user, get_chat_longest_streaks, get_chat_stats, get_stats
from src.messages import (
    ALREADY_TRACKING,
    BEGIN_TRACKING,
    HELP_MESSAGE,
    NO_STATS_YET,
    leaderboard_message,
    stats_message,
)


async def help(update: Update, _) -> None:
    message = update.effective_message
    if message is None:
        logger.warning("Message missing for help, ignoring.")
        return

    await message.reply_text(
        text=HELP_MESSAGE,
        parse_mode=ParseMode.HTML,
    )


async def begin(update: Update, _) -> None:
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


async def stats(update: Update, _) -> None:
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


def _score(wins: int, losses: int) -> float:
    total = wins + losses
    if total <= 0:
        return 0.0

    winrate = wins / total
    confidence = total / (total + 50)
    return winrate * confidence


async def _get_usernames[T: (int, float)](
    chat: Chat, stats: Sequence[tuple[int, T]]
) -> list[tuple[str, T]]:
    usernames = []
    for user in stats:
        member = await chat.get_member(user_id=user[0])
        username = (
            member.user.username
            if member.user.username is not None
            else member.user.first_name
        )
        usernames.append((username, user[1]))

    return usernames


async def leaderboard(update: Update, _) -> None:
    message = update.effective_message
    chat = update.effective_chat
    if message is None or chat is None or chat.title is None:
        logger.warning("Message, user, or chat missing for stats, ignoring.")
        return

    stats: list[Record] = await get_chat_stats(chat_id=chat.id)
    stat_list: list[tuple[int, float]] = [
        (record["user_id"], _score(wins=record["wins"], losses=record["losses"]))
        for record in stats
    ]
    stat_list.sort(key=lambda x: x[1], reverse=True)

    stat_usernames = await _get_usernames(chat=chat, stats=stat_list[0:10])

    longest_streaks: list[Record] = await get_chat_longest_streaks(chat_id=chat.id)
    longest_streaks_list: list[tuple[int, int]] = [
        (record["user_id"], record["longest_streak"]) for record in longest_streaks
    ]
    longest_streaks_list.sort(key=lambda x: x[1], reverse=True)

    streak_usernames = await _get_usernames(chat=chat, stats=longest_streaks_list[0:10])

    await message.reply_text(
        text=leaderboard_message(
            chat_title=chat.title,
            stat_list=stat_usernames,
            longest_streaks=streak_usernames,
        ),
        parse_mode=ParseMode.HTML,
    )
