from asyncio import run, sleep

from aiotimer import Timer
from aiotimer.interval import once


async def main() -> None:
    """
    Demonstrate an example of a one-off timer usage.
    """

    timer = Timer(
        once(3),
        on_timer_complete=lambda: print('The timer has ran for 3 seconds.'),
    )
    await timer.run()
    print('The timer is running.')

    # Add a sleep margin of one second to avoid any race conditions.
    await sleep(3 + 1)


if __name__ == '__main__':
    run(main())
