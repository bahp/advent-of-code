# Libraries
import re
import numpy as np
from collections import Counter
from pathlib import Path


def invert_binary(s):
    return 1

def most_common(l, default='1', inv=False):
    """"""
    c = Counter(l).most_common(2)
    c = c[::-1] if inv else c
    if c[0][1] == c[1][1]:
        return default
    return c[0][0]



# --------------------------------------
# Part 1
# --------------------------------------
def part1(input):
    """Solution part 1"""
    # Variables
    lines = input.split("\n")
    W = len(lines[0])

    # Compute gamma
    gamma = ''
    for i in range(W):
        c0, c1 = 0,0
        for l in lines:
            if l[i] == '0':
                c0 += 1
            if l[i] == '1':
                c1 += 1
        if c0 > c1:
            gamma += '0'
        else:
            gamma += '1'

    # Compute epsilon (always inverse of gamma)
    epsilon = np.abs(np.array(list(map(int, gamma))) - 1)
    epsilon = ''.join(list(map(str, epsilon)))

    # Compute answer
    answer = int(gamma, 2) * int(epsilon, 2)
    return answer


def part1_counter(input):
    """Solution part1 using counter"""
    # Variables
    lines = input.split("\n")
    W = len(lines[0])

    # Compute gamma
    gamma = ''
    for i in range(W):
        gamma += most_common([l[i] for l in lines])

    # Compute epsilon (always inverse of gamma)
    epsilon = np.abs(np.array(list(map(int, gamma))) - 1)
    epsilon = ''.join(list(map(str, epsilon)))

    # Compute answer
    answer = int(gamma, 2) * int(epsilon, 2)
    return answer

# --------------------------------------
# Part 2
# --------------------------------------
def part2(input):
    """Solution part 2"""
    lines = input.split("\n")
    W = len(lines[0])


    o2_cand, co2_cand = lines, lines
    for i in range(W):

        if len(o2_cand) > 1:
            c0, c1 = 0, 0
            for l in o2_cand:
                if l[i] == '0':
                    c0 += 1
                if l[i] == '1':
                    c1 += 1

            m = '0' if c0>c1 else '1'
            o2_cand = [e for e in o2_cand if e[i]==m]

        if len(co2_cand) > 1:
            c0, c1 = 0, 0
            for l in co2_cand:
                if l[i] == '0':
                    c0 += 1
                if l[i] == '1':
                    c1 += 1

            m = '0' if c0 <= c1 else '1'
            co2_cand = [e for e in co2_cand if e[i]==m]

    # Compute
    o2_cand = ''.join(o2_cand)
    co2_cand = ''.join(co2_cand)
    answer = int(o2_cand, 2) * int(co2_cand, 2)

    return answer


def part2_counter(input):
    """Solution part 2"""
    lines = input.split("\n")
    W = len(lines[0])

    o2_cand, co2_cand = lines, lines
    for i in range(W):

        if len(o2_cand) > 1:
            v = [l[i] for l in o2_cand]
            m = most_common(v, inv=False, default='1')
            o2_cand = [e for e in o2_cand if e[i]==m]

        if len(co2_cand) > 1:
            v = [l[i] for l in co2_cand]
            m = most_common(v, inv=True, default='0')
            co2_cand = [e for e in co2_cand if e[i]==m]

    # Compute
    o2_cand = ''.join(o2_cand)
    co2_cand = ''.join(co2_cand)
    answer = int(o2_cand, 2) * int(co2_cand, 2)

    return answer


# ---------------------------------
# Main
# ---------------------------------
# Path
path = Path('./data/day03/')

with open(path / 'sample02.txt', 'r') as f:
    data = f.read()

print(part1(data))
print(part1_counter(data))
print(part2(data))
print(part2_counter(data))

# 198
# 230

# 2648450
# 2845944
