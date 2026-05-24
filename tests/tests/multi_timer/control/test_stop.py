from asyncio import sleep
from unittest.mock import Mock

from pytest import approx, mark

from aiotimer import MultiTimer
from aiotimer.duration import forever, once
from aiotimer.state.stopped_state import StoppedState


@mark.asyncio
async def test_callbacks_are_not_called_after_pausing() -> None:
    # Arrange
    on_complete = Mock()
    on_interval = Mock()
    timer = MultiTimer(once(0.1), on_complete, on_interval)

    # Act
    await timer.start()
    await timer.stop()
    await sleep(1)

    # Assert
    on_complete.assert_not_called()
    on_interval.assert_not_called()


@mark.asyncio
async def test_stop_does_not_reset_time_left() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    await timer.start()
    await sleep(1)
    await timer.stop()
    time_left = await timer.remaining

    # Assert
    assert time_left == approx(41, abs=0.1)


@mark.asyncio
async def test_time_left_is_not_decreasing_when_timer_is_stopd() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    await timer.start()
    await timer.stop()
    await sleep(1)
    time_left = await timer.remaining

    # Assert
    assert time_left == approx(42, abs=0.001)


@mark.asyncio
async def test_can_stop_the_timer_from_on_interval() -> None:
    # Arrange
    timer: MultiTimer

    async def on_interval() -> None:
        await timer.stop()

    timer = MultiTimer(forever(once(0.1)), on_interval_complete=on_interval)
    await timer.start()
    await sleep(1)

    # Act
    state = await timer.state

    # Assert
    assert state == StoppedState
