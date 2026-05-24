from unittest.mock import Mock

from pytest import mark, raises

from aiotimer import MultiTimer
from aiotimer.duration import once
from aiotimer.error import InvalidDurationError


@mark.asyncio
async def test_can_not_prolong_duration_to_negative_number() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    with raises(InvalidDurationError) as error:
        await timer.prolong(-142)

    # Assert
    assert str(error.value) == 'The duration must be a positive number or zero'


@mark.asyncio
async def test_can_prolong_duration_to_positive_number() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    await timer.prolong(10)
    duration = await timer.remaining

    # Assert
    assert duration == 52


@mark.asyncio
async def test_can_prolong_duration_to_zero() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    await timer.prolong(-42)
    duration = await timer.remaining

    # Assert
    assert duration == 0
