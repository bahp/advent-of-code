# Libraries
import itertools
import numpy as np
from pathlib import Path


def parse_numpy(input):
    """Parse using numpy.

    .. note: Could any of these methods be used?
             m0 = np.fromregex(path, '.', [('', str)] * 10)
             m1 = np.loadtxt(path, dtype=str)
             m2 = np.fromfile(path, dtype='S1').reshape(-1, 11)
             m3 = np.genfromtxt(path, dtype='str')
    """
    return np.array([np.array(list(l))
        for l in input.splitlines()])


def traverse(m, r=3, d=1):
    """Traverse map.

    Parameters
    ----------
    m: list of strings
        It is the board (matrix) represented as a list of
        strings which has the following shape:
            height=len(m)
            width=len(m[0])
    """
    w, h = len(m[0]), len(m)
    x, y, trees = 0, 0, 0
    while y < h:
        if m[y][x % w] == '#':
            trees += 1
        x += r
        y += d
    return trees


def traverse_numpy(m, r=3, d=1):
    """Traverse map using numpy.

    Parameters
    ----------
    m: np.2darray
        It is the board (matrix) which has been read from the
        file directly. Since shape returns (rows, cols) the
        mapping is h, w = m.shape()
    """
    h, w = m.shape
    y = np.arange(0, h, d)
    x = np.arange(0, y.shape[0]) * r
    return np.sum(m[y, x % w] == '#')


def part1(input):
    """Solution part 1"""
    return traverse(input.split("\n"), r=3, d=1)


def part1_numpy(input):
    """Solution part 1 (numpy)"""
    return traverse_numpy(parse_numpy(input), r=3, d=1)


def part2(input):
    """Solution part 2"""
    m = input.split("\n")
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    numbers = [traverse(m, r, d) for r, d in slopes]
    return np.prod(numbers)

def part2_numpy(input):
    """Solution part 2 (numpy)"""
    m = parse_numpy(input)
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    numbers = [traverse_numpy(m, r, d) for r, d in slopes]
    return np.prod(numbers)



# -------------------------------------
# Main
# -------------------------------------
# Path
path = Path('data/day03') / 'sample02.txt'

with open(path) as f:
    lines  = f.read()


# Show
print("Part 1: %s" % part1(lines))
print("Part 2: %s" % part2(lines))
print("Part 1 (numpy): %s" % part1_numpy(lines))
print("Part 2 (numpy): %s" % part2_numpy(lines))