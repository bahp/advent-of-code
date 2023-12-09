# Libraries
import itertools
import numpy as np
from pathlib import Path


def parse(input):
    return list(map(int, input.split("\n")))


def solver(input, k=2):
    """Generic solution.

    .. note: Not entirely valid since it is also considering
             the same element twice. For example, if 1010
             was there it would return 1010*1010.
    """
    n = parse(input)
    args = [n for i in range(k)]
    for n in itertools.product(*args):
        if sum(n) == 2020:
            return np.prod(n)
    return -1

def part1(input):
    """Solution part 1"""
    n = parse(input)
    for i in range(len(n)):
        for j in range(len(n)):
            if i==j:
                continue
            if n[i]+n[j] == 2020:
                return n[i]*n[j]
    return -1


def part2(input):
    """Solution part 2"""
    n = parse(input)
    for i in range(len(n)):
        for j in range(len(n)):
            if i==j:
                continue
            for k in range(len(n)):
                if i==k or j==k:
                    continue
                if n[i]+n[j]+n[k] == 2020:
                    return n[i]*n[j]*n[k]
    return -1

# -------------------------------------
# Main
# -------------------------------------
# Path
path = Path('data/day01') / 'sample01.txt'

with open(path) as f:
    lines  = f.read()

# Show
print("Part 1: %s" % part1(lines))
print("Part 2: %s" % part2(lines))
print("Part 1: %s" % solver(lines, k=2))
print("Part 2: %s" % solver(lines, k=3))
print("Part 3: %s" % solver(lines, k=4))
