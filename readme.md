# Asyncio Timer

An asynchronous timer with a human-friendly API and rich functionality.

* State management with `start()`, `stop()`, and `reset()` methods.
* On-the-fly adjustment of the duration with `set()`, `prolong()`, and `shorten()` methods.
* Introspection with `elapsed`, `remaining`, and `state` properties.
* Multi-interval configuration when a timer runs multiple times with a predefined schedule pattern.
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
* [States and transitions](#states-and-transitions)
* [Interval Generator Factories](#interval-generator-factories)
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

  timer = Timer(3, lambda: print('3 seconds passed'))
  await timer.start()

  # Wait for the timer to complete.
  await sleep(3 + 1)


if __name__ == '__main__':
  run(main())
```

### Multi-interval timer

```python
from asyncio import run, sleep

from aiotimer import MultiTimer
from aiotimer.interval import thrice


async def main() -> None:
  """
  Will run the timer three times for 1 second each.
  And will print intermediate messages every second.
  Then will print the final message after a total of 3 seconds.
  """

  timer = MultiTimer(
    thrice(1),
    on_timer_complete=lambda: print('3 seconds passed'),
    on_interval_complete=lambda: print('1 more second passed'),
  )
  await timer.start()

  # Wait for the timer to complete.
  await sleep(3 + 1)


if __name__ == '__main__':
  run(main())
```

### Other usage examples
More usage examples are available [here](examples).

## States and transitions
The timer class implements the [State Pattern](https://en.wikipedia.org/wiki/State_pattern). Methods that modify the timer state may only be called when the timer is in a supported state.

Any transition not listed in the diagram will raise an [`InvalidStateError`](sources/aiotimer/error/state_error.py). For example, you cannot `reset()` a timer while it is in the `InitialState`, and you cannot `run()` a timer that is in the `CompleteState`.

This design is used as a defensive programming technique that helps catch any logic errors in the code early and simplifies the debugging process.

![](.assets/state-diagram.png)

## Interval Generator Factories
[Interval Generator Factories](sources/aiotimer/interval/generator) (IGFs) are responsible for the making of Interval Generators. Which in turn are responsible for the generation of interval durations for timers. 

There are many built-in IGFs that should cover the majority of common use cases.

```python
from aiotimer.interval import *

# Generates 1 interval of 5 seconds.
once(5)


# Generates 2 intervals of 5 seconds each.
twice(5)


# Generates 3 intervals of 5 seconds each.
thrice(5)


# Generates 1 interval between 5 and 10 seconds.
randomly(5, 10)


# Generates 3 intervals of 1, 2, and 3 seconds.
sequentially(1, 2, 3)


# Generates 5 intervals of: 1, 2, 4, 8, and 16 seconds (powers of 2).
exponentially(2, interval_count=5)


# Generates 5 intervals of: 1, 2, 4, 8, and 16 seconds (powers of 2).
exponentially(2, maximum_duration=16)


# Generates 30 intervals of 1, 2, 3, 1, 2, 3, ... seconds.
# Any IGF may be passed as the first argument.
repeatedly(sequentially(1, 2, 3), 10)


# Generates an infinite number of intervals of 1, 2, 3, 1, 2, 3, ... seconds.
# Any IGF may be passed as the first argument.
forever(sequentially(1, 2, 3))


# Generates 3 intervals of 5±0.5 seconds (10% relative jitter).
# Any IGF may be passed as the first argument.
jittery(thrice(5), relative=0.1)


# Generates 3 intervals of 5±0.5 seconds (0.5 second absolute jitter).
# Any IGF may be passed as the first argument.
jittery(thrice(5), absolute=0.5)


# Generates 4 intervals of 0, 5, 5, and 5 seconds.
# Any IGF may be passed as the first argument.
immediately_then(thrice(5))


# Generates no intervals.
# Used in the test suite for testing edge cases. 
never()
```

> If you believe some type of Interval Generator Factory is missing, feel free to submit an issue or a pull request.

## Event system
All event handlers **must** comply with the following API contract. Non-compliant event handlers result in undefined behavior.
* Event handler **must** have either:
    * Zero parameters.
    * Exactly one positional parameter accepting the corresponding event object type.
* An event handler's signature **must not** be modified at runtime after registration with the timer object.
* Event handler **should not** return any values because they will be ignored and discarded by the timer.
* Event handler **may** be either:
  * Synchronous callable.
  * Asynchronous callable.

> All event objects have a `timer` property that references the timer object that fired the event.

> Any public method of a timer object may be safely called from any event handler. The internal timer architecture prevents any race conditions and deadlocks from occurring. 

### Timer complete event
This event is fired each time the last interval of a timer is complete. An `on_timer_complete` handler **_may_** optionally accept a [`TimerCompleteEvent`](sources/aiotimer/event/timer_complete_event.py) object. Events of this type have the following properties:
* `timer: Timer|MultiTimer`
* `interval_count: int`

### Interval complete event
This event is fired each time any interval of a timer is complete. An `on_interval_complete` handler **_may_** optionally accept an [`IntervalCompleteEvent`](sources/aiotimer/event/interval_complete_event.py) object. Events of this type have the following properties:
* `timer: MultiTimer`
* `interval_number: int`
* `interval_duration: float`

### Error event
This event is fired each time any exception is propagated from any of the event handlers described above. Additionally, it is fired when an exception occurs inside a system coroutine of a timer. An `on_error` handler **_may_** optionally accept an [`ErrorEvent`](sources/aiotimer/event/error_event.py) object. Events of this type have the following properties:
* `timer: Timer|MultiTimer`
* `error: Exception`

## Advanced usage

### Configuring precision
The timer class has a configurable `precision: float` parameter. It represents the amount of seconds a timer would idle between its system ticks.

For adequate accuracy, it is recommended to have the precision value configured significantly (at least several times) smaller than the shortest interval the timer would have.

At the same time, having the precision configured to an extremely low value (e.g. `0.001`) may yield a high CPU load.

### Custom intervals
The first argument to the timer constructor is an [`Interval Generator Factory`](sources/aiotimer/interval/generator/generator.py). In other words, it is a callable that returns a generator that yields interval durations.

> This design decision is required to support multiple functionalities.
>
> A regular list of interval durations could not be used because this would not allow having an infinite number of intervals.
>
> A regular generator object could not be used because it could not be reset to its initial state, which is required to support the `timer.reset()` functionality.

```python
from asyncio import run, sleep

from aiotimer import MultiTimer


async def main() -> None:
  # The simplest form of the Interval Generator Factory.
  intervals = lambda: (duration for duration in [1, 2, 3])

  timer = MultiTimer(intervals, lambda: print('6 seconds passed'))
  await timer.start()

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

Additionally, convenient `Quick QA` and `Full QA` run configuration are provided for `PyCharm` users.
