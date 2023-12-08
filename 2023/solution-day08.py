import re
import math
import numpy as np
import functools
from itertools import cycle
from pathlib import Path
from collections import Counter

def parse(input):
    """Parse the input"""
    lines = input.split("\n")
    nav = input.split("\n")[0]
    network = {}
    for l in lines[2:]:
        key, left, right = re.findall('\w+', l)
        network[key] = (left, right)
    return nav, network

def parse2(input):
    """Parse the input

    .. note: Not used (matrix format)."""
    lines = input.split("\n")
    nav = cycle(input.split("\n")[0])
    net = [re.findall('\w+', l) for l in lines[2:]]
    return nav, np.array(net)

def parse3(input):
    """Parse the input.

    .. note: Just an interesting approach."""
    directions, _, *str_ways = input.splitlines()
    ways = {way[0:3]: {'L': way[7:10], 'R': way[12:15]}
        for way in str_ways}
    return directions, ways

def solvesteps_for(start, nav, net):
    """Solve steps with for loop."""
    pos = start
    idx = 0
    for d in cycle(nav):
        pos = net[pos][0 if d == 'L' else 1]
        idx += 1
        if pos.endswith('Z'):
            break
    return idx

def solvesteps_while(start, nav, net):
    """Solve steps with while loop."""
    pos = start
    idx = 0
    while not pos.endswith('Z'):
        d = nav[idx % len(nav)]
        pos = net[pos][0 if d == 'L' else 1]
        idx += 1
    return idx



def part1(input):
    """Solution part 1"""
    nav, net = parse(input)
    curr = 'AAA'
    for i,e in enumerate(nav):
        idx = 1 if e=='R' else 0
        curr = net[curr][idx]
        if curr == 'ZZZ':
            break
    return i+1


def part2_v1(input):
    """Solution part 2 (just looping).

    .. note: Loop will take too long...
    .. note: Using enumerate might be slower...
    """
    nav, net = parse(input)
    curr = [e for e in net.keys() if e.endswith('A')]
    i, l = 0, len(curr)
    for e in nav:
        i += 1
        idx = 1 if e == 'R' else 0
        for j in range(l):
            curr[j] = net[curr[j]][idx]
        finish = [a for a in curr if a.endswith('Z')]
        if len(curr) == len(finish):
            break
    return i


def part2_v2(input):
    """Solution to part 2 (LCM).

    Looping through all the cases simultaneously and checking whether
    the condition is fulfilled will take too long (see part2_v2). Thus,
    a different strategy is required.

    .. note: Using the lowest common multiple LCM).
             The LCM(4,6) is 12.

    .. note: LCM(4,6,8) = LCM(LCM(4,6), 8)

    .. note: It is supposed not to work in most of the cases. However,
             the problem has been design like it. Ideally the chinese
             theorem should be usd. (read more in reddit)
    """
    nav, net = parse(input)
    ret = 1
    for start in net:
        if start.endswith('A'):
            n = solvesteps_while(start, nav, net)
            ret = math.lcm(ret, n)
    return ret


def part2_leijurv(input):
    """Solution provided by leijurv."""
    ll = [x for x in input.strip().split('\n\n')]
    import math
    inst = list(ll[0])
    conn = {}
    for l in ll[1].split("\n"):
        a = l.split(" ")[0]
        b = l.split("(")[1].split(",")[0]
        c = l.split(" ")[3].split(")")[0]
        conn[a] = (b, c)
    pos = 'AAA'
    idx = 0
    while pos != 'ZZZ':
        d = inst[idx % len(inst)]
        pos = conn[pos][0 if d == 'L' else 1]
        idx += 1
    print("p1", idx)

    def solvesteps(start):
        pos = start
        idx = 0
        while not pos.endswith('Z'):
            d = inst[idx % len(inst)]
            pos = conn[pos][0 if d == 'L' else 1]
            idx += 1
        return idx

    ret = 1
    for start in conn:
        if start.endswith('A'):
            ret = math.lcm(ret, solvesteps(start))

    return ret




# -------------------------------------
# Main
# -------------------------------------
# Path
path = Path('data/day08')

with open(path / 'sample01.txt', 'r') as f:
    lines  = f.read()

dirs, ways = parse3(lines)
print(dirs, ways)


# Show
print(part1(lines))
#print(part2_v1(lines))
print(part2_v2(lines))
print(part2_leijurv(lines))