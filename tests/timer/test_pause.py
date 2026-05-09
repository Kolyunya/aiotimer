from asyncio import sleep
from unittest.mock import Mock

from pytest import approx, mark

from aiotimer import Timer
from aiotimer.interval import forever, once
from aiotimer.state.stopped_state import StoppedState


@mark.asyncio
async def test_callbacks_are_not_called_after_pausing() -> None:
    # Arrange
    on_complete = Mock()
    on_interval = Mock()
    timer = Timer(once(0.1), on_complete, on_interval)

    # Act
    await timer.run()
    await timer.pause()
    await sleep(1)

    # Assert
    on_complete.assert_not_called()
    on_interval.assert_not_called()


@mark.asyncio
async def test_pause_does_not_reset_time_left() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.run()
    await sleep(1)
    await timer.pause()
    time_left = await timer.view()

    # Assert
    assert time_left == approx(41, abs=0.1)


@mark.asyncio
async def test_time_left_is_not_decreasing_when_timer_is_paused() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.run()
    await timer.pause()
    await sleep(1)
    time_left = await timer.view()

    # Assert
    assert time_left == 42


@mark.asyncio
async def test_can_pause_the_timer_from_on_interval() -> None:
    # Arrange
    timer: Timer

    async def on_interval() -> None:
        await timer.pause()

    timer = Timer(forever(once(0.1)), on_interval_complete=on_interval)
    await timer.run()
    await sleep(1)

    # Act
    state = await timer.view_state()

    # Assert
    assert state == StoppedState
