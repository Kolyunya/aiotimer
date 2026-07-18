from asyncio import run, sleep

from aiotimer import Timer
from aiotimer.duration import once, repeatedly


async def main() -> None:
    """
    Demonstrate an example of a multi-interval timer usage.
    """

    timer = Timer(
        repeatedly(once(1), 3),
        lambda: print('The timer has ran for a total of 3 seconds.'),
        lambda: print('The timer has ran for another second.'),
    )
    await timer.start()
    print('The timer is running.')

    # Wait for the timer to complete.
    await sleep(3 + 0.1)


if __name__ == '__main__':
    run(main())
