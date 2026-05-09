from asyncio import sleep
from unittest.mock import Mock

from pytest import mark

from aiotimer.utility.callback import Executor


@mark.asyncio
async def test_executor_executes_a_callback() -> None:
    # Arrange
    callback = Mock()
    executor = Executor(Mock(), Mock())

    # Act
    await executor(callback, Mock())
    await sleep(1)

    # Assert
    callback.assert_called_once()
