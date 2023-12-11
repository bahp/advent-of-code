import re
import math
import numpy as np
import sys
import time

from pathlib import Path
from functools import wraps
from collections import Counter

# This is the adjacency list uset to compute the neighbors. It
# It contains for the current location, the possible movements
# towards North (N), East (E), South (S) and West (W) of the
# map.
# N = -1, S = 1, W = -1, E = 1
ADJ = {
    '.': [],  # No pipe
    '|': [[-1, 0], [1, 0]],  # N-S
    '-': [[0, 1], [0, -1]],  # E-W
    'L': [[-1, 0], [0, 1]],  # N-E
    'J': [[-1, 0], [0, -1]], # N-W
    '7': [[1, 0], [0, -1]],  # S-W
    'F': [[1, 0], [0, 1]],   # S-E
    'S': [[1,0], [0,1], [-1,0], [0, -1]],  # N-S-W-E
}

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Part2 ({func.__name__}): {result} | Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


def simulation(pth):
    for e in pth:
        show(*e)

def numpy2str(m):
    return '\n'.join([''.join(e) for e in m])

def show(x, y, neighbors=None):
    tmp = M.copy()
    tmp[x, y] = 'O'
    print("\nPoint: (%s, %s) | %s" % (x, y, M[x,y]))
    if neighbors is not None:
        print("Neighbors: %s" % str(neighbors))
    print(numpy2str(tmp))

def parse(input):
    return np.array([np.array(list(l))
        for l in input.splitlines()])


def get_neighbors(node, letter=None):
    """Compute the neighbors.

    .. note: Not possible to move outside map.
    """
    h, w = M.shape
    neighbors = []
    adj = ADJ[M[node]] if letter is None else ADJ[letter]
    for r,c in adj:
        i,j = node[0]+r, node[1]+c
        if i<0 or j<0 or i>=h or j>=w:
            continue
        neighbors.append((i,j))
    return neighbors


def dfs(visited, graph, node):
    """Depth first search (recursive)

    .. note: It traces and returns the path.
    .. note: The graph ends when node 'S' is reached. Since we can only
             go up, down, left and right, the minimum length to reach the
             start point S within a loop is 4. This ensures that the first
             iterations in which we could access S straight away from the
             neighbors are ignored.
    """

    if (M[node] == 'S') and (len(visited) > 3):
        return [node]

    if node not in visited:
        visited.add(node)
        neighbors = get_neighbors(node)
        if VERBOSE:
            show(*node, neighbors)
        for next in neighbors:
            way = dfs(visited, graph, next)
            if way:
                way.append(node)
                return way
    return []


def ray_tracing(x,y,poly):
    """Copied from stack overflow just for checking.

    .. note: See https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
    """
    n = len(poly)
    inside = False
    p2x = 0.0
    p2y = 0.0
    xints = 0.0
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside



@timeit
def polygon_contains_points_mpl(pth, points):
    """"""
    import matplotlib as mpl
    polygon = mpl.path.Path(pth, closed=True)
    return np.sum(polygon.contains_points(points))

@timeit
def polygon_contains_points_shapely(pth, points):
    """"""
    from shapely.geometry import Point
    from shapely.geometry.polygon import Polygon
    polygon = Polygon(pth)
    count = 0
    for i, j in points:
        if polygon.contains(Point(i, j)):
            count += 1
    return count

@timeit
def polygon_contains_points_ray(pth, points):
    """"""
    # Using ray
    pth = np.array(pth)
    count = 0
    for i,j in points:
        if ray_tracing(i, j, pth):
            count += 1
    return count


def part1(input):
    """Solution part 1.

    .. note: The start point is twice in the path, because it is
             the beginning and the end. Thus, it is necessary to
             remove 1 to the length to compute the distance.
    """

    # Find the start point.
    start = tuple(np.argwhere(M == 'S')[0])
    # Compute depth first search.
    r = dfs(set(), ADJ, tuple(start))
    # Compute answer
    answer = round(round((len(r) - 1) / 2))

    # The path is in inverse order and contains the
    # start point (S) twice, because it is beginning
    # and end.
    if SIMULATE:
        print("\n\n\nSimulation:")
        simulation(r)

    # Return
    return answer



def part2(input):
    """Solution part 2.

    .. note: Some solutions are more efficient than others.
    """
    # Find the start point.
    start = tuple(np.argwhere(M == 'S')[0])
    # Compute depth first search.
    r = dfs(set(), ADJ, tuple(start))


    def find_points(way):
        """Find those points of interest.

        .. note: Those present in way must be excluded.
        .. note: Map boundary cannot be contained in polygon.
        """
        points = []
        h, w = M.shape
        for i in range(1, h-1):
            for j in range(1, w-1):
                if (i, j) in r:
                    continue
                points.append((i,j))
        return points

    # Get points of interest
    points = find_points(r)

    answer1 = polygon_contains_points_mpl(r, points)
    #answer2 = polygon_contains_points_shapely(r, points)  # slow
    #answer3 = polygon_contains_points_ray(r, points)      # very slow

    # Return
    return answer1




# -------------------------------------
# Main
# -------------------------------------
# .. note: If issue the recursive approach, it is necessary
# to increase the recursion limit to compute the solution.
# Otherwise it will raise a recursion limit exceeded error.
sys.setrecursionlimit(1000000)

# Config
SIMULATE = False
VERBOSE = False

# Path
path = Path('data/day10') / 'sample05.txt'

with open(path) as f:
    lines  = f.read()

# Define the map globally
M = parse(lines)

# Show
print("Part1: %s" % part1(lines))
print("Part2: %s" % part2(lines))

# Output:
#Part1: 6773
#Part2 (polygon_contains_points_mpl): 493 | Took 0.2251 seconds
#Part2 (polygon_contains_points_shapely): 493 | Took 16.9798 seconds
#Part2 (polygon_contains_points_ray): 493 | Took 63.7521 seconds
#Part2: 493