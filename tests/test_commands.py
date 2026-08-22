import pytest

import src.commands as commands


def test_score_returns_correct_value():
    wins = 1
    losses = 2

    score = commands._score(wins=wins, losses=losses)

    assert score == pytest.approx(expected=0.018867924)


def test_score_returns_zero_with_no_games():
    wins = 0
    losses = 0

    score = commands._score(wins=wins, losses=losses)

    assert score == 0.0
