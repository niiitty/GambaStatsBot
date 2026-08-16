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
📉 Pisin häviöputki: {longest_streak}
"""

NO_STATS_YET = "🎰 <i>Seuraa ensin pyöräytyksiä komennolla /begin</i>"

LOSS_STREAK_TEMPLATE = (
    "🎰 <i><b>{username}</b> on {current_streak} pelin häviöputkessa</i> 📉"
)

LEADERBOARD_TEMPLATE = """
🎰 {chat_title} top 10:

{stat_list}
    """


def stats_message(
    username: str, chat_title: str, wins: int, losses: int, longest_streak: int
) -> str:
    return STATS_TEMPLATE.format(
        username=escape(username),
        chat_title=escape(chat_title),
        wins=wins,
        losses=losses,
        win_percentage=escape(f"{_win_percentage(wins, losses)}"),
        longest_streak=longest_streak,
    )


def _win_percentage(wins: int, losses: int) -> str:
    if wins + losses <= 0:
        return "N/A"

    return str(round(wins / (wins + losses) * 100, ndigits=3))


def loss_streak_message(username: str, current_streak: int) -> str:
    return LOSS_STREAK_TEMPLATE.format(
        username=escape(username),
        current_streak=current_streak,
    )


def score(wins: int, losses: int) -> float:
    total = wins + losses
    if total <= 0:
        return 0.0

    winrate = wins / total
    confidence = total / (total + 50)
    return winrate * confidence


def create_leaderboard(stat_list: list[tuple[str, float]]) -> str:
    leaderboard: list[str] = []
    for pos, stat in enumerate(iterable=stat_list, start=1):
        leaderboard.append(f"{pos}. {escape(stat[0])}")

    return "\n".join(leaderboard)


def leaderboard_message(chat_title: str, stat_list: list[tuple[str, float]]) -> str:
    return LEADERBOARD_TEMPLATE.format(
        chat_title=chat_title,
        stat_list=create_leaderboard(stat_list),
    )
