from asyncio import sleep
from unittest.mock import Mock

from pytest import mark, raises

from aiotimer import Timer
from aiotimer.duration.factory import once
from aiotimer.error import InvalidConfigurationError


@mark.asyncio
async def test_can_not_set_duration_to_negative_number() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    with raises(InvalidConfigurationError) as error:
        await timer.set(-1)

    # Assert
    assert str(error.value) == 'Duration must be a positive number or zero'


@mark.asyncio
async def test_can_set_duration_to_zero() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.set(0)

    duration = timer.remaining

    # Assert
    assert duration == 0


@mark.asyncio
async def test_can_set_duration_to_positive_number() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.set(142)

    duration = timer.remaining

    # Assert
    assert duration == 142


@mark.asyncio
async def test_can_change_duration_after_starting() -> None:
    # Arrange
    on_complete = Mock()
    timer = Timer(once(42), on_complete)

    # Act
    await timer.start()
    await timer.set(0.1)
    await sleep(1)

    # Assert
    on_complete.assert_called_once()
