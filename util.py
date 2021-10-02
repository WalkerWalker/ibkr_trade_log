from functools import reduce
from math import gcd


def find_gcd(sequence: list):
    return reduce(gcd, sequence)
