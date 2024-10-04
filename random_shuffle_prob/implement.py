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
from veramath import linear_invert, prod, sigma, increment


fac = cache(factorial)
pro = cache(prod)


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


def _random_shuffle_solve(
        arr: tuple[float],
        i: int,
        base: float,
        coeff_lookup: dict[frozenset[int], float]
    ) -> float:

    n = len(arr)
    this = arr[i]
    inv_arrwi = linear_invert(arr[:i] + arr[i + 1:])

    init_sum = base * pro(increment(inv_arrwi))

    def sigma_func(j: int) -> float:
        if coeff_lookup[frozenset({j, n - j - 1})] == 0: return 0

        return coeff_lookup[frozenset({j, n - j - 1})] * _elem_symm_poly(inv_arrwi, j)

    return this * (init_sum + sigma(n - 1, 0, sigma_func))


def random_shuffle_prob(arr: tuple[float]) -> list[float]:
    """
    Given a list of floats between 0 and 1,\n
    Iterated through with a random value until the value is less than the current value,\n
    Return the probability of each item in the list.

    Args:
        arr (list[float]): The input array of floats between 0 and 1.

    Returns:
        list[float]: The probability of each item in the list.
    """

    n = len(arr)
    
    base = fac(floor((n - 1) / 2)) * fac(ceil((n - 1) / 2))
    coeff_lookup = {frozenset({x, n - x - 1}): fac(x) * fac(n - x - 1) for x in range(ceil(n / 2))}

    return [_random_shuffle_solve(arr, i, base, coeff_lookup) / fac(len(arr)) for i in range(len(arr))]


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

    TESTING: bool = False # change

    _t = perf_counter()
    this_arr = tuple(random() for _ in range(100))

    print(f"Running with n = {len(this_arr)}\n")

    out = random_shuffle_prob(this_arr)

    _t = perf_counter() - _t
    if TESTING: _t2 = perf_counter()

    if TESTING: control = test(this_arr)

    if TESTING: _t2 = perf_counter() - _t2

    print(f"Output: {out}")
    if TESTING: print(f"Test: {control}")
    if TESTING: print(f"Success? {[round(x, 6) for x in out] == [round(x, 6) for x in control]}")

    print(f"\nPermutation Sum Runtime: {_t:.6f} seconds")
    print(f"Permutation Sum Hz.: {1/_t:.6f} Hz")
    if TESTING: print(f"Test Runtime: {_t2:.6f} seconds")