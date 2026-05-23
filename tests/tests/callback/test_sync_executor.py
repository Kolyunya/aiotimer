from asyncio import sleep
from unittest.mock import AsyncMock, Mock

from pytest import mark

from aiotimer.callback import Callback, SyncExecutor


@mark.asyncio
async def test_calls_a_sync_callback() -> None:
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
async def test_awaits_an_async_callback() -> None:
    # Arrange
    callback = AsyncMock()
    executor = SyncExecutor(
        error_handler=Mock(),
        error_factory=Mock(),
    )

    # Act
    await executor(Callback(callback), Mock())
    await sleep(0.1)

    # Assert
    callback.assert_awaited_once()
