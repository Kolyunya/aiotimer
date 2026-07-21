from asyncio import sleep
from unittest.mock import Mock

from pytest import mark, raises

from aiotimer import Timer
from aiotimer.duration import once
from aiotimer.error import InvalidConfigurationError


@mark.asyncio
async def test_can_not_shorten_duration_to_negative_number() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    with raises(InvalidConfigurationError) as error:
        await timer.shorten(142)

    # Assert
    assert str(error.value) == 'Duration must be a positive number or zero'


@mark.asyncio
async def test_can_shorten_duration_to_positive_number() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.shorten(10)

    duration = timer.remaining

    # Assert
    assert duration == 32


@mark.asyncio
async def test_can_shorten_duration_to_zero() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.shorten(42)

    duration = timer.remaining

    # Assert
    assert duration == 0


@mark.asyncio
@mark.parametrize(('duration', 'delta', 'wait'), [
    (100.0, 99.0, 1.0),
    (100.0, 99.9, 0.1),
    (100.0, 100.0, 0.0),
])
async def test_completes_earlier_after_shortening(duration: float, delta: float, wait: float) -> None:
    # Arrange
    on_complete = Mock()
    timer = Timer(once(duration), on_complete)

    # Act
    await timer.start()
    await timer.shorten(delta)
    await sleep(wait + 0.1)

    # Assert
    on_complete.assert_called_once()
