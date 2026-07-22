from asyncio import sleep
from unittest.mock import AsyncMock, Mock

from pytest import approx, mark

from aiotimer import Timer
from aiotimer.duration.factory import forever, once
from aiotimer.event import IntervalCompleteEvent
from aiotimer.state import StoppedState


@mark.asyncio
async def test_callbacks_are_not_called_after_stopping() -> None:
    # Arrange
    on_timer_complete = Mock()
    on_interval_complete = Mock()
    timer = Timer(once(0.1), on_timer_complete, on_interval_complete)

    # Act
    await timer.start()
    await timer.stop()
    await sleep(1)

    # Assert
    on_timer_complete.assert_not_called()
    on_interval_complete.assert_not_called()


@mark.asyncio
async def test_stop_does_not_reset_remaining_time() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.start()
    await sleep(1)
    await timer.stop()

    remaining = timer.remaining

    # Assert
    assert remaining == approx(41, abs=0.1)


@mark.asyncio
async def test_remaining_time_is_not_decreasing_when_timer_is_stopped() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.start()
    await timer.stop()
    await sleep(1)

    remaining = timer.remaining

    # Assert
    assert remaining == approx(42, abs=0.001)


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_can_stop_from_on_interval_complete(await_callbacks: bool) -> None:
    # Arrange
    on_interval_complete = AsyncMock()
    on_error = AsyncMock()

    async def stop(event: IntervalCompleteEvent) -> None:
        await on_interval_complete()
        await event.timer.stop()

    timer = Timer(
        forever(once(0.1)),
        on_interval_complete=stop,
        on_error=on_error,
        await_callbacks=await_callbacks,
    )

    # Act
    await timer.start()
    await sleep(1)

    state = timer.state

    # Assert
    assert state == StoppedState
    on_interval_complete.assert_awaited_once()
    on_error.assert_not_awaited()
