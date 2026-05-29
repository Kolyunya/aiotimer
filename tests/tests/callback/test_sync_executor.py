from asyncio import Event, sleep
from unittest.mock import Mock

from pytest import approx, mark

from aiotimer.callback import Callback, SyncExecutor
from tests.support import stopwatch


@mark.asyncio
async def test_does_wait_for_callback_to_complete() -> None:
    # Arrange
    callback_is_called = Event()

    async def callback() -> None:
        await sleep(1)
        callback_is_called.set()

    executor = SyncExecutor(
        error_handler=Mock(),
        error_factory=Mock(),
    )

    # Act
    async with stopwatch() as time:
        await executor(Callback(callback), Mock())

    # Assert
    assert callback_is_called.is_set()
    assert time.elapsed == approx(1, abs=0.1)
