"""
Timer Error Classes.
"""

from .duration_error import InvalidDurationError
from .event_handler_error import MissingEventHandlerError
from .generator_error import EmptyGeneratorError
from .precision_error import InvalidPrecisionError
from .state_error import InvalidStateError, InvalidStateNameError
from .timer_error import (
    InvalidConfigurationError,
    TimerError,
)

__all__ = [
    'EmptyGeneratorError',
    'InvalidConfigurationError',
    'InvalidDurationError',
    'InvalidPrecisionError',
    'InvalidStateError',
    'InvalidStateNameError',
    'MissingEventHandlerError',
    'TimerError',
]
