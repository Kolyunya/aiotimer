from asyncio import Event, run, sleep

from tests.support import stopwatch

from aiotimer import Timer
from aiotimer.duration import thrice


async def main() -> None:
    """
    Demonstrate an example of a timer that does await callbacks.

    Note that the timer does not keep running, while the `on_interval_complete`
    callback is sleeping. The timer is waiting for it to complete.
    """

    async def on_timer_complete() -> None:
        timer_complete.set()

    async def on_interval_complete() -> None:
        await sleep(1)

    timer = Timer(
        thrice(1),
        on_timer_complete,
        on_interval_complete,
        await_callbacks=True,
    )

    timer_complete = Event()

    async with stopwatch() as time:
        print('The timer is running.')
        await timer.start()
        await timer_complete.wait()

    print(f'The timer is complete in {time.elapsed:.3f} seconds.')


if __name__ == '__main__':
    run(main())
