from asyncio import sleep
from unittest.mock import AsyncMock, Mock

from pytest import mark

from aiotimer.callback import AsyncExecutor, Callback, SyncExecutor


@mark.asyncio
async def test_sync_executor_executes_a_callback() -> None:
    # Arrange
    callback = Mock()
    executor = SyncExecutor(
        error_handler=Mock(),
        error_factory=Mock(),
    )

    # Act
    await executor(Callback(callback), Mock())
    await sleep(0.1)

    # Assert
    callback.assert_called_once()


@mark.asyncio
async def test_async_executor_executes_a_callback() -> None:
    # Arrange
    callback = AsyncMock()
    executor = AsyncExecutor(
        error_handler=Mock(),
        error_factory=Mock(),
    )

    # Act
    await executor(Callback(callback), Mock())
    await sleep(0.1)

    # Assert
    callback.assert_awaited_once()
