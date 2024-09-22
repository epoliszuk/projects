"""Python implementation of the "Probability of Individual Items in a Randomly Shuffled List" problem.

Important functions:
- ``random_shuffle_prob`` -> ``list[float]``
- ``test`` -> ``list[float]``
- ``inCr`` -> ``int``
"""

from itertools import permutations
from math import ceil, floor, factorial, inf
from random import random
from verahelper import cache
from veramath import linear_invert, prod, sigma


fac = cache(factorial)
pro = cache(prod)


@cache
def inCr(n: int, k: int) -> int:
    """1 over ``n`` choose ``k``.

    Args:
        n (int): Number of items.
        k (int): Number of items to choose.

    Returns:
        int: The number of combinations for ``n`` items choose ``k`` raised to the -1 power.
    """
    if k > n: return inf
    return fac(k) * fac(n - k) / fac(n)


@cache
def _elem_symm_poly(arr: tuple[float], deg: int) -> float:
    """Elementary symmetric polynomial of a given degree using elements of ``arr``.

    Args:
        arr (tuple[float]): Tuple of floats to use for the el. symmetric polynomial.
        deg (int): The degree of the polynomial.

    Returns:
        float: The el. symmetric polynomial for the given input.
    """
    if deg == len(arr): return pro(arr)
    if deg == 0: return 1
    if deg == 1: return sum(arr)
    if deg > len(arr): return 0

    return sum(arr[i] * _elem_symm_poly(arr[i + 1:], deg - 1) for i in range(len(arr)))


def _random_shuffle_solve(arr: list[float], i: int) -> float:
    arr_without_i = tuple(arr[:i] + arr[i + 1:])
    n = len(arr)
    this = arr[i]
    inv_arrwi = linear_invert(arr_without_i)

    sumfunc = lambda j : inCr(n, j + 1) / (j + 1) * (_elem_symm_poly(inv_arrwi,j) + _elem_symm_poly(inv_arrwi, n - j - 1))

    init_sum = this * sigma(floor(.5 * n) - 1, 0, sumfunc)

    if n % 2 == 1:
        return init_sum + this * inCr(n, floor(n/2) + 1) / (ceil(n/2)) * _elem_symm_poly(inv_arrwi, floor(.5 * n))
    
    return init_sum


def random_shuffle_prob(arr: list[float]) -> list[float]:
    """
    Given a list of floats between 0 and 1,\n
    Iterated through with a random value until the value is less than the current value,\n
    Return the probability of each item in the list.

    Args:
        arr (list[float]): The input array of floats between 0 and 1.

    Returns:
        list[float]: The probability of each item in the list.
    """

    # / fac(len(arr))
    return [_random_shuffle_solve(arr, i)  for i in range(len(arr))]


def _base_solve(arr: tuple[float,...]) -> float:
    if len(arr) == 1:
        return arr[0]
    return arr[-1] * pro(linear_invert(arr[:-1]))


def test(this_arr: list[float]) -> list[float]:
    """Brute force method for testing.

    Args:
        this_arr (list[float]): The input array of floats.

    Returns:
        list[float]: The output array of respective probabilities.
    """
    out = [0] * len(this_arr)

    for p in permutations(this_arr):
        for ind, item in enumerate(p):
            out[this_arr.index(item)] += _base_solve(p[:ind + 1])

    return [x / fac(len(this_arr)) for x in out]


if __name__ == "__main__":
    from time import perf_counter

    _t = perf_counter()
    this_arr = [random() for _ in range(20)]

    print(f"Running with n = {len(this_arr)}\n")

    out = random_shuffle_prob(this_arr)

    _t = perf_counter() - _t
    #_t2 = perf_counter()

    #control = test(this_arr)

    #_t2 = perf_counter() - _t2

    print(f"Output: {out}")
    #print(f"Test: {control}")
    #print(f"Success? {[round(x, 6) for x in out] == [round(x, 6) for x in control]}")

    print(f"\nPermutation Sum Runtime: {_t:.6f} seconds")
    print(f"Permutation Sum Hz.: {1/_t:.6f} Hz")
    #print(f"Test Runtime: {_t2:.6f} seconds")