from asyncio import run, sleep
from time import perf_counter


async def main(seconds: int) -> None:
    """
    Demonstrate that `asyncio.sleep` drifts significantly.

    Naive implementations may use `asyncio.sleep` under the hood of the timer.
    But such implementations would lack precision and would drift when timer
    has many small intervals.
    """

    print('Running the timer...')
    print(f'Desired duration: {seconds:.3f} seconds.')

    time_start = perf_counter()

    for _ in range(seconds):
        await sleep(1)

    time_end = perf_counter()
    time_elapsed = time_end - time_start

    print(f'Actual duration: {time_elapsed:.3f} seconds.\n')


if __name__ == '__main__':
    durations = [
        10,
        60 * 1,
        60 * 3,
        60 * 5,
    ]

    for duration in durations:
        run(main(duration))
