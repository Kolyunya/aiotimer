from asyncio import sleep
from unittest.mock import Mock

from pytest import mark

from aiotimer import MultiTimer
from aiotimer.interval import once


@mark.asyncio
async def test_can_restart_sequential_timer_from_on_complete() -> None:
    """
    Attempt to restart a timer from a completion handler.

    Configure a timer for 0.1 seconds.
    Run it, then reset and restart 2 times.
    Expected a total of 3 calls to `on_complete`.
    """
    # Arrange
    timer: MultiTimer
    complete = Mock()

    async def on_complete() -> None:
        complete()
        if complete.call_count < 3:
            await timer.reset()
            await timer.start()

    timer = MultiTimer(once(0.1), on_complete)

    # Act
    await timer.start()
    await sleep(1)

    # Assert
    assert complete.call_count == 3
