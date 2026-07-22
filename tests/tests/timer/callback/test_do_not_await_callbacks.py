from asyncio import Event, sleep

from _pytest.python_api import approx
from pytest import mark

from aiotimer import Timer
from aiotimer.duration.factory import once, repeatedly
from tests.support import stopwatch


@mark.asyncio
async def test_do_not_await_callbacks() -> None:
    # Arrange
    timer_complete = Event()

    async def on_timer_complete() -> None:
        timer_complete.set()

    async def on_interval_complete() -> None:
        await sleep(0.1)

    timer = Timer(
        repeatedly(once(0.1), 5),
        on_timer_complete,
        on_interval_complete,
        await_callbacks=False,
    )

    # Act
    async with stopwatch() as time:
        await timer.start()
        await timer_complete.wait()

    # Assert
    assert time.elapsed == approx(0.5, abs=0.1)
