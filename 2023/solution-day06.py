# Libraries
import re
import math
import numpy as np
from pathlib import Path

def parse1(input):
    """"""
    lines = input.split("\n")
    times = list(map(int, re.findall('\d+', lines[0])))
    dists = list(map(int, re.findall('\d+', lines[1])))
    return times, dists

def parse2(input):
    """"""
    lines = input.split("\n")
    time = int("".join(re.findall('\d+', lines[0])))
    dist = int("".join(re.findall('\d+', lines[1])))
    return time, dist

def part1(input):
    """

    .. note: It could be made more efficient, since only half of the
             options need to be created as the other half gives the
             same results. Note that (*2) not always works, sometimes
             is (*2 - 1).
    """
    times, dists = parse1(input)

    wins = []
    for t,d in zip(times, dists):
        hold = np.arange(t) + 1# t // 2) + 1 # improve half are repeated
        move = t - hold
        dist = hold * move
        wins.append(np.sum(dist > d))    # *2 issue for last

    answer = np.prod(wins)
    return answer

def part2_v1(input):
    """"""
    t, d = parse2(input)
    hold = np.arange(t, dtype=np.int64) + 1
    move = t - hold
    wins = np.sum(hold * move > d)
    return wins

def part2_v2(input):
    """"""
    t, d = parse2(input)
    hold = np.arange((t-1)//2, dtype=np.int64) + 1
    move = t - hold
    wins = np.sum(hold * move > d)*2 + 1
    return wins

def part2_aimada(input):
    """Solution from aimada.

    .. note: It is wrong. It does not provide the same output
             when using the input 'sample02.txt'.
    """
    t, d = parse2(input)
    wins =  math.floor(math.sqrt(t ** 2 - 4 * d))
    return wins

def part2_paixaop(input):
    """Solution from paixaop.

    t = T - B    (1)
    D = t * B    (2)

    where t=travel time,
          T=race time,
          B=button pressed,
          D=travelled distance

    Substitute (1) in (2)

    D = (T - B) * B
    D = T*B - B^2      (3)
    B^2 - T*B + D = 0

    Use the quadratic formula to solve B, setting D to record distance + 1
    for
        ax2 + bx + c =0 th
    the solution is
        (b +- sqrt(b^2-4ac) ) / 2a
    thus
        a=B, b=-T, c=D

    .. note: (-T)^2=(T)^2

    B1 = (T + SQRT(T*T - 4 * D))/2
    B2 = (T - SQRT(T*T - 4 * D))/2

    Number f wins is B1-B2 which is the number of integer solutions
    between two record point solutions.
    """
    T, D = parse2(input)
    b1 = math.floor((T + math.sqrt(pow(T, 2) - 4 * D)) / 2)
    b2 = math.ceil((T - math.sqrt(pow(T, 2) - 4 * D)) / 2)
    return b1 - b2 + 1

# -----------------------------------
# Main
# -----------------------------------
# Path
path = Path('data/day06')

with open(path / 'sample02.txt', 'r') as f:
    lines  = f.read() #.split("\n")

print(part1(lines))
print(part2_v1(lines))
print(part2_v2(lines))
print(part2_aimada(lines))
print(part2_paixaop(lines))