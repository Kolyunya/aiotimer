from os import getenv
from warnings import warn

from .utility.boolean import parse_boolean

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


# The library's modules must be imported after beartype initialization
# for runtime type checking to be enabled.
from .timer import Timer
from .timer_interface import TimerInterface

__all__ = [
    'Timer',
    'TimerInterface',
]
