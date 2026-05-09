# Asyncio Timer

An asynchronous timer with a human-friendly API and rich functionality.

* State management with `start()`, `stop()`, `pause()`, and `reset()` methods.
* On-the-fly adjustment of the duration with `set()`, `prolong()`, and `shorten()` methods.
* Multi-interval configuration when the timer runs multiple times with a predefined pattern of durations.
* Looping capabilities for continuously running timers.
* Rich callback system enabling hooking into the timer lifecycle events.
* Concurrency-safe architecture designed to prevent race conditions and deadlocks.
* Support for a wide range of Python versions from `3.9` onward.
* Zero third-party dependencies.

## Table of contents
* [Basic usage](#basic-usage)
  * [One-off timer](#one-off-timer)
  * [Multi-interval timer](#multi-interval-timer)
  * [Other usage examples](#other-usage-examples)
* [Built-in intervals](#built-in-interval-generators)
* [Event system](#event-system)
  * [Interval complete event](#interval-complete-event)
  * [Timer complete event](#timer-complete-event)
  * [Error event](#error-event)
* [Advanced usage](#advanced-usage)
  * [Configuring precision](#configuring-precision)
  * [Custom intervals](#custom-intervals)
* [Contributing](#contributing)

## Basic usage

### One-off timer
```python
from asyncio import run, sleep

from aiotimer import Timer
from aiotimer.interval import once


async def main() -> None:
    """
    Will run the timer for 3 seconds.
    Then will print a message.
    """

    timer = Timer(once(3), lambda: print('3 seconds passed'))
    await timer.run()

    # Wait for the timer to complete.
    await sleep(3 + 1)

if __name__ == '__main__':
    run(main())
```

### Multi-interval timer

```python
from asyncio import run, sleep

from aiotimer import Timer
from aiotimer.interval import thrice


async def main() -> None:
    """
    Will run the timer three times for 1 second each.
    And will print intermediate messages every second.
    Then will print the final message after a total of 3 seconds.
    """

    timer = Timer(
        thrice(1),
        on_timer_complete=lambda: print('3 seconds passed'),
        on_interval_complete=lambda: print('1 more second passed'),
    )
    await timer.run()

    # Wait for the timer to complete.
    await sleep(3 + 1)

if __name__ == '__main__':
    run(main())
```

### Other usage examples
More usage examples are available [here](examples).


## Built-in interval generators
There are many built-in [interval generators](sources/aiotimer/interval) that should cover the majority of common use cases.

```python
from aiotimer import Timer
from aiotimer.interval import *

Timer(once(5), lambda: print('Ran once for 5 seconds'))

Timer(twice(5), lambda: print('Ran twice for 5 seconds each'))

Timer(thrice(5), lambda: print('Ran thrice for 5 seconds each'))

# Repeatedly accepts any other interval and repeats it.
Timer(repeatedly(once(5), 10), lambda: print('Ran 10 times for 5 seconds each'))

Timer(repeatedly(randomly(3, 5), 10), lambda: print('Ran 10 times between 3 and 5 seconds each'))

Timer(sequentially(1, 2, 3), lambda: print('Ran for 1, 2, and 3 seconds'))

Timer(exponentially(1, 5), lambda: print('Ran for 1, 2, 4, 8, and 16 seconds'))

# Any interval construct could be combined with `immediately_then()`.
Timer(immediately_then(once(5)), lambda: print('Fired immediately and after 5 seconds'))

# Jitter may be specified relative to the duration.
Timer(jittery(thrice(5), relative=0.1), lambda: print('Ran thrice for 5±0.5 seconds'))

# Jitter may be specified as an absolute value.
Timer(jittery(thrice(5), absolute=0.5), lambda: print('Ran thrice for 5±0.5 seconds'))

# `on_timer_complete` will never be fired, use `on_interval_complete` instead.
Timer(forever(once(5)), on_interval_complete=lambda: print('5 more seconds passed'))
```

> If you believe some type of interval generator is missing, feel free to create an issue or a pull request.

## Event system
All event handlers **must** comply with the following API contract. Non-compliant event handlers result in undefined behavior.
* Event handler **may** be either:
  * Synchronous callable.
  * Asynchronous callable.
* Event handler **must** have either:
    * Zero parameters.
    * Exactly one positional parameter accepting the corresponding event object type.
* Event handler **should not** return any values because they will be ignored and discarded by the timer.
* An event handler's signature **must not** be modified at runtime after registration with the timer object.

> Any public method of a timer object may be safely called from any event handler. The internal timer architecture prevents any race conditions and deadlocks from occurring. 

### Interval complete event
This event is fired each time any interval of a timer is complete. An `on_interval_complete` handler **_may_** optionally accept an [`IntervalCompleteEvent`](sources/aiotimer/event/interval_complete_event.py) object.

### Timer complete event
This event is fired each time the last interval of a timer is complete. An `on_timer_complete` handler **_may_** optionally accept a [`TimerCompleteEvent`](sources/aiotimer/event/timer_complete_event.py) object.

### Error event
This event is fired each time any exception is propagated from any of the event handlers described above. Additionally, it is fired when an exception occurs inside a system coroutine of a timer. An `on_error` handler **_may_** optionally accept an [`ErrorEvent`](sources/aiotimer/event/error_event.py) object.

## Advanced usage

### Configuring precision
The timer class has a configurable `precision: float` parameter. It represents the amount of seconds a timer would idle between its system ticks.

For adequate accuracy, it is recommended to have the precision value configured significantly (at least several times) smaller than the shortest interval the timer would have.

At the same time, having the precision configured to an extremely low value (e.g. `0.001`) may yield a high CPU load.

### Custom intervals
The first argument to the timer constructor is an [`Interval Generator Factory`](sources/aiotimer/interval/type/interval_generator.py). In other words, it is a callable that returns a generator that yields interval durations.

> This design decision is required to support multiple functionalities.
>
> A regular list of interval durations could not be used because this would not allow having an infinite number of intervals.
>
> A regular generator object could not be used because it could not be reset to its initial state, which is required to support the `timer.reset()` functionality.

```python
from asyncio import run, sleep

from aiotimer import Timer


async def main() -> None:
    # The simplest form of the Interval Generator Factory.
    intervals = lambda: (duration for duration in [1, 2, 3])

    timer = Timer(intervals, lambda: print('6 seconds passed'))
    await timer.run()

    # Add an extra second of sleep to avoid a race condition.
    await sleep(6 + 1)

if __name__ == '__main__':
    run(main())
```

## Contributing

### Configuring the development environment
```bash
# Create and activate a virtual environment.
python -m venv .
source bin/activate

# Install the library and its dependencies.
pip install --upgrade pip
pip install --editable ".[development]"

# Run the test suite.
BEARTYPE=Yes python -m test --skip-slow=No
```

Additionally, a convenient `Test` run configuration is provided for `PyCharm` users.
