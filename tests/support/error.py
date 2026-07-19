from asyncio import AbstractEventLoop, get_running_loop
from typing import Any
from unittest.mock import Mock

from aiotimer import TimerInterface
from aiotimer.event import ErrorEvent


async def error_factory(error: Exception) -> ErrorEvent:
    event = ErrorEvent(
        timer=Mock(spec=TimerInterface),
        error=error,
    )

    return event


def watch_loop_errors() -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []

    def exception_handler(_loop: AbstractEventLoop, context: dict[str, Any]) -> None:
        errors.append(context)

    loop = get_running_loop()
    loop.set_exception_handler(exception_handler)

    return errors
