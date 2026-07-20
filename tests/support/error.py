from asyncio import AbstractEventLoop, get_running_loop
from typing import Any


def watch_bubbled_errors() -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []

    def exception_handler(_loop: AbstractEventLoop, context: dict[str, Any]) -> None:
        errors.append(context)

    loop = get_running_loop()
    loop.set_exception_handler(exception_handler)

    return errors
