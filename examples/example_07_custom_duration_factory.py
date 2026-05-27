from asyncio import run, sleep

from aiotimer import Timer
from aiotimer.event import IntervalCompleteEvent, TimerCompleteEvent


async def main() -> None:
    """
    Demonstrate an example of a custom duration factory.
    """

    duration_factory = lambda: [1, 2, 3]

    async def on_timer_complete(event: TimerCompleteEvent) -> None:
        print(f'Timer complete after {event.interval_count} intervals')

    async def on_interval_complete(event: IntervalCompleteEvent) -> None:
        print(f'Interval complete after {event.interval_duration} seconds')

    timer = Timer(
        duration_factory,
        on_timer_complete,
        on_interval_complete,
    )
    await timer.start()

    # Wait for the timer to complete.
    await sleep(6 + 0.1)


if __name__ == '__main__':
    run(main())
