from asyncio import run, sleep

from aiotimer import Timer
from aiotimer.event import IntervalCompleteEvent, TimerCompleteEvent
from aiotimer.interval import thrice


async def main() -> None:
    """
    Demonstrate an example of a timer that does await callbacks.

    Note that the timer does not keep running, while the `on_interval_complete`
    callback is sleeping. The timer is waiting for it to complete.
    """

    async def on_interval_complete(event: IntervalCompleteEvent) -> None:
        print(f'Interval is complete in {event.elapsed:.2f} seconds.')
        await sleep(1)

    async def on_timer_complete(event: TimerCompleteEvent) -> None:
        print(f'Timer is complete in {event.elapsed:.2f} seconds.')

    timer = Timer(
        thrice(1),
        on_interval_complete=on_interval_complete,
        on_timer_complete=on_timer_complete,
        await_callbacks=True,
        precision=0.001,
    )

    await timer.run()
    print('The timer is running.')

    # Wait for the timer to complete.
    await sleep(6 + 0.1)


if __name__ == '__main__':
    run(main())
