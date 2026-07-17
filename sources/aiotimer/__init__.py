from os import getenv

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
        import logging

        logger = logging.getLogger(__name__)
        logger.warning('Beartype is not installed. Type checking is disabled.')
