# Libraries
import numpy as np

from pathlib import Path
from itertools import combinations

def numpy2str(m):
    return '\n'.join([''.join(e) for e in m])


def parse(input):
    return np.array([np.array(list(l))
        for l in input.splitlines()])


def expand_map(m):
    """Expand the map with galaxies"""
    # Find vectors to repeat
    r, c = m.shape
    cols = (np.sum(m=='.', axis=0) == c) + 1
    rows = (np.sum(m=='.', axis=1) == r) + 1

    # Repeat
    E = np.repeat(m, cols, axis=1)
    E = np.repeat(E, rows, axis=0)
    
    # Return
    return E

def expand_coords(coords, m, n_copies=1e6):
    """Expand just the coordinates of galaxies"""
    r, c = M.shape
    cols = np.argwhere(np.sum(m == '.', axis=0) == c).flatten()
    rows = np.argwhere(np.sum(m == '.', axis=1) == r).flatten()

    expanded = []
    for i, j in coords:
        a = i + n_copies*(np.sum(i>=rows))
        b = j + n_copies*(np.sum(j>=cols))
        expanded.append((a,b))

    return expanded


def manhattan(a, b):
    """Compute the manhattan distance"""
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))


def part1_map():
    """Solution part 1.

    .. note: We are manually expending the rows and columns. And
             computing the manhattan distance for each pair of
             galaxies. This approach is very limited, not feasible
             to expand each row/col by a factor of 1e6 (part2).
    """
    # Find galaxies on the expanded map
    galaxies = np.argwhere(expand_map(M) == '#').tolist()
    return int(np.sum([manhattan(c0, c1)
        for c0, c1 in combinations(galaxies, 2)
    ]))


def part1():
    """Solution part 1"""
    galaxies = np.argwhere(M == '#').tolist()
    galaxies = expand_coords(galaxies, M, n_copies=1)
    return int(np.sum([manhattan(c0, c1)
        for c0, c1 in combinations(galaxies, 2)
    ]))


def part2():
    """Solution part 2"""
    galaxies = np.argwhere(M == '#').tolist()
    galaxies = expand_coords(galaxies, M, n_copies=1e6-1)
    return int(np.sum([manhattan(c0, c1)
        for c0, c1 in combinations(galaxies, 2)
    ]))


def part2_4hbQ(filename):
    """Solution from 4hbQ.

    .. note: This is golfing... trying to make code short.
    """
    return sum(map(lambda g:
        sum(sum(map(i.__ge__, g)) * (i in g or 1000000) *
            sum(map(i.__lt__, g)) for i in range(max(g))),
                zip(*[(x, y) for y, r in enumerate(open(filename))
                    for x, c in enumerate(r) if c == '#'])))




# -------------------------------------
# Main
# -------------------------------------
# .. note: If issue the recursive approach, it is necessary
# to increase the recursion limit to compute the solution.
# Otherwise it will raise a recursion limit exceeded error.
#sys.setrecursionlimit(1000000)

# Path
path = Path('data/day11') / 'sample02.txt'

with open(path) as f:
    lines  = f.read()

# Define the map globally
M = parse(lines)

# Show
print("Part1 (map):    %s" % part1_map())
print("Part1 (coords): %s" % part1())
print("Part2 (coords): %s" % part2())
print("Part2 (4hbQ):   %s" % part2_4hbQ(path))