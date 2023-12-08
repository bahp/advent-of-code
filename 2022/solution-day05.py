# Libraries
import re
import numpy as np
from pathlib import Path
from collections import deque


def parse_moves(input):
    """Parse instructions."""
    moves = input.split("\n\n")[1]
    return [
        tuple(map(int, re.findall(r"\d+", move)))
            for move in moves.strip().split("\n")
    ]


def parse_stacks(input):
    """Parse the stacks.

    .. note: Assumes stacks only have one letter components and
             exploits the fact that they are a fixe distance
             apart from each other.
    """
    board, moves = input.split("\n\n")
    numbers = re.findall('\d+', board.split("\n")[-1])
    stacks = [""] * max(list(map(int, numbers)))
    for line in board.split("\n")[:-1]:
        for i, box in enumerate(line[1::4]):
            if box != " ":
                stacks[i] += box
    return stacks


def solvecrane(input, is_cr9001=False):
    """Solve crane problem.

    Params
    ------
    is_cr9001: bool
       If true, various crates are moved at once and therefore
       the order remains. Otherwise, crates can only be moved
       one by one.
    """
    # Get information
    stacks = parse_stacks(input)
    moves = parse_moves(input)

    # Loop
    for m in moves:
        n, f, t = m
        mv = stacks[f - 1][:n]
        mv = mv if is_cr9001 else mv[::-1]
        stacks[t - 1] = mv + stacks[t - 1]
        stacks[f - 1] = stacks[f - 1][n:]

    # Return
    return stacks


def part1(input):
    """Solution part 1."""
    stacks = solvecrane(input, is_cr9001=False)
    answer = ''.join([e[0] for e in stacks])
    return answer


def part2(input):
    """Solution part 2."""
    stacks = solvecrane(input, is_cr9001=True)
    answer = ''.join([e[0] for e in stacks])
    return answer





# ---------------------------------------------
# Main
# ---------------------------------------------
# Path
path = Path('data/day05')

with open(path / 'sample02.txt', 'r') as f:
    lines = f.read()

# Show
print(part1(lines))
print(part2(lines))