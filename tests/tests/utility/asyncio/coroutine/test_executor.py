from asyncio import sleep
from typing import Union
from unittest.mock import AsyncMock, call

from pytest import mark

from aiotimer.utility.asyncio.coroutine.executor import AsyncExecutor, SyncExecutor
from aiotimer.utility.asyncio.error.handler import ErrorHandler
from tests.support import watch_bubbled_errors

ExecutorType = Union[type[SyncExecutor], type[AsyncExecutor]]


@mark.asyncio
@mark.parametrize('executor_type', [AsyncExecutor, SyncExecutor])
async def test_coroutine_is_awaited(executor_type: ExecutorType) -> None:
    # Arrange
    handler = AsyncMock()
    error_handler = ErrorHandler(handler)
    executor = executor_type(error_handler)

    coroutine = AsyncMock()

    # Act
    await executor.execute(coroutine())
    await sleep(0.1)

    # Assert
    assert coroutine.await_count == 1


@mark.asyncio
@mark.parametrize('executor_type', [AsyncExecutor, SyncExecutor])
async def test_error_is_handled_when_handler_is_provided(executor_type: ExecutorType) -> None:
    # Arrange
    bubbled_errors = watch_bubbled_errors()
    error = RuntimeError('Handled error')

    handler = AsyncMock()
    error_handler = ErrorHandler(handler)
    executor = executor_type(error_handler)

    coroutine = AsyncMock(side_effect=error)

    # Act
    await executor.execute(coroutine())
    await sleep(0.1)

    # Assert
    assert handler.await_count == 1
    assert handler.await_args == call(error)
    assert len(bubbled_errors) == 0


@mark.asyncio
@mark.parametrize('executor_type', [AsyncExecutor, SyncExecutor])
async def test_error_is_bubbled_when_handler_is_missing(executor_type: ExecutorType) -> None:
    # Arrange
    bubbled_errors = watch_bubbled_errors()
    error = RuntimeError('Bubbled error')

    handler = None
    error_handler = ErrorHandler(handler)
    executor = executor_type(error_handler)

    coroutine = AsyncMock(side_effect=error)

    # Act
    await executor.execute(coroutine())
    await sleep(0.1)

    # Assert
    assert len(bubbled_errors) == 1
    assert bubbled_errors[0]['exception'] is error
    assert bubbled_errors[0]['message'] == 'Bubbled error'


@mark.asyncio
@mark.parametrize('executor_type', [AsyncExecutor, SyncExecutor])
async def test_failed_handler_bubbles_both_errors(executor_type: ExecutorType) -> None:
    # Arrange
    bubbled_errors = watch_bubbled_errors()
    initial_error = RuntimeError('Initial error')
    handler_error = RuntimeError('Handler error')

    handler = AsyncMock(side_effect=handler_error)
    error_handler = ErrorHandler(handler)
    executor = executor_type(error_handler)

    coroutine = AsyncMock(side_effect=initial_error)

    # Act
    await executor.execute(coroutine())
    await sleep(0.1)

    # Assert
    assert len(bubbled_errors) == 2
    assert bubbled_errors[0]['exception'] is initial_error
    assert bubbled_errors[0]['message'] == 'Initial error'
    assert bubbled_errors[1]['exception'] is handler_error
    assert bubbled_errors[1]['message'] == 'Handler error'
    assert handler.await_count == 1


@mark.asyncio
@mark.parametrize('executor_type', [AsyncExecutor, SyncExecutor])
async def test_error_is_bubbled_when_bubbling_is_requested(executor_type: ExecutorType) -> None:
    # Arrange
    bubbled_errors = watch_bubbled_errors()
    error = RuntimeError('Bubbled error')

    handler = AsyncMock()
    error_handler = ErrorHandler(handler)
    executor = executor_type(error_handler)

    coroutine = AsyncMock(side_effect=error)

    # Act
    await executor.execute(coroutine(), bubble_errors=True)
    await sleep(0.1)

    # Assert
    assert len(bubbled_errors) == 1
    assert bubbled_errors[0]['exception'] is error
    assert bubbled_errors[0]['message'] == 'Bubbled error'
    assert handler.await_count == 0
