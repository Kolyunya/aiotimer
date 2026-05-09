from asyncio import sleep
from unittest.mock import AsyncMock, Mock

from pytest import mark

from aiotimer import Timer
from aiotimer.interval import thrice


@mark.asyncio
async def test_sync_callback_is_called_after_completion() -> None:
    # Arrange
    on_complete = Mock()
    timer = Timer(thrice(0.1), on_complete)

    # Act
    await timer.run()
    await sleep(1)

    # Assert
    on_complete.assert_called_once()


@mark.asyncio
async def test_async_callback_is_awaited_after_completion() -> None:
    # Arrange
    on_complete = AsyncMock()
    timer = Timer(thrice(0.1), on_complete)

    # Act
    await timer.run()
    await sleep(1)

    # Assert
    on_complete.assert_awaited_once()
