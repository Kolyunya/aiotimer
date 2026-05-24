from asyncio import run, sleep

from aiotimer import MultiTimer
from aiotimer.duration import thrice
from aiotimer.event import IntervalCompleteEvent, TimerCompleteEvent


async def main() -> None:
    """
    Demonstrate an example of a timer that does not await callbacks.

    Note that the timer keeps running, while the `on_interval_complete`
    callback is sleeping. The timer is not waiting for it to complete.
    """

    async def on_interval_complete(event: IntervalCompleteEvent) -> None:
        print(f'Interval is complete in {event.elapsed:.3f} seconds.')
        await sleep(1)

    async def on_timer_complete(event: TimerCompleteEvent) -> None:
        print(f'Timer is complete in {event.elapsed:.3f} seconds.')

    timer = MultiTimer(
        thrice(1),
        on_interval_complete=on_interval_complete,
        on_timer_complete=on_timer_complete,
        await_callbacks=False,
    )

    await timer.start()
    print('The timer is running.')

    # Wait for the timer to complete.
    await sleep(3 + 0.1)


if __name__ == '__main__':
    run(main())
