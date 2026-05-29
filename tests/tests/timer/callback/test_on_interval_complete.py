from asyncio import sleep
from unittest.mock import AsyncMock, Mock

from pytest import mark

from aiotimer import Timer
from aiotimer.duration import sequentially, thrice
from aiotimer.event import IntervalCompleteEvent
from tests.support import EventData, assert_callback_awaited


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_sync_callback_is_called_after_interval_completion(await_callbacks: bool) -> None:
    # Arrange
    on_interval = Mock()
    timer = Timer(
        thrice(0.1),
        on_interval_complete=on_interval,
        await_callbacks=await_callbacks,
    )

    # Act
    await timer.start()
    await sleep(1)

    # Assert
    assert on_interval.call_count == 3


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_async_callback_is_awaited_after_interval_completion(await_callbacks: bool) -> None:
    # Arrange
    on_interval = AsyncMock()
    timer = Timer(
        thrice(0.1),
        on_interval_complete=on_interval,
        await_callbacks=await_callbacks,
    )

    # Act
    await timer.start()
    await sleep(1)

    # Assert
    assert on_interval.await_count == 3


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_interval_index_and_duration_are_passed_to_on_interval(await_callbacks: bool) -> None:
    # Arrange
    on_interval = AsyncMock()
    timer = Timer(
        sequentially(0.3, 0.2, 0.1),
        on_interval_complete=on_interval,
        await_callbacks=await_callbacks,
    )

    # Act
    await timer.start()
    await sleep(1)

    # Assert
    assert_callback_awaited(on_interval, [
        EventData(IntervalCompleteEvent, {
            'timer': timer,
            'interval_number': 1,
            'interval_duration': 0.3,
        }),
        EventData(IntervalCompleteEvent, {
            'timer': timer,
            'interval_number': 2,
            'interval_duration': 0.2,
        }),
        EventData(IntervalCompleteEvent, {
            'timer': timer,
            'interval_number': 3,
            'interval_duration': 0.1,
        }),
    ])
