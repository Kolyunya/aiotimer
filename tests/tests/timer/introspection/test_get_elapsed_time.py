from asyncio import sleep
from collections.abc import Iterable
from unittest.mock import Mock

from pytest import approx, mark

from aiotimer import Timer
from aiotimer.duration import once, sequentially


@mark.asyncio
async def test_get_elapsed_time_after_instantiation() -> None:
    timer = Timer(once(42), Mock())

    elapsed = timer.elapsed

    assert elapsed == 0


@mark.asyncio
@mark.parametrize(('intervals', 'sleep_for', 'elapsed_expected'), [
    ([1.0], 0.0, 0.0),
    ([1.0], 0.1, 0.1),
    ([0.1, 0.2], 0.2, 0.1),
    ([0.1, 0.2, 0.3], 0.4, 0.1),
])
async def test_get_elapsed_time_after_running_for_some_time(
        intervals: Iterable[float],
        sleep_for: float,
        elapsed_expected: float,
) -> None:
    # Arrange
    timer = Timer(sequentially(*intervals), Mock())

    # Act
    await timer.start()
    await sleep(sleep_for)

    elapsed = timer.elapsed

    # Assert
    assert elapsed == approx(elapsed_expected, abs=0.1)


@mark.asyncio
async def test_elapsed_time_must_not_be_greater_than_duration() -> None:
    # Arrange

    timer = Timer(once(0.1), Mock())

    # Act
    await timer.start()
    await sleep(1)

    elapsed = timer.elapsed

    # Assert
    assert elapsed == approx(0.1)
