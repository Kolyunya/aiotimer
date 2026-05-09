from asyncio import run, sleep

from aiotimer import Timer
from aiotimer.interval import once, repeatedly


async def main() -> None:
    """
    Demonstrate an example of a multi-interval timer usage.
    """

    timer = Timer(
        repeatedly(once(1), 3),
        on_timer_complete=lambda: print('The timer has ran for a total of 3 seconds.'),
        on_interval_complete=lambda: print('The timer has ran for another second.'),
    )
    await timer.run()
    print('The timer is running.')

    # Add a sleep margin of one second to avoid any race conditions.
    await sleep(3 + 1)


if __name__ == '__main__':
    run(main())
