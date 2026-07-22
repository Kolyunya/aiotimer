from pytest import approx, mark, raises

from aiotimer.duration.factory import backoff
from aiotimer.error import InvalidConfigurationError


def test_only_one_of_retries_or_maximum_duration_may_be_specified() -> None:
    with raises(InvalidConfigurationError) as error:
        backoff(retries=5, maximum_duration=60)

    assert str(error.value) == 'Only one of `retries` and `maximum_duration` may be specified'


@mark.parametrize('retries', [-1, 0])
def test_retries_must_be_greater_than_zero(retries: int) -> None:
    with raises(InvalidConfigurationError) as error:
        backoff(retries=retries)

    assert str(error.value) == 'Retries count must be greater than zero'


@mark.parametrize('maximum_duration', [-1, 0])
def test_maximum_duration_must_be_greater_than_zero(maximum_duration: int) -> None:
    with raises(InvalidConfigurationError) as error:
        backoff(maximum_duration=maximum_duration)

    assert str(error.value) == 'Maximum duration must be greater than zero'


@mark.parametrize('base', [-1, 0, 1])
def test_base_must_be_greater_than_one(base: int) -> None:
    with raises(InvalidConfigurationError) as error:
        backoff(base=base)

    assert str(error.value) == 'Exponent base must be greater than one'


@mark.parametrize('scale', [-1, 0])
def test_scale_must_be_greater_than_zero(scale: int) -> None:
    with raises(InvalidConfigurationError) as error:
        backoff(scale=scale)

    assert str(error.value) == 'Exponent scale must be greater than zero'


@mark.parametrize('jitter', [-1, -0.1])
def test_jitter_must_not_be_negative(jitter: float) -> None:
    with raises(InvalidConfigurationError) as error:
        backoff(jitter=jitter)

    assert str(error.value) == 'Relative jitter must not be negative'


def test_default_configuration() -> None:
    factory = backoff()

    durations = list(factory())

    assert len(durations) == 6
    assert durations[0] == 0.0
    assert durations[1] == approx(0.5, 0.25)
    assert durations[2] == approx(1.0, 0.25)
    assert durations[3] == approx(2.0, 0.25)
    assert durations[4] == approx(4.0, 0.25)
    assert durations[5] == approx(8.0, 0.25)


def test_canonical_growth() -> None:
    factory = backoff(base=2, scale=1, jitter=0)

    durations = list(factory())

    assert durations == [0, 1, 2, 4, 8, 16]


def test_faster_growth() -> None:
    factory = backoff(base=3, scale=1, jitter=0)

    durations = list(factory())

    assert durations == [0, 1, 3, 9, 27, 81]


def test_scale_down() -> None:
    factory = backoff(base=2, scale=0.1, jitter=0)

    durations = list(factory())

    assert durations == [0.0, 0.1, 0.2, 0.4, 0.8, 1.6]


def test_with_jitter() -> None:
    factory = backoff(base=2, scale=1, jitter=0.1)

    durations = list(factory())

    assert len(durations) == 6
    assert durations[0] == 0.0
    assert durations[1] == approx(1, 0.1)
    assert durations[2] == approx(2, 0.1)
    assert durations[3] == approx(4, 0.1)
    assert durations[4] == approx(8, 0.1)
    assert durations[5] == approx(16, 0.1)
    assert durations != [0, 1, 2, 4, 8, 16]


def test_retries_count() -> None:
    factory = backoff(retries=3, base=2, scale=1, jitter=0)

    durations = list(factory())

    assert durations == [0, 1, 2, 4]


@mark.parametrize('maximum_duration', [16, 31.999])
def test_maximum_duration(maximum_duration: float) -> None:
    factory = backoff(maximum_duration=maximum_duration, base=2, scale=1, jitter=0)

    durations = list(factory())

    assert durations == [0, 1, 2, 4, 8, 16]
