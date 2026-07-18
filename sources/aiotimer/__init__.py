from os import getenv
from warnings import warn

from .timer import Timer
from .timer_interface import TimerInterface
from .utility.boolean import parse_boolean

__all__ = [
    'Timer',
    'TimerInterface',
]

if parse_boolean(getenv('BEARTYPE', '')):
    try:
        from beartype import BeartypeConf
        from beartype.claw import beartype_this_package

        beartype_this_package(conf=BeartypeConf(
            is_pep484_tower=True,
        ))

    except ImportError:
        warning = 'Beartype is not installed. Type checking is disabled.'
        warn(warning, stacklevel=2)
