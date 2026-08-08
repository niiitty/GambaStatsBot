import pytest

import src.slotmachine as slotmachine


def test_checking_win():
    assert slotmachine._is_win(spin_value=1)  # bar bar bar
    assert not slotmachine._is_win(spin_value=2)


@pytest.mark.asyncio
async def test_handle_win(mocker):
    mock_add_win = mocker.patch(
        "src.slotmachine.add_win", new_callable=mocker.AsyncMock
    )
    await slotmachine._handle_win(1, 1)
    mock_add_win.assert_called_once()


@pytest.mark.asyncio
async def test_handle_loss(mocker):
    mock_add_loss = mocker.patch(
        "src.slotmachine.add_loss", new_callable=mocker.AsyncMock
    )
    await slotmachine._handle_loss(1, 1, "test")
    mock_add_loss.assert_called_once()
