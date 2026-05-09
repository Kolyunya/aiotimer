from asyncio import run, sleep

from aiotimer import Timer
from aiotimer.event import ErrorEvent
from aiotimer.interval import thrice


async def main() -> None:
    """
    Demonstrate an example of error handling.
    """

    async def on_complete() -> None:
        raise RuntimeError('Error while executing `on_complete`')

    async def on_interval() -> None:
        raise RuntimeError('Error while executing `on_interval`')

    async def on_error(event: ErrorEvent) -> None:
        print(f'An exception was handled: {event.error!r}.')

    timer = Timer(
        thrice(1),
        on_timer_complete=on_complete,
        on_interval_complete=on_interval,
        on_error=on_error,
    )
    await timer.run()
    print('The timer is running.')

    # Add a sleep margin of one second to avoid any race conditions.
    await sleep(3 + 1)


if __name__ == '__main__':
    run(main())
