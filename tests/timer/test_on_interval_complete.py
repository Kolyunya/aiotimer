from asyncio import sleep
from unittest.mock import AsyncMock, Mock, call

from pytest import mark

from aiotimer import Timer
from aiotimer.event import IntervalCompleteEvent
from aiotimer.interval import sequentially, thrice


@mark.asyncio
async def test_sync_callback_is_called_after_interval_completion() -> None:
    # Arrange
    on_interval = Mock()
    timer = Timer(thrice(0.1), on_interval_complete=on_interval)

    # Act
    await timer.run()
    await sleep(1)

    # Assert
    assert on_interval.call_count == 3


@mark.asyncio
async def test_async_callback_is_awaited_after_interval_completion() -> None:
    # Arrange
    on_interval = AsyncMock()
    timer = Timer(thrice(0.1), on_interval_complete=on_interval)

    # Act
    await timer.run()
    await sleep(1)

    # Assert
    assert on_interval.await_count == 3


@mark.asyncio
async def test_interval_index_and_duration_are_passed_to_on_interval() -> None:
    # Arrange
    on_interval = AsyncMock()
    timer = Timer(sequentially(0.3, 0.2, 0.1), on_interval_complete=on_interval)

    # Act
    await timer.run()
    await sleep(1)

    # Assert
    assert on_interval.await_count == 3
    on_interval.assert_has_awaits([
        call(IntervalCompleteEvent(timer, 1, 0.3)),
        call(IntervalCompleteEvent(timer, 2, 0.2)),
        call(IntervalCompleteEvent(timer, 3, 0.1)),
    ])
