from functools import lru_cache
from math import factorial
from veramath import prod, linear_invert, increment


fac = lru_cache(maxsize = 512)(factorial)
prod = lru_cache(maxsize = 512)(prod)


def _permutation_sum_solve(arr: list[float], ind: int) -> float:
    """Internal function for permutation_sum"""
    arr_without_ind = tuple(arr[:ind] + arr[ind + 1:])
    inv_arr_wo_ind = linear_invert(arr_without_ind)
    arr_len = len(arr)
    arr_prod = prod(inv_arr_wo_ind)

    return arr[ind] * (
        fac(arr_len - 1) * (1 + arr_prod) + 
        fac(arr_len - 2) * (prod(increment(inv_arr_wo_ind)) - 1 - arr_prod)
        )


def permutation_sum(arr: list[float]) -> list[float]:
    """
    Given a list of floats between 0 and 1,\n
    Iterated through with a random value until the value is less than the current value,\n
    Return the probability of each item in the list.

    Args:
        arr (list[float]): The input array of floats between 0 and 1.

    Returns:
        list[float]: The probability of each item in the list.
    """

    return [_permutation_sum_solve(arr, i) / fac(len(arr)) for i in range(len(arr))]
