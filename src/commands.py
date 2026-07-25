"""Command handler callback functions."""

from telegram import Update
from telegram.ext import ContextTypes

from src.db import add_user, get_stats


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        return

    await message.reply_text(
        """
    Komennot:

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

    user_id = user.id
    chat_id = chat.id

    await add_user(user_id, chat_id)
    await message.reply_text(
        "🎰 _Tervetuloa pelaamaan\\.\\.\\._", parse_mode="MarkdownV2"
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

    user_id = user.id
    chat_id = chat.id

    wins, losses = await get_stats(user_id, chat_id)
    await message.reply_text(
        f"""
        🍒**{user.username}** tilastot ryhmässä {chat.title}:
        
        🏆 Voitot: {wins}

        💸 Häviöt: {losses}
        
        Voitto\\-%: {_win_percentage(wins, losses)} %
        """,
        parse_mode="MarkdownV2",
    )
