from html import escape

HELP_MESSAGE = """
🎰 Komennot:

/help - Tulosta tämä viesti.

/begin - Ala seuraamaan voittoja ja häviöitä.
/stats - Tulosta tilastosi.
"""

BEGIN_TRACKING = "🎰 <i>Gamba gamba</i>"

ALREADY_TRACKING = "🎰 <i>Pyöräytyksesi lasketaan jo</i>"

STATS_TEMPLATE = """
🎰 <b>{username}</b> tilastot ryhmässä {chat_title}:

🏆 Voitot: {wins}
💸 Häviöt: {losses}

🍒 Voitto-%: {win_percentage} %
"""

NO_STATS_YET = "🎰 <i>Seuraa ensin pyöräytyksiä komennolla /begin</i>"


def stats_message(username: str, chat_title: str, wins: int, losses: int) -> str:
    return STATS_TEMPLATE.format(
        username=escape(username),
        chat_title=escape(chat_title),
        wins=wins,
        losses=losses,
        win_percentage=escape(f"{_win_percentage(wins, losses)}"),
    )


def _win_percentage(wins: int, losses: int) -> str:
    if wins + losses <= 0:
        return "N/A"

    return str(round(wins / (wins + losses) * 100, ndigits=3))
