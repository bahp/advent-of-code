# Libraries
import math
import itertools
import numpy as np
from pathlib import Path


def parse(input):
    return list(map(int, input.split("\n")))


def part1(input):
    """Solution part 1"""
    return sum([math.floor(m/3)-2 for m in parse(input)])


def part2(input):
    """Solution part 2"""
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