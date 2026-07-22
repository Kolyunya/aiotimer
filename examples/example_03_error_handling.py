from asyncio import run, sleep

from aiotimer import Timer
from aiotimer.duration.factory import thrice
from aiotimer.event import ErrorEvent


async def main() -> None:
    """
    Demonstrate an example of error handling.
    """

    async def on_timer_complete() -> None:
        raise RuntimeError('Error while executing `on_timer_complete`')

    async def on_interval_complete() -> None:
        raise RuntimeError('Error while executing `on_interval_complete`')

    async def on_error(event: ErrorEvent) -> None:
        print(f'An exception was handled: {event.error!r}.')

    timer = Timer(
        thrice(1),
        on_timer_complete,
        on_interval_complete,
        on_error,
    )
    await timer.start()
    print('The timer is running.')

    # Wait for the timer to complete.
    await sleep(3 + 0.1)


if __name__ == '__main__':
    run(main())
