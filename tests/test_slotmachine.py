import pytest
from telegram import Update

import src.slotmachine as slotmachine


@pytest.fixture
def mock_bot(mocker):
    return mocker.AsyncMock()


@pytest.fixture
def mock_context(mocker):
    return mocker.Mock()


@pytest.fixture
def make_update(mocker, mock_bot):
    """Factory so each test can vary spin value / user / chat as needed."""

    def _make_update(*, dice_value=2, user_id=123, username="testuser", chat_id=456):
        mock_user = mocker.Mock(id=user_id)
        mock_user.username = username

        update = mocker.Mock(spec=Update)
        update.effective_message = mocker.Mock(dice=mocker.Mock(value=dice_value))
        update.effective_user = mock_user
        update.effective_chat = mocker.Mock(id=chat_id)
        update.get_bot = mocker.Mock(return_value=mock_bot)
        return update

    return _make_update


@pytest.mark.asyncio
async def test_check_spin_sends_loss_message(
    mocker, mock_bot, mock_context, make_update
):
    mock_handle_result = mocker.patch(
        "src.slotmachine.handle_result",
        new_callable=mocker.AsyncMock,
        return_value=slotmachine.SpinResult(won=False, message="loss message"),
    )

    update = make_update()

    await slotmachine.check_spin(update, mock_context)

    mock_handle_result.assert_awaited_once_with(
        spin_value=2,
        user_id=123,
        chat_id=456,
        username="testuser",
    )
    mock_bot.send_message.assert_awaited_once_with(
        chat_id=456,
        text="loss message",
        parse_mode=slotmachine.ParseMode.HTML,
    )


@pytest.mark.asyncio
async def test_check_spin_sends_nothing_on_loss(
    mocker, mock_bot, mock_context, make_update
):
    mock_handle_result = mocker.patch(
        "src.slotmachine.handle_result",
        new_callable=mocker.AsyncMock,
        return_value=slotmachine.SpinResult(won=False, message=None),
    )

    update = make_update()

    await slotmachine.check_spin(update, mock_context)

    mock_handle_result.assert_awaited_once_with(
        spin_value=2,
        user_id=123,
        chat_id=456,
        username="testuser",
    )
    mock_bot.send_message.assert_not_called()


@pytest.mark.asyncio
async def test_check_spin_sends_nothing_on_win(
    mocker, mock_bot, mock_context, make_update
):
    mock_handle_result = mocker.patch(
        "src.slotmachine.handle_result",
        new_callable=mocker.AsyncMock,
        return_value=slotmachine.SpinResult(won=True),
    )

    update = make_update(dice_value=1)

    await slotmachine.check_spin(update, mock_context)

    mock_handle_result.assert_awaited_once_with(
        spin_value=1,
        user_id=123,
        chat_id=456,
        username="testuser",
    )
    mock_bot.send_message.assert_not_called()


def test_checking_win():
    assert slotmachine._is_win(spin_value=1)  # bar bar bar
    assert not slotmachine._is_win(spin_value=2)


@pytest.mark.asyncio
async def test_handle_result_calls_handle_win(mocker):
    mocker.patch("src.slotmachine._is_win", new_callable=mocker.Mock, return_value=True)

    mock_handle_win = mocker.patch(
        "src.slotmachine._handle_win",
        new_callable=mocker.AsyncMock,
        return_value=slotmachine.SpinResult(won=True),
    )

    await slotmachine.handle_result(
        spin_value=1, user_id=123, chat_id=456, username="testuser"
    )

    mock_handle_win.assert_called_once_with(user_id=123, chat_id=456)


@pytest.mark.asyncio
async def test_handle_result_calls_handle_loss(mocker):
    mocker.patch(
        "src.slotmachine._is_win", new_callable=mocker.Mock, return_value=False
    )

    mock_handle_loss = mocker.patch(
        "src.slotmachine._handle_loss",
        new_callable=mocker.AsyncMock,
        return_value=slotmachine.SpinResult(won=False),
    )

    await slotmachine.handle_result(
        spin_value=2, user_id=123, chat_id=456, username="testuser"
    )

    mock_handle_loss.assert_called_once_with(
        user_id=123, chat_id=456, username="testuser"
    )


@pytest.mark.asyncio
async def test_handle_win(mocker):
    mock_add_win = mocker.patch(
        "src.slotmachine.add_win", new_callable=mocker.AsyncMock
    )
    await slotmachine._handle_win(user_id=123, chat_id=456)
    mock_add_win.assert_called_once()


@pytest.mark.asyncio
async def test_handle_loss_with_message(mocker):
    mock_record = mocker.MagicMock()
    mock_record.__getitem__.return_value = True

    loss_message = "loss message"
    mock_loss_message = mocker.patch(
        "src.slotmachine.loss_streak_message",
        new_callable=mocker.Mock,
        return_value=loss_message,
    )

    mock_add_loss = mocker.patch(
        "src.slotmachine.add_loss",
        new_callable=mocker.AsyncMock,
        return_value=mock_record,
    )

    result = await slotmachine._handle_loss(
        user_id=123, chat_id=456, username="testuser"
    )
    mock_add_loss.assert_called_once()
    mock_loss_message.assert_called_once()

    assert result == slotmachine.SpinResult(won=False, message=loss_message)


@pytest.mark.asyncio
async def test_handle_loss_with_no_message(mocker):
    mock_record = mocker.MagicMock()
    mock_record.__getitem__.return_value = False

    mock_add_loss = mocker.patch(
        "src.slotmachine.add_loss",
        new_callable=mocker.AsyncMock,
        return_value=mock_record,
    )

    result = await slotmachine._handle_loss(
        user_id=123, chat_id=456, username="testuser"
    )

    mock_add_loss.assert_called_once()
    assert result == slotmachine.SpinResult(won=False)
