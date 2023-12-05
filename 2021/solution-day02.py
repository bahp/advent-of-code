# Libraries
import re
import numpy as np
from pathlib import Path

# -----------------------------------
# Part 1
# -----------------------------------
def part1(input):
    """Solution 1"""
    horizontal, depth = 0, 0
    for l in input.split("\n"):
        direction, m = l.split(" ")
        m = int(m)
        if direction=='forward':
            horizontal += m
        elif direction=='down':
            depth += m
        elif direction=='up':
            depth -= m
        else:
            print("not possible!")

    answer = horizontal*depth

    return answer

# -----------------------------------
# Part 2
# -----------------------------------
def part2(input):
    """Solution 2"""
    horizontal, depth, aim = 0, 0, 0
    for l in input.split("\n"):
        direction, m = l.split(" ")
        m = int(m)
        if direction=='forward':
            horizontal += m
            depth += aim * m
        elif direction=='down':
            aim += m
        elif direction=='up':
            aim -= m
        else:
            print("not possible!")

    answer = horizontal*depth
    return answer

# -------------------------------------
# Main
# -------------------------------------
# Path
path = Path('./data/day02/')

with open(path / 'sample02.txt', 'r') as f:
    data = f.read()

print(part1(data))
print(part2(data))
