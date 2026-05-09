from asyncio import sleep
from unittest.mock import AsyncMock, Mock, call

from pytest import mark

from aiotimer import Timer
from aiotimer.event import IntervalCompleteEvent, TimerCompleteEvent
from aiotimer.interval import once, sequentially
from aiotimer.state import InitialState


@mark.asyncio
async def test_callbacks_are_not_called_after_resetting() -> None:
    # Arrange
    on_complete = Mock()
    on_interval = Mock()
    timer = Timer(once(0.1), on_complete, on_interval)

    # Act
    await timer.run()
    await timer.reset()
    await sleep(1)

    # Assert
    on_complete.assert_not_called()
    on_interval.assert_not_called()


@mark.asyncio
async def test_can_reset_a_running_timer() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.run()
    await timer.reset()
    state = await timer.view_state()

    # Assert
    assert state == InitialState


@mark.asyncio
async def test_can_reset_a_stopped_timer() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.run()
    await timer.pause()
    await timer.reset()
    state = await timer.view_state()

    # Assert
    assert state == InitialState


@mark.asyncio
async def test_reset_resets_time_left() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.run()
    await sleep(1)
    await timer.reset()
    time_left = await timer.view()

    # Assert
    assert time_left == 42


@mark.asyncio
async def test_time_left_is_not_decreasing_when_timer_is_reset() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.run()
    await timer.reset()
    await sleep(1)
    time_left = await timer.view()

    # Assert
    assert time_left == 42


@mark.asyncio
async def test_reset_resets_interval_number_and_duration() -> None:
    # Arrange
    async def on_timer_complete(event: TimerCompleteEvent) -> None:
        await event.timer.reset()
        await event.timer.run()

    on_interval_complete = AsyncMock()

    timer = Timer(
        sequentially(0.1, 0.2),
        on_timer_complete=on_timer_complete,
        on_interval_complete=on_interval_complete,
        precision=0.01,
    )

    # Act
    await timer.run()
    await sleep(1)

    # Assert
    on_interval_complete.assert_has_awaits([
        call(IntervalCompleteEvent(timer, 1, 0.1)),
        call(IntervalCompleteEvent(timer, 2, 0.2)),
        call(IntervalCompleteEvent(timer, 1, 0.1)),
        call(IntervalCompleteEvent(timer, 2, 0.2)),
        call(IntervalCompleteEvent(timer, 1, 0.1)),
        call(IntervalCompleteEvent(timer, 2, 0.2)),
    ])
