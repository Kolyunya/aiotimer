from asyncio import sleep
from collections.abc import Iterator
from unittest.mock import Mock

from pytest import mark

from aiotimer import Timer
from aiotimer.event import ErrorEvent
from aiotimer.state import FailedState
from tests.support import watch_bubbled_errors


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_error_is_handled_when_handler_is_provided(await_callbacks: bool) -> None:
    # Arrange
    bubbled_errors = watch_bubbled_errors()
    handled_errors: list[Exception] = []
    error = RuntimeError()

    def duration_factory() -> Iterator[float]:
        yield 0
        raise error

    def error_handler(event: ErrorEvent) -> None:
        handled_errors.append(event.error)

    timer = Timer(
        duration_factory,
        Mock(),
        on_error=error_handler,
        await_callbacks=await_callbacks,
    )

    # Act
    await timer.start()
    await sleep(0.1)

    # Assert
    assert len(bubbled_errors) == 0
    assert len(handled_errors) == 1
    assert handled_errors[0] is error
    assert await timer.state is FailedState


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_error_is_bubbled_when_handler_is_missing(await_callbacks: bool) -> None:
    # Arrange
    loop_errors = watch_bubbled_errors()
    error = RuntimeError('Bubbled error')

    def duration_factory() -> Iterator[float]:
        yield 0
        raise error

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
    assert loop_errors[0]['exception'] is error
    assert loop_errors[0]['message'] == 'Bubbled error'
    assert await timer.state is FailedState


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_failed_handler_bubbles_both_errors(
    await_callbacks: bool,
) -> None:
    # Arrange
    bubbled_errors = watch_bubbled_errors()
    initial_error = RuntimeError('Initial error')
    handler_error = RuntimeError('Handler error')

    def duration_factory() -> Iterator[float]:
        yield 0
        raise initial_error

    def error_handler() -> None:
        raise handler_error

    timer = Timer(
        duration_factory,
        Mock(),
        on_error=error_handler,
        await_callbacks=await_callbacks,
    )

    # Act
    await timer.start()
    await sleep(0.1)

    # Assert
    assert len(bubbled_errors) == 2
    assert len(bubbled_errors) == 2
    assert bubbled_errors[0]['exception'] is initial_error
    assert bubbled_errors[0]['message'] == 'Initial error'
    assert bubbled_errors[1]['exception'] is handler_error
    assert bubbled_errors[1]['message'] == 'Handler error'
    assert await timer.state is FailedState
