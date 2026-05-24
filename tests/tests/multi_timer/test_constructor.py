from asyncio import sleep
from unittest.mock import Mock

from pytest import mark, raises

from aiotimer import MultiTimer
from aiotimer.duration import never, once
from aiotimer.error import (
    EmptyDurationIterableError,
    InvalidConfigurationError,
    InvalidDurationError,
)
from aiotimer.event import ErrorEvent


@mark.asyncio
async def test_intervals_must_not_be_empty() -> None:
    with raises(EmptyDurationIterableError) as error:
        MultiTimer(never(), Mock())

    assert str(error.value) == 'Duration iterable must have at least one value'


@mark.asyncio
async def test_at_least_one_callback_must_be_specified() -> None:
    with raises(InvalidConfigurationError) as error:
        MultiTimer(once(42))

    assert str(error.value) == 'At least one of the `on_interval_complete` and `on_timer_complete` callbacks must be specified'


@mark.asyncio
@mark.parametrize('precision', [-1, 0])
async def test_precision_must_be_positive(precision: float) -> None:
    with raises(InvalidConfigurationError) as error:
        MultiTimer(once(42), Mock(), precision=precision)

    assert str(error.value) == 'The precision must be a positive number'


@mark.asyncio
async def test_first_duration_must_be_non_negative() -> None:
    # Arrange
    intervals = lambda: (_ for _ in [-0.1])

    # Act
    with raises(InvalidConfigurationError) as error:
        MultiTimer(intervals, Mock())

    # Assert
    assert str(error.value) == 'The duration must be a positive number or zero'


@mark.asyncio
async def test_all_durations_must_be_non_negative() -> None:
    # Arrange
    intervals = lambda: (_ for _ in [0.1, -0.1])
    on_error = Mock()

    timer = MultiTimer(
        intervals,
        on_timer_complete=Mock(),
        on_error=on_error,
    )

    # Act
    await timer.start()
    await sleep(1)

    # Assert
    assert on_error.call_count == 1

    event = on_error.call_args_list[0].args[0]
    assert isinstance(event, ErrorEvent)
    assert isinstance(event.error, InvalidDurationError)
    assert str(event.error) == 'The duration must be a positive number or zero'
