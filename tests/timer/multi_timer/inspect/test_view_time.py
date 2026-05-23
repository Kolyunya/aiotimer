from asyncio import sleep
from unittest.mock import Mock

from pytest import approx, mark

from aiotimer import MultiTimer
from aiotimer.interval import once


@mark.asyncio
async def test_view_after_instantiation() -> None:
    timer = MultiTimer(once(42), Mock())

    time_left = await timer.remaining

    assert time_left == 42


@mark.asyncio
async def test_view_after_running_for_some_time() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    await timer.start()
    await sleep(1)
    time_left = await timer.remaining

    # Assert
    assert time_left == approx(41, abs=0.01)


@mark.asyncio
async def test_remaining_time_could_be_negative() -> None:
    # Arrange

    timer = MultiTimer(once(0.1), Mock())

    # Act
    await timer.start()
    await sleep(1)
    time_left = await timer.remaining

    # Assert
    assert time_left == approx(0, abs=0.01)
