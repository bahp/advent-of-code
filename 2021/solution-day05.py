# Libraries
import re
import numpy as np
from collections import Counter
from pathlib import Path


def parse(input):
    tuples = []
    for l in input.split("\n"):
        tuples.append(re.findall('\d+', l))
    return np.array(tuples, dtype=int)


def get_range(a, b):
    """"""
    if a<b:
        return range(a, b+1, 1)
    return range(a, b-1, -1)


def solve(x, diagonal=False):
    """Solve problem.

    .. note: when computing the ranges for the diagonals, we
             use the following code to know if we are increasing
             or decreasing and therefore set up the step
             parameter: (-1)**((x2>x1) + 1)

             x1=1, x2=3 => (-1)**(1+1) = (-1)**2 = 1
             x1=3, x2=1 => (-1)**(0+1) = (-1)**1 = -1
    """
    N = np.max(x) + 1
    m = np.zeros((N, N), dtype=int)
    for x1, y1, x2, y2 in x:
        # horizontal
        if y1==y2:
            r = range(min(x1,x2), max(x1,x2)+1)
            m[y1, r] += 1
        # vertical
        elif x1==x2:
            r = range(min(y1,y2), max(y1,y2)+1)
            m[r, x1] += 1
        # diagonal
        elif abs(x1 - x2) == abs(y1 - y2):
            if not diagonal:
                continue
            r1 = range(x1, x2 + (-1)**((x2>x1) + 1), (-1)**((x2>x1) + 1))
            r2 = range(y1, y2 + (-1)**((y2>y1) + 1), (-1)**((y2>y1) + 1))
            for i,j in zip(r1, r2):
                m[i,j] += 1

    # Return
    return np.sum(m>1)


def solve_v2(x, diagonal):
    """Solve problem.

    .. note: Identical to previous approach, but instead of using the
             ranges with max/min and the trick to get the step to be
             -1/1, we just create an easy get_range that takes all
             this things into consideration.
    """
    N = np.max(x) + 1
    m = np.zeros((N, N), dtype=int)
    for x1, y1, x2, y2 in x:
        # horizontal
        if y1 == y2:
            m[y1, get_range(x1, x2)] += 1
        # vertical
        elif x1 == x2:
            m[get_range(y1, y2), x1] += 1
        # diagonal
        elif abs(x1 - x2) == abs(y1 - y2):
            if not diagonal:
                continue
            r1 = get_range(x1, x2)
            r2 = get_range(y1, y2)
            for i, j in zip(r1, r2):
                m[i, j] += 1

    # Return
    return np.sum(m > 1)

def part1(input):
    """Solution part 1."""
    return solve(parse(input), diagonal=False)


def part2(input):
    """Solution part 2."""
    return solve(parse(input), diagonal=True)


def part2_v2(input):
    return solve_v2(parse(input), diagonal=True)


def part2_4HbQ(path):
    """Solution from 4HbQ

    .. note: Instead of fixing to 1000, we could calculate
             the length required based on the maximum number
             that appears in the file. Otherwise it might
             break.

    .. note: Horizontal and vertical lines are stored in the
             first block of grid, diagonals in the second.

    .. note: The grid[dx*dy,x,y] trick works because dx*dy
             is 0 for a horizontal or vertical line, and -1
             or +1 for a diagonal.
    """

    grid = np.zeros((2, 1000, 1000))
    ls = np.fromregex(path, '\d+', [('', int)] * 4)

    for (x, y, X, Y) in ls:
        dx, dy = np.sign([X - x, Y - y])
        while (x, y) != (X + dx, Y + dy):
            grid[dx * dy, x, y] += 1
            x += dx;
            y += dy

    answer1 = (grid[0] > 1).sum()
    answer2 = (grid.sum(0) > 1).sum()
    return answer1, answer2


def part2_semicolonator(path):
    """Solution frmo semicolonator.

    .. note: It is funny.
    .. note: It requires skimage to work.
    """
    from skimage.draw import line

    with open(path) as f:
        coords = [[[int(k) for k in c.split(",")]
            for c in x.strip().split(" -> ")]
                for x in f]

    arr1 = np.zeros((1000, 1000), dtype=np.uint8)
    arr2 = np.zeros((1000, 1000), dtype=np.uint8)

    for ((x1, y1), (x2, y2)) in coords:
        rr, cc = line(x1, y1, x2, y2)
        if x1 == x2 or y1 == y2:
            arr1[rr, cc] += 1
        arr2[rr, cc] += 1

    answer1 = len(arr1[arr1 > 1])
    answer2 = len(arr2[arr2 > 1])
    return answer1, answer2

# ---------------------------------
# Main
# ---------------------------------
# Path
path = Path('./data/day05/') / 'sample02.txt'

with open(path, 'r') as f:
    data = f.read()

print(part1(data))
print(part2(data))
print(part2_v2(data))
print(part2_4HbQ(path))