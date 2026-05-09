"""
Interval Generator Types.

Type definitions for interval generators used by timer library.

Types:
    IntervalGenerator: Generator that yields duration values for timer intervals.
    IntervalGeneratorFactory: Factory function that creates interval generators.
"""

from .interval_generator import (
    IntervalGenerator,
    IntervalGeneratorFactory,
)

__all__ = [
    'IntervalGenerator',
    'IntervalGeneratorFactory',
]
