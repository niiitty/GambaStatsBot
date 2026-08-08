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
