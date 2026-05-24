from asyncio import sleep
from time import perf_counter

from pytest import approx, mark

from aiotimer import MultiTimer
from aiotimer.interval import once, repeatedly


@mark.slow
@mark.asyncio
@mark.parametrize('duration', [60, 60 * 3, 60 * 5])
async def test_one_long_interval_produces_no_drift(duration: int) -> None:
    # Arrange
    timer_is_complete = False

    def on_complete() -> None:
        end_time = perf_counter()
        elapsed_time = end_time - start_time
        assert elapsed_time == approx(duration, abs=0.01)
        print(f'elapsed_time: {elapsed_time}')

        nonlocal timer_is_complete
        timer_is_complete = True

    timer = MultiTimer(
        once(duration),
        on_complete,
        await_callbacks=False,
    )

    start_time = perf_counter()

    # Act
    await timer.start()
    await sleep(duration + 0.01)

    # Assert
    assert timer_is_complete


@mark.asyncio
@mark.slow
@mark.parametrize('duration', [60, 60 * 3, 60 * 5])
async def test_many_short_intervals_produce_no_drift_profile(duration: int) -> None:
    # Arrange
    timer_is_complete = False

    def on_complete() -> None:
        end_time = perf_counter()
        elapsed_time = end_time - start_time
        assert elapsed_time == approx(duration, abs=1.00)
        print(f'elapsed_time: {elapsed_time}')

        nonlocal timer_is_complete
        timer_is_complete = True

    timer = MultiTimer(
        repeatedly(once(1), duration),
        on_complete,
        await_callbacks=False,
    )

    start_time = perf_counter()

    # Act
    await timer.start()
    await sleep(duration + 1.00)

    # Assert
    assert timer_is_complete
