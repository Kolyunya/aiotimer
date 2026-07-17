from asyncio import sleep
from unittest.mock import AsyncMock, Mock

from pytest import mark

from aiotimer import Timer
from aiotimer.duration import thrice


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_sync_callback_is_called_after_completion(await_callbacks: bool) -> None:
    # Arrange
    on_complete = Mock()
    timer = Timer(
        thrice(0.1),
        on_complete,
        await_callbacks=await_callbacks,
    )

    # Act
    await timer.start()
    await sleep(1)

    # Assert
    on_complete.assert_called_once()


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_async_callback_is_awaited_after_completion(await_callbacks: bool) -> None:
    # Arrange
    on_complete = AsyncMock()
    timer = Timer(
        thrice(0.1),
        on_complete,
        await_callbacks=await_callbacks,
    )

    # Act
    await timer.start()
    await sleep(1)

    # Assert
    on_complete.assert_awaited_once()
