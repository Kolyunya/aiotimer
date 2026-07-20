from unittest.mock import AsyncMock, call

from pytest import mark

from aiotimer.utility.asyncio.error.handler import ErrorHandler
from tests.support import watch_bubbled_errors


@mark.asyncio
async def test_error_is_handled_when_handler_is_provided() -> None:
    # Arrange
    bubbled_errors = watch_bubbled_errors()
    error = RuntimeError('Handled error')

    handler = AsyncMock()
    error_handler = ErrorHandler(handler)

    # Act
    await error_handler.handle(error)

    # Assert
    assert handler.await_count == 1
    assert handler.await_args == call(error)
    assert len(bubbled_errors) == 0


@mark.asyncio
async def test_error_is_bubbled_when_handler_is_missing() -> None:
    # Arrange
    bubbled_errors = watch_bubbled_errors()
    error = RuntimeError('Bubbled error')

    handler = None
    error_handler = ErrorHandler(handler)

    # Act
    await error_handler.handle(error)

    # Assert
    assert len(bubbled_errors) == 1
    assert bubbled_errors[0]['exception'] is error
    assert bubbled_errors[0]['message'] == 'Bubbled error'


@mark.asyncio
async def test_failed_handler_bubbles_both_errors() -> None:
    # Arrange
    bubbled_errors = watch_bubbled_errors()
    initial_error = RuntimeError('Initial error')
    handler_error = RuntimeError('Handler error')

    handler = AsyncMock(side_effect=handler_error)
    error_handler = ErrorHandler(handler)

    # Act
    await error_handler.handle(initial_error)

    # Assert
    assert len(bubbled_errors) == 2
    assert bubbled_errors[0]['exception'] is initial_error
    assert bubbled_errors[0]['message'] == 'Initial error'
    assert bubbled_errors[1]['exception'] is handler_error
    assert bubbled_errors[1]['message'] == 'Handler error'
    assert handler.await_count == 1


@mark.asyncio
async def test_error_is_bubbled_when_bubbling_is_requested() -> None:
    # Arrange
    bubbled_errors = watch_bubbled_errors()
    error = RuntimeError('Bubbled error')

    handler = AsyncMock()
    error_handler = ErrorHandler(handler)

    # Act
    await error_handler.bubble(error)

    # Assert
    assert len(bubbled_errors) == 1
    assert bubbled_errors[0]['exception'] is error
    assert bubbled_errors[0]['message'] == 'Bubbled error'
    assert handler.await_count == 0
