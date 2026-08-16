import pytest

import src.messages as messages


def test_win_percentage_returns_na():
    assert messages._win_percentage(wins=0, losses=0) == "N/A"


def test_win_percentage_rounds_correctly():
    assert messages._win_percentage(wins=1, losses=2) == "33.333"


def test_stats_message_formats_properly():
    expected = """
🎰 <b>test_name</b> tilastot ryhmässä test_chat:

🏆 Voitot: 0
💸 Häviöt: 0

🍒 Voitto-%: N/A %
📉 Pisin häviöputki: 0
"""
    message = messages.stats_message(
        username="test_name", chat_title="test_chat", wins=0, losses=0, longest_streak=0
    )

    assert message == expected


def test_score_returns_correct_value():
    wins = 1
    losses = 2

    score = messages.score(wins=wins, losses=losses)

    assert score == pytest.approx(expected=0.018867924)


def test_score_returns_zero_with_no_games():
    wins = 0
    losses = 0

    score = messages.score(wins=wins, losses=losses)

    assert score == 0.0


def test_leaderboard_message_formats_correctly():
    expected = """
🎰 test_chat top 10:

1. user1
2. user2
3. user3
    """

    stat_list: list[tuple[str, float]] = [
        ("user1", 2.0),
        ("user2", 1.0),
        ("user3", 0.0),
    ]

    assert expected == messages.leaderboard_message(
        chat_title="test_chat", stat_list=stat_list
    )
