from math import log10
from functools import lru_cache
from veramath import T


def loose_match(a: float, b: float, threshold: int = 5) -> bool:
    """Loosely match two floats. Threshold is the number of decimal places necessary.

    Args:
        a (float): The first float.
        b (float): The second float.
        threshold (int, optional): The minimum number of matched decimal places. Defaults to 5.

    Returns:
        bool: Whether or not the floats loosely match.
    """
    return a == b or log10(abs(a - b)) <= -threshold - 1


def cache(func, maxsize = 512) -> callable:
    """Wrapper for functools.lru_cache that allows for annotations and docstrings to carry over on VSCode.

    Args:
        func (Any): The function to cache.
        maxsize (int, optional): The maximum size of the cache. Defaults to 512.

    Returns:
        callable: The _lru_cache_wrapper cached function.
    """
    return lru_cache(maxsize = maxsize)(func)

    #if hasattr(func, '__annotations__'):
    #    new_func.__annotations__ = func.__annotations__

    #if hasattr(func, '__doc__'):
    #    new_func.__doc__ = lambda _ : "(Cached using verahelper.cache)\n\n" + func.__doc__
    
    #return new_func