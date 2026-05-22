from asyncio import run, sleep

from aiotimer import Timer
from aiotimer.event import TimerCompleteEvent


async def main() -> None:
    """
    Demonstrate an example of a one-off timer usage.
    """

    async def on_timer_complete(event: TimerCompleteEvent) -> None:
        print(f'Timer is complete in {event.elapsed:.3f} seconds.')

    timer = Timer(1.00, on_timer_complete)

    await timer.start()
    print('The timer is running.')

    # Wait for the timer to complete.
    await sleep(1 + 0.1)


if __name__ == '__main__':
    run(main())
