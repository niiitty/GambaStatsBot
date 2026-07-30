"""Command handler callback functions."""

from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

from src.db import add_user, get_stats


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        logger.warning("Message missing for help, ignoring.")
        return

    await message.reply_text(
        """
    🎰 Komennot:

    /help \\- Tulosta tämä viesti

    /begin \\- Ala seuraamaan voittoja ja häviöitä\\. Tämän jälkeen botti laskee kaikki pyöräytykset\\.
    /stats \\- Tulosta tilastosi
    """,
        parse_mode="MarkdownV2",
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

    response = await add_user(user_id, chat_id)
    if response:
        await message.reply_text(
            "🎰 _Lisäät kolikon\\.\\.\\._", parse_mode="MarkdownV2"
        )
    else:
        await message.reply_text(
            "🎰 _Pyöräytyksesi lasketaan jo\\._", parse_mode="MarkdownV2"
        )


def _win_percentage(wins: int, losses: int) -> str:
    if wins + losses <= 0:
        return "N/A"

    perc = str(round(wins / (wins + losses), 2))
    return perc.replace(".", "\\.")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    if message is None or user is None or chat is None:
        logger.warning("Message, user, or chat missing for stats, ignoring.")
        return

    user_id = user.id
    chat_id = chat.id

    stats = await get_stats(user_id, chat_id)
    if stats:
        wins, losses = stats
        await message.reply_text(
            f"""
            🎰**{user.username}** tilastot ryhmässä {chat.title}:

            🏆 Voitot: {wins}

            💸 Häviöt: {losses}

            🍒 Voitto\\-%: {_win_percentage(wins, losses)} %
            """,
            parse_mode="MarkdownV2",
        )
    else:
        await message.reply_text(
            """
            🎰 _Seuraa ensin pyöräytyksiä komennolla `\\begin`._
            """
        )
