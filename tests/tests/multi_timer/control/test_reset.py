from asyncio import sleep
from unittest.mock import AsyncMock, Mock

from pytest import mark

from aiotimer import MultiTimer
from aiotimer.duration import once, sequentially
from aiotimer.event import IntervalCompleteEvent, TimerCompleteEvent
from aiotimer.state import InitialState
from tests.support.callback import EventData, assert_callback_awaited


@mark.asyncio
async def test_callbacks_are_not_called_after_resetting() -> None:
    # Arrange
    on_complete = Mock()
    on_interval = Mock()
    timer = MultiTimer(once(0.1), on_complete, on_interval)

    # Act
    await timer.start()
    await timer.reset()
    await sleep(1)

    # Assert
    on_complete.assert_not_called()
    on_interval.assert_not_called()


@mark.asyncio
async def test_can_reset_a_running_timer() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    await timer.start()
    await timer.reset()
    state = await timer.state

    # Assert
    assert state == InitialState


@mark.asyncio
async def test_can_reset_a_stopped_timer() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    await timer.start()
    await timer.stop()
    await timer.reset()
    state = await timer.state

    # Assert
    assert state == InitialState


@mark.asyncio
async def test_reset_resets_time_left() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    await timer.start()
    await sleep(1)
    await timer.reset()
    time_left = await timer.remaining

    # Assert
    assert time_left == 42


@mark.asyncio
async def test_time_left_is_not_decreasing_when_timer_is_reset() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    await timer.start()
    await timer.reset()
    await sleep(1)
    time_left = await timer.remaining

    # Assert
    assert time_left == 42


@mark.asyncio
async def test_reset_resets_interval_number_and_duration() -> None:
    # Arrange
    async def on_timer_complete(event: TimerCompleteEvent) -> None:
        await event.timer.reset()
        await event.timer.start()

    on_interval_complete = AsyncMock()

    timer = MultiTimer(
        sequentially(0.1, 0.2),
        on_timer_complete=on_timer_complete,
        on_interval_complete=on_interval_complete,
    )

    # Act
    await timer.start()
    await sleep(1)

    # Assert
    assert_callback_awaited(on_interval_complete, [
        EventData(IntervalCompleteEvent, {
            'timer': timer,
            'interval_number': 1,
            'interval_duration': 0.1,
        }),
        EventData(IntervalCompleteEvent, {
            'timer': timer,
            'interval_number': 2,
            'interval_duration': 0.2,
        }),
        EventData(IntervalCompleteEvent, {
            'timer': timer,
            'interval_number': 1,
            'interval_duration': 0.1,
        }),
        EventData(IntervalCompleteEvent, {
            'timer': timer,
            'interval_number': 2,
            'interval_duration': 0.2,
        }),
        EventData(IntervalCompleteEvent, {
            'timer': timer,
            'interval_number': 1,
            'interval_duration': 0.1,
        }),
        EventData(IntervalCompleteEvent, {
            'timer': timer,
            'interval_number': 2,
            'interval_duration': 0.2,
        }),
    ])
