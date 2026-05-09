from asyncio import sleep
from unittest.mock import Mock

from pytest import approx, mark

from aiotimer import Timer
from aiotimer.interval import once


@mark.asyncio
async def test_view_after_instantiation() -> None:
    timer = Timer(once(42), Mock())

    time_left = await timer.view()

    assert time_left == 42


@mark.asyncio
async def test_view_after_running_for_some_time() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.run()
    await sleep(1)
    time_left = await timer.view()

    # Assert
    assert time_left == approx(41, abs=0.1)


@mark.asyncio
async def test_remaining_time_could_not_be_negative() -> None:
    # Arrange

    # A timer with very low precision, resulting in
    # the elapsed time being much larger than the duration.
    timer = Timer(once(0.1), Mock(), precision=0.5)

    # Act
    await timer.run()
    await sleep(1)
    time_left = await timer.view()

    # Assert
    assert time_left == 0
