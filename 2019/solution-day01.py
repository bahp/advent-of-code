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
    cumu = 0
    for mass in parse(input):
        while True:
            mass = math.floor(mass / 3) - 2
            if mass < 0:
                break
            cumu += mass
    return cumu

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