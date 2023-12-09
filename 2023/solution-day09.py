import re
import math
import numpy as np
import functools
from itertools import cycle
from pathlib import Path
from collections import Counter


def solve_next(l):
    """Find next element in list.

    .. note: It is basically adding the last element.
    .. note: The cumulative starts in l[-1]
    """
    v, c = np.array(l), l[-1]
    while np.sum(v) != 0:
        v = np.diff(v)
        c += v[-1]
    return c


def solve_prev(l):
    """Find prev element in list"""
    v, c = np.array(l), [l]
    while np.sum(v)!=0:
        v = np.diff(v)
        c.append(list(v))

    curr = 0
    for e in c[::-1]:
        curr = e[0] - curr
    return curr


def part1(input):
    """Solve part 1"""
    cumu = 0
    for l in input.split("\n"):
        cumu += solve_next(list(map(int, l.split(" "))))
    return cumu


def part2(input):
    """Solver part 2"""
    cumu = 0
    for l in input.split("\n"):
        cumu += solve_prev(list(map(int, l.split(" "))))
    return cumu

# -------------------------------------
# Main
# -------------------------------------
# Path
path = Path('data/day09')

with open(path / 'sample02.txt', 'r') as f:
    lines  = f.read()

# Show
print(part1(lines))
print(part2(lines))
