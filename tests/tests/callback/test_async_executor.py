from asyncio import Event, sleep
from unittest.mock import Mock

from pytest import approx, mark

from aiotimer.callback import AsyncExecutor, Callback
from tests.support import stopwatch


@mark.asyncio
async def test_does_not_wait_for_callback_to_complete() -> None:
    # Arrange
    callback_is_called = Event()

    async def callback() -> None:
        callback_is_called.set()
        await sleep(1)

    executor = AsyncExecutor(
        error_handler=Mock(),
        error_factory=Mock(),
    )

    # Act
    async with stopwatch() as time:
        await executor.execute(Callback(callback), Mock())
        await callback_is_called.wait()

    # Assert
    assert time.elapsed == approx(0, abs=0.1)
