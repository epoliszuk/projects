"""
A helper module for mathematical functions.
"""

from functools import reduce
from typing import TypeVar, overload, TypeAlias
from collections.abc import Callable, Iterable
from enum import Enum

SupportsSumT = TypeVar('SupportsSumT')
SupportsMultT = TypeVar('SupportsMultT')
SupportsRightSubT = TypeVar('SupportsRightSubT')
T = TypeVar('T')
IterableT: TypeAlias = Iterable[T]


class BasicFunctions(Enum):
    """Enum for basic functions."""
    IDENTITY = lambda x: x
    SQUARE = lambda x: x ** 2
    CUBE = lambda x: x ** 3


### Overloads ###

@overload
def sigma(upper: int, lower: int, f: Callable[[int], SupportsSumT]) -> SupportsSumT:
    """Mathematical summation operator.

    Args:
        upper (int): The upper bound of the summation.
        lower (int): The lower bound of the summation.
        f (Callable[[int], SupportsSumT]): The function to apply to each element of the summation.

    Returns:
        SupportsSumT: The completed sum.
    """
    ...
@overload
def sigma(this_set: Iterable[int], condition: Callable[[int], bool], f: Callable[[int], SupportsSumT]) -> SupportsSumT:
    """Mathematical summation operator.

    Args:
        this_set (Iterable[int]): Set to iterate through.
        condition (Callable[[int], bool]): Condition to filter the set.
        f (Callable[[int], SupportsSumT]): The function to apply to each element of the summation.

    Returns:
        SupportsSumT: The completed sum.
    """
    ...
@overload
def sigma(upper: int, lower: int, f: BasicFunctions) -> float:
    """Mathematical summation operator.

    Args:
        upper (int): The upper bound of the summation.
        lower (int): The lower bound of the summation.
        f (BasicFunctions): The basic function to apply to each element of the summation.

    Returns:
        float: The completed sum.
    """
    ...


### Implementations ###


def sigma(*args):
    if len(args) >= 3 and args[2]:
        upper, lower, f = args[:3]
        
        match f:
            case BasicFunctions.IDENTITY:
                return (upper * (upper + 1) - lower * (lower - 1)) / 2
            case BasicFunctions.SQUARE:
                return (upper * (upper + 1) * (2 * upper + 1) - lower * (lower - 1) * (2 * lower - 1)) / 6
            case BasicFunctions.CUBE:
                return (upper ** 2 * (upper + 1) ** 2 - lower ** 2 * (lower - 1) ** 2) / 4

    elif not len(args) and isinstance(args[0], int):
        upper, lower, f = args[:3]
        return sum(f(x) for x in range(lower, upper + 1))
    
    else:
        this_set, condition, f = args[:3]
        return sum(f(x) for x in this_set if condition(x))


def pi(upper: int, lower: int, f: Callable[[int], SupportsMultT]) -> SupportsMultT:
    """Mathematical product operator.

    Args:
        upper (int): The upper bound of the product.
        lower (int): The lower bound of the product.
        f (Callable[[int], SupportsSumT]): The function to apply to each element of the product.

    Returns:
        SupportsSumT: The completed product.
    """
    return f(upper) if upper == lower else f(upper) * pi(upper - 1, lower, f)


def linear_invert(arr: IterableT[T]) -> IterableT[T]:
    """Applies an inversion to an iterable of some numeric type.
    This inversion is defined as ``(1 - x)`` for ``x`` an element.

    Args:
        arr (Iterable[int]): Iterable of numbers to invert.

    Returns:
        Iterable[float]: Iterable of inverted integers.
    """
    
    return arr.__class__(1 - x for x in arr)


def increment(arr: IterableT[T]) -> IterableT[T]:
    """Increments each element of an iterable of numbers by 1.

    Args:
        arr (Iterable[int]): Iterable of numbers to increment.

    Returns:
        Iterable[float]: Iterable of incremented integers.
    """
    return arr.__class__(x + 1 for x in arr)


def prod(arr: Iterable[T]) -> T:
    """Calculates the product of an iterable of numbers.

    Args:
        arr (Iterable[int]): Iterable of numbers to multiply.

    Returns:
        float: The product of the numbers.
    """
    return reduce(lambda x, y: x * y, arr)

