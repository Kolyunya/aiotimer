from asyncio import sleep
from unittest.mock import AsyncMock, Mock

from pytest import mark, raises

from aiotimer import Timer
from aiotimer.error import InvalidConfigurationError, InvalidDurationError
from aiotimer.event import ErrorEvent
from aiotimer.interval import once
from aiotimer.interval.never import never


@mark.asyncio
async def test_at_least_one_callback_must_be_specified() -> None:
    with raises(InvalidConfigurationError) as error:
        Timer(once(42))

    assert str(error.value) == 'At least one of the `on_interval_complete` and `on_timer_complete` event handlers must be specified'


@mark.asyncio
@mark.parametrize('precision', [-1, 0])
async def test_precision_must_be_positive(precision: float) -> None:
    with raises(InvalidConfigurationError) as error:
        Timer(once(42), Mock(), precision=precision)

    assert str(error.value) == 'The precision must be a positive number'


@mark.asyncio
async def test_interval_generator_must_not_be_empty() -> None:
    with raises(InvalidConfigurationError) as error:
        Timer(never(), Mock())

    assert str(error.value) == 'The interval generator must yield at least one value'


@mark.asyncio
@mark.parametrize('first_duration', [-1.0, -0.1])
async def test_first_duration_must_be_non_negative(first_duration: float) -> None:
    # Arrange
    intervals = lambda: (duration for duration in [first_duration])

    # Act
    with raises(InvalidConfigurationError) as error:
        Timer(intervals, Mock())

    # Assert
    assert str(error.value) == 'The duration must be a positive number or zero'


@mark.asyncio
@mark.parametrize('durations', [
    (0.1, -1.0),
    (0.1, -0.1),
])
async def test_all_durations_must_be_non_negative(durations: tuple[float]) -> None:
    # Arrange
    intervals = lambda: (duration for duration in durations)
    on_complete = Mock()
    on_error = Mock()

    timer = Timer(
        intervals,
        on_timer_complete=on_complete,
        on_error=on_error,
    )

    # Act
    await timer.run()
    await sleep(1)

    # Assert
    assert on_error.call_count == 1

    event = on_error.call_args_list[0].args[0]
    assert isinstance(event, ErrorEvent)
    assert isinstance(event.error, InvalidDurationError)
    assert str(event.error) == 'The duration must be a positive number or zero'


@mark.asyncio
async def test_on_complete_could_be_sync() -> None:
    Timer(once(42), Mock())


@mark.asyncio
async def test_on_complete_could_be_async() -> None:
    Timer(once(42), AsyncMock())
