from unittest.mock import AsyncMock, Mock, call

from pytest import mark

from aiotimer.callback import Callback
from aiotimer.event import TimerEvent


@mark.asyncio
async def test_callback_is_not_set() -> None:
    # Arrange
    callback = Callback[TimerEvent](None)

    # Act
    is_set = callback.is_set

    # Assert
    assert is_set is False


@mark.asyncio
async def test_callback_is_set() -> None:
    # Arrange
    callback = Callback[TimerEvent](Mock())

    # Act
    is_set = callback.is_set

    # Assert
    assert is_set is True


@mark.asyncio
async def test_sync_function_is_called_once() -> None:
    # Arrange
    event = Mock()
    event_handler = Mock()
    callback = Callback[TimerEvent](event_handler)

    # Act
    await callback(event)

    # Assert
    event_handler.assert_called_once_with(event)


@mark.asyncio
async def test_sync_function_is_called_thrice() -> None:
    # Arrange
    event_1 = Mock()
    event_2 = Mock()
    event_3 = Mock()
    event_handler = Mock()
    callback = Callback[TimerEvent](event_handler)

    # Act
    await callback(event_1)
    await callback(event_2)
    await callback(event_3)

    # Assert
    assert event_handler.call_count == 3
    event_handler.assert_has_calls([
        call(event_1),
        call(event_2),
        call(event_3),
    ])


@mark.asyncio
async def test_async_function_is_awaited_once() -> None:
    # Arrange
    event = Mock()
    event_handler = AsyncMock()
    callback = Callback[TimerEvent](event_handler)

    # Act
    await callback(event)

    # Assert
    event_handler.assert_called_once_with(event)


@mark.asyncio
async def test_async_function_is_awaited_thrice() -> None:
    # Arrange
    event_1 = Mock()
    event_2 = Mock()
    event_3 = Mock()
    event_handler = AsyncMock()
    callback = Callback[TimerEvent](event_handler)

    # Act
    await callback(event_1)
    await callback(event_2)
    await callback(event_3)

    # Assert
    assert event_handler.call_count == 3
    event_handler.assert_has_awaits([
        call(event_1),
        call(event_2),
        call(event_3),
    ])
