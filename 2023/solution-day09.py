import re
import math
import numpy as np
import functools
from itertools import cycle
from pathlib import Path
from collections import Counter


def parse_line(l):
    return list(map(int, l.split(" ")))

def solve_next(l):
    """Find next element in list.

    .. note: Adding the last element.
    .. note: The cumulative starts in l[-1]
    """
    v, c = np.array(l), l[-1]
    while np.sum(v) != 0:
        v = np.diff(v)
        c += v[-1]
    return c


def solve_prev(l):
    """Find prev element in list.

    .. note: Instead of this, it is just possible to reverse
             the lists and call the solve_next method.
    """
    v, c = np.array(l), [l]
    while np.sum(v)!=0:
        v = np.diff(v)
        c.append(list(v))

    curr = 0
    for e in c[::-1]:
        curr = e[0] - curr
    return curr


def part1(input):
    """Solution part 1"""
    return np.sum([
        solve_next(parse_line(l))
            for l in input.split("\n")
    ])


def part2(input):
    """Solution part 2"""
    return np.sum([
        solve_prev(parse_line(l))
            for l in input.split("\n")
    ])


def part2_v2(input):
    """Solution part 2.

    .. note: Reverse the list and use part 1.
    """
    return np.sum([
        solve_next(parse_line(l)[::-1])
            for l in input.split("\n")
    ])


def part2_4HbQ(path):
    """Solution provided by 4HbQ.

    .. note: It uses recursion.
    .. note: np.diff() instead of diffs line?
    .. note: commented line and edited to return answers.
    """
    data = [[*map(int, s.split())] for s in open(path)]

    def f(l):
        diffs = [b - a for a, b in zip(l, l[1:])]
        return l[-1] + f(diffs) if l else 0

    #for dir in 1, -1:
    #    print(sum(f(l[::dir]) for l in data))

    return [
        sum(f(l[::p]) for l in data)
            for p in [1, -1]
    ]


def part2_4HbQ_numpy(path):
    """Solution provided b 4HbQ.

    .. note: Edited to use diff.
    .. note: Edited to return answers.
    """
    data = [[*map(int, s.split())] for s in open(path)]

    def f(l):
        return l[-1] + f(np.diff(l)) if len(l)>0 else 0

    answer1 = sum(f(l[::1]) for l in data)
    answer2 = sum(f(l[::-1]) for l in data)
    return answer1, answer2


def part2_4HbQ_lambda(path):
    """Solution provided by 4HbQ"""
    l = [[*map(int, l.split())] for l in open(path)]
    d = lambda l: [b - a for a, b in zip(l, l[1:])]
    f = lambda l: l[-1] + f(d(l)) if l else 0
    #for p in [1, -1]: print(sum(f(l[::p]) for l in l))

    return [
        sum(f(l[::p]) for l in l)
            for p in [1, -1]
    ]


def part2_substantial_sign_827(input):
    """Solution from substantial_sign_827.

    Notice that the differences in each "layer" are divided differences
    with the denominator equal to 1. Therefore, basically, each value in
    the original array is a value generated by a polynomial P(x), and the
    0th,1st,2nd,... elements are corresponding to P(0), P(1), P(2),...

    Suppose the array has n elements corresponding to P(0), P(1),..., P(n-1):

    - Part 1 requires us to find P(n)
    - Part 2 requires us to find P(-1)

    Lagrange's interpolation formula provides a straightforward solution.
    """

    history = input.split("\n")

    from math import comb

    def Lagrange1(nums):
        n = len(nums)
        res = 0
        for i, x in enumerate(nums):
            res += x * comb(n, i) * (-1) ** (n - 1 - i)
        return res

    def Lagrange2(nums):
        n = len(nums)
        res = 0
        for i, x in enumerate(nums):
            res += x * comb(n, i + 1) * (-1) ** i
        return res

    res1, res2 = 0, 0
    for line in history:
        nums = list(map(int, line.strip().split()))
        res1 += Lagrange1(nums)
        res2 += Lagrange2(nums)

    return res1, res2


# -------------------------------------
# Main
# -------------------------------------
# Path
path = Path('data/day09') / 'sample02.txt'

with open(path) as f:
    lines  = f.read()

# Show
print("Part 1: %s" % part1(lines))
print("Part 2:           %s" % part2(lines))
print("Part 2 (reverse): %s" % part2_v2(lines))
print("Recursion:          %s" % part2_4HbQ(path))
print("Recursion (numpy):  %s" % str(part2_4HbQ_numpy(path)))
print("Recursion (lambda): %s" % str(part2_4HbQ_lambda(path)))
print("Lagrange:           %s" % str(part2_substantial_sign_827(lines)))

