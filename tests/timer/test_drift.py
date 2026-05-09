from asyncio import sleep
from time import perf_counter

from pytest import approx, mark

from aiotimer import Timer
from aiotimer.interval import once, repeatedly


@mark.asyncio
@mark.slow
async def test_one_long_interval_produces_no_drift() -> None:
    # Arrange
    timer_complete = False
    time_start = perf_counter()

    # Assert #1
    async def on_complete() -> None:
        nonlocal timer_complete
        timer_complete = True

        time_end = perf_counter()
        duration_actual = time_end - time_start
        assert duration_actual == approx(60, abs=0.1)

    # Act
    timer = Timer(once(60), on_complete)
    await timer.run()

    # Assert #2
    await sleep(60 + 1)
    assert timer_complete


@mark.asyncio
@mark.slow
@mark.skip(reason='Not implemented yet')
async def test_many_short_intervals_produce_no_drift() -> None:
    # Arrange
    timer_is_complete = False
    time_start = perf_counter()

    # Assert #1
    async def on_complete() -> None:
        nonlocal timer_is_complete
        timer_is_complete = True

        time_end = perf_counter()
        duration_actual = time_end - time_start
        assert duration_actual == approx(60, abs=1)

    # Act
    timer = Timer(repeatedly(once(1), 60), on_complete)
    await timer.run()

    # Assert #2
    await sleep(60 + 1)
    assert timer_is_complete
