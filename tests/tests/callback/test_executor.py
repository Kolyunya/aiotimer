from asyncio import sleep
from typing import Union
from unittest.mock import Mock

from pytest import mark

from aiotimer.callback import AsyncExecutor, Callback, SyncExecutor
from aiotimer.event import ErrorEvent
from tests.support import error_factory, watch_loop_errors

ExecutorType = Union[type[SyncExecutor], type[AsyncExecutor]]


@mark.asyncio
@mark.parametrize('executor_type', [SyncExecutor, AsyncExecutor])
async def test_error_is_forwarded_to_event_loop_when_no_error_handler_is_provided(
    executor_type: ExecutorType,
) -> None:
    # Arrange
    loop_errors = watch_loop_errors()
    callback_error = RuntimeError()

    error_handler = None

    def callback() -> None:
        raise callback_error

    executor = executor_type(Callback(error_handler), error_factory)

    # Act
    await executor.execute(Callback(callback), Mock())
    await sleep(0.1)

    # Assert
    assert len(loop_errors) == 1
    assert loop_errors[0]['exception'] is callback_error
    assert loop_errors[0]['message'] == 'No error handler is provided'


@mark.asyncio
@mark.parametrize('executor_type', [SyncExecutor, AsyncExecutor])
async def test_error_handler_is_invoked_when_provided(executor_type: ExecutorType) -> None:
    # Arrange
    loop_errors = watch_loop_errors()
    handled_errors: list[Exception] = []
    callback_error = RuntimeError()

    def error_handler(event: ErrorEvent) -> None:
        handled_errors.append(event.error)

    def callback() -> None:
        raise callback_error

    executor = executor_type(Callback(error_handler), error_factory)

    # Act
    await executor.execute(Callback(callback), Mock())
    await sleep(0.1)

    # Assert
    assert len(loop_errors) == 0
    assert len(handled_errors) == 1
    assert handled_errors[0] == callback_error


@mark.asyncio
@mark.parametrize('executor_type', [SyncExecutor, AsyncExecutor])
async def test_error_raised_by_error_handler_is_forwarded_to_event_loop(
    executor_type: ExecutorType,
) -> None:
    # Arrange
    loop_errors = watch_loop_errors()
    error_handler_error = RuntimeError()
    callback_error = RuntimeError()

    def error_handler(_event: ErrorEvent) -> None:
        raise error_handler_error

    def callback() -> None:
        raise callback_error

    executor = executor_type(Callback(error_handler), error_factory)

    # Act
    await executor.execute(Callback(callback), Mock())
    await sleep(0.1)

    # Assert
    assert len(loop_errors) == 1
    assert loop_errors[0]['exception'] is error_handler_error
    assert loop_errors[0]['message'] == 'Error handler is disabled'


@mark.asyncio
@mark.parametrize('executor_type', [SyncExecutor, AsyncExecutor])
async def test_error_handler_is_not_invoked_when_error_handling_is_disabled(
    executor_type: ExecutorType,
) -> None:
    # Arrange
    loop_errors = watch_loop_errors()
    handled_errors: list[Exception] = []
    callback_error = RuntimeError()

    def error_handler(event: ErrorEvent) -> None:
        handled_errors.append(event.error)

    def callback() -> None:
        raise callback_error

    executor = executor_type(Callback(error_handler), error_factory)

    # Act
    await executor.execute(Callback(callback), Mock(), handle_errors=False)
    await sleep(0.1)

    # Assert
    assert len(handled_errors) == 0
    assert len(loop_errors) == 1
    assert loop_errors[0]['exception'] is callback_error
    assert loop_errors[0]['message'] == 'Error handler is disabled'
