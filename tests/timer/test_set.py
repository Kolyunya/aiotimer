from unittest.mock import Mock

from pytest import mark, raises

from aiotimer import Timer
from aiotimer.error import InvalidConfigurationError
from aiotimer.interval import once


@mark.asyncio
async def test_can_not_set_duration_to_negative_number() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    with raises(InvalidConfigurationError) as error:
        await timer.set(-1)

    # Assert
    assert str(error.value) == 'The duration must be a positive number or zero'


@mark.asyncio
async def test_can_set_duration_to_zero() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.set(0)
    duration = await timer.view()

    # Assert
    assert duration == 0


@mark.asyncio
async def test_can_set_duration_to_positive_number() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.set(142)
    duration = await timer.view()

    # Assert
    assert duration == 142
