from asyncio import sleep
from unittest.mock import Mock

from pytest import mark, raises

from aiotimer import Timer
from aiotimer.duration import Durations
from aiotimer.duration.factory import never, once, sequentially
from aiotimer.error import (
    EmptyDurationIterableError,
    InvalidConfigurationError,
    NegativeDurationError,
)
from aiotimer.event import ErrorEvent


@mark.asyncio
@mark.parametrize('durations', [
    [],
    never(),
])
async def test_durations_must_not_be_empty(durations: Durations) -> None:
    with raises(EmptyDurationIterableError) as error:
        Timer(durations, Mock())

    assert str(error.value) == 'Duration iterable must not be empty'


@mark.asyncio
@mark.parametrize('durations', [
    [-1, 1],
    (-1, 1),
])
async def test_first_duration_must_be_positive_or_zero(durations: Durations) -> None:
    # Act
    with raises(NegativeDurationError) as error:
        Timer(durations, Mock())

    # Assert
    assert str(error.value) == 'Duration must be a positive number or zero'


@mark.asyncio
async def test_all_durations_must_be_positive_or_zero() -> None:
    # Arrange
    durations = lambda: [0.1, -0.1]
    on_error = Mock()

    timer = Timer(durations, Mock(), on_error=on_error)

    # Act
    await timer.start()
    await sleep(1)

    # Assert
    assert on_error.call_count == 1

    event = on_error.call_args_list[0].args[0]
    assert isinstance(event, ErrorEvent)
    assert isinstance(event.error, NegativeDurationError)
    assert str(event.error) == 'Duration must be a positive number or zero'


@mark.asyncio
@mark.parametrize('durations', [
    42,
    [42],
    (42,),
    once(42),
    sequentially(42),
])
async def test_can_pass_durations_in_different_forms(durations: Durations) -> None:
    # Arrange
    timer = Timer(durations, Mock())

    # Act
    remaining = timer.remaining

    # Assert
    assert remaining == 42


@mark.asyncio
async def test_at_least_one_callback_must_be_specified() -> None:
    with raises(InvalidConfigurationError) as error:
        Timer(once(42))

    assert str(error.value) == 'At least one of the `on_interval_complete` and `on_timer_complete` callbacks must be specified'


@mark.asyncio
@mark.parametrize('precision', [-1, 0])
async def test_precision_must_be_positive(precision: float) -> None:
    with raises(InvalidConfigurationError) as error:
        Timer(once(42), Mock(), precision=precision)

    assert str(error.value) == 'Precision must be a positive number'
