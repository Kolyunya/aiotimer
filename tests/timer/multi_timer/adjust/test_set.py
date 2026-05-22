from asyncio import sleep
from unittest.mock import Mock

from pytest import mark, raises

from aiotimer import MultiTimer, Timer
from aiotimer.error import InvalidConfigurationError
from aiotimer.interval import once


@mark.asyncio
async def test_can_not_set_duration_to_negative_number() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    with raises(InvalidConfigurationError) as error:
        await timer.set(-1)

    # Assert
    assert str(error.value) == 'The duration must be a positive number or zero'


@mark.asyncio
async def test_can_set_duration_to_zero() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    await timer.set(0)
    duration = await timer.remaining

    # Assert
    assert duration == 0


@mark.asyncio
async def test_can_set_duration_to_positive_number() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    await timer.set(142)
    duration = await timer.remaining

    # Assert
    assert duration == 142


@mark.asyncio
async def test_can_change_duration_after_starting() -> None:
    # Arrange
    on_complete = Mock()
    timer = Timer(42, on_complete)

    # Act
    await timer.start()
    await timer.set(0.1)
    await sleep(1)

    # Assert
    on_complete.assert_called_once()
