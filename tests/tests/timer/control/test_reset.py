from asyncio import sleep
from unittest.mock import AsyncMock, Mock

from pytest import mark

from aiotimer import Timer
from aiotimer.duration import forever, once, sequentially
from aiotimer.event import IntervalCompleteEvent, TimerCompleteEvent
from aiotimer.state import InitialState
from tests.support import EventData, assert_callback_awaited


@mark.asyncio
async def test_callbacks_are_not_called_after_resetting() -> None:
    # Arrange
    on_complete = Mock()
    on_interval = Mock()
    timer = Timer(once(0.1), on_complete, on_interval)

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
    timer = Timer(once(42), Mock())

    # Act
    await timer.start()
    await timer.reset()
    state = await timer.state

    # Assert
    assert state == InitialState


@mark.asyncio
async def test_can_reset_a_stopped_timer() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.start()
    await timer.stop()
    await timer.reset()
    state = await timer.state

    # Assert
    assert state == InitialState


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_can_reset_from_on_interval_complete(await_callbacks: bool) -> None:
    # Arrange
    on_interval_complete = AsyncMock()
    on_error = AsyncMock()

    async def reset(event: IntervalCompleteEvent) -> None:
        await on_interval_complete()
        await event.timer.reset()

    timer = Timer(
        forever(once(0.1)),
        on_interval_complete=reset,
        on_error=on_error,
        await_callbacks=await_callbacks,
    )

    # Act
    await timer.start()
    await sleep(1)

    # Assert
    assert await timer.state == InitialState
    on_interval_complete.assert_awaited_once()
    on_error.assert_not_awaited()


@mark.asyncio
async def test_reset_resets_time_left() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

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
    timer = Timer(once(42), Mock())

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

    timer = Timer(
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
