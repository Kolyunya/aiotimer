from asyncio import sleep
from collections.abc import Iterable
from unittest.mock import Mock

from pytest import approx, mark

from aiotimer import MultiTimer
from aiotimer.duration import once, sequentially


@mark.asyncio
async def test_get_remaining_time_after_instantiation() -> None:
    timer = MultiTimer(once(42), Mock())

    remaining = await timer.remaining

    assert remaining == 42


@mark.asyncio
@mark.parametrize(('intervals', 'sleep_for', 'remaining_expected'), [
    ([1.0], 0.0, 1.0),
    ([1.0], 0.1, 0.9),
    ([0.1, 0.2], 0.2, 0.1),
    ([0.1, 0.2, 0.3], 0.4, 0.2),
])
async def test_get_remaining_time_after_running_for_some_time(
        intervals: Iterable[float],
        sleep_for: float,
        remaining_expected: float,
) -> None:
    # Arrange
    timer = MultiTimer(sequentially(*intervals), Mock())

    # Act
    await timer.start()
    await sleep(sleep_for)
    remaining = await timer.remaining

    # Assert
    assert remaining == approx(remaining_expected, abs=0.01)


@mark.asyncio
async def test_remaining_time_must_not_be_negative() -> None:
    # Arrange

    timer = MultiTimer(once(0.1), Mock())

    # Act
    await timer.start()
    await sleep(1)
    remaining = await timer.remaining

    # Assert
    assert remaining == 0
