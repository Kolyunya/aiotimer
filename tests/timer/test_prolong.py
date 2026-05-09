from unittest.mock import Mock

from pytest import mark, raises

from aiotimer import Timer
from aiotimer.error import InvalidConfigurationError
from aiotimer.interval import once


@mark.asyncio
async def test_can_prolong_duration() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.prolong(10)
    duration = await timer.view()

    # Assert
    assert duration == 52


@mark.asyncio
async def test_can_prolong_duration_to_zero() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.prolong(-42)
    duration = await timer.view()

    # Assert
    assert duration == 0


@mark.asyncio
async def test_can_not_prolong_duration_to_negative_number() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    with raises(InvalidConfigurationError) as error:
        await timer.prolong(-142)

    # Assert
    assert str(error.value) == 'The duration must be a positive number or zero'
