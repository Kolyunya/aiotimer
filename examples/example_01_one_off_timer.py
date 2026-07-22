from asyncio import run, sleep

from aiotimer import Timer
from aiotimer.duration.factory import once


async def main() -> None:
    """
    Demonstrate an example of a one-off timer usage.
    """

    async def on_complete() -> None:
        print('The timer is complete.')

    timer = Timer(once(1.00), on_complete)

    await timer.start()
    print('The timer is running.')

    # Wait for the timer to complete.
    await sleep(1 + 0.1)


if __name__ == '__main__':
    run(main())
