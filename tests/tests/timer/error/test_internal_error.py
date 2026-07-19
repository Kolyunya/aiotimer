from asyncio import sleep
from collections.abc import Iterator
from unittest.mock import Mock

from pytest import mark

from aiotimer import Timer
from aiotimer.event import ErrorEvent
from aiotimer.state import FailedState
from tests.support import watch_loop_errors


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_error_is_forwarded_to_event_loop_when_no_error_handler_is_provided(
    await_callbacks: bool,
) -> None:
    # Arrange
    loop_errors = watch_loop_errors()
    internal_error = RuntimeError()

    def duration_factory() -> Iterator[float]:
        yield 0
        raise internal_error

    timer = Timer(
        duration_factory,
        Mock(),
        await_callbacks=await_callbacks,
    )

    # Act
    await timer.start()
    await sleep(0.1)

    # Assert
    assert len(loop_errors) == 1
    assert loop_errors[0]['exception'] is internal_error
    assert loop_errors[0]['message'] == 'No error handler is provided'
    assert await timer.state is FailedState


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_error_handler_is_invoked_when_provided(await_callbacks: bool) -> None:
    # Arrange
    loop_errors = watch_loop_errors()
    handled_errors: list[Exception] = []
    internal_error = RuntimeError()

    def duration_factory() -> Iterator[float]:
        yield 0
        raise internal_error

    def on_error(event: ErrorEvent) -> None:
        handled_errors.append(event.error)

    timer = Timer(
        duration_factory,
        Mock(),
        on_error=on_error,
        await_callbacks=await_callbacks,
    )

    # Act
    await timer.start()
    await sleep(0.1)

    # Assert
    assert len(loop_errors) == 0
    assert len(handled_errors) == 1
    assert handled_errors[0] is internal_error
    assert await timer.state is FailedState


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_error_raised_by_error_handler_is_forwarded_to_event_loop(
    await_callbacks: bool,
) -> None:
    # Arrange
    loop_errors = watch_loop_errors()
    error_handler_error = RuntimeError()

    def duration_factory() -> Iterator[float]:
        yield 0
        raise RuntimeError

    def on_error() -> None:
        raise error_handler_error

    timer = Timer(
        duration_factory,
        Mock(),
        on_error=on_error,
        await_callbacks=await_callbacks,
    )

    # Act
    await timer.start()
    await sleep(0.1)

    # Assert
    assert len(loop_errors) == 1
    assert loop_errors[0]['exception'] is error_handler_error
    assert loop_errors[0]['message'] == 'Error handler is disabled'
    assert await timer.state is FailedState
