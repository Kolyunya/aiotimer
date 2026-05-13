from asyncio import sleep
from unittest.mock import AsyncMock, Mock

from pytest import mark

from aiotimer import Timer
from aiotimer.interval import once


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_sync_on_error_is_called(await_callbacks: bool) -> None:
    # Arrange
    def on_complete() -> None:
        raise RuntimeError

    on_error = Mock()

    timer = Timer(
        once(0.1),
        on_timer_complete=on_complete,
        on_error=on_error,
        await_callbacks=await_callbacks,
    )

    # Act
    await timer.run()
    await sleep(1)

    # Assert
    on_error.assert_called()


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_async_on_error_is_called(await_callbacks: bool) -> None:
    # Arrange
    async def on_complete() -> None:
        raise RuntimeError

    on_error = AsyncMock()

    timer = Timer(
        once(0.1),
        on_timer_complete=on_complete,
        on_error=on_error,
        await_callbacks=await_callbacks,
    )

    # Act
    await timer.run()
    await sleep(1)

    # Assert
    on_error.assert_awaited_once()


@mark.asyncio
@mark.parametrize('await_callbacks', [True, False])
async def test_no_infinite_loop_after_error_inside_error_handler(await_callbacks: bool) -> None:
    # Arrange
    def on_complete() -> None:
        raise RuntimeError

    def on_error() -> None:
        raise RuntimeError

    # Act
    timer = Timer(
        once(0.1),
        on_timer_complete=on_complete,
        on_error=on_error,
        await_callbacks=await_callbacks,
    )

    # Assert
    await timer.run()
    await sleep(1)
