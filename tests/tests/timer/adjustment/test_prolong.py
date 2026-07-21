from unittest.mock import Mock

from pytest import mark, raises

from aiotimer import Timer
from aiotimer.duration import once
from aiotimer.error import NegativeDurationError


@mark.asyncio
async def test_can_not_prolong_duration_to_negative_number() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    with raises(NegativeDurationError) as error:
        await timer.prolong(-142)

    # Assert
    assert str(error.value) == 'Duration must be a positive number or zero'


@mark.asyncio
async def test_can_prolong_duration_to_positive_number() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.prolong(10)

    duration = timer.remaining

    # Assert
    assert duration == 52


@mark.asyncio
async def test_can_prolong_duration_to_zero() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.prolong(-42)

    duration = timer.remaining

    # Assert
    assert duration == 0
