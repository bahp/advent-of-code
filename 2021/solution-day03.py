# Libraries
import re
import numpy as np
from collections import Counter
from pathlib import Path

# Path
path = Path('./data/day03/')

with open(path / 'sample02.txt', 'r') as f:
    lines  = f.read().split("\n")


# --------------------------------------
# Part 1
# --------------------------------------
# Line width
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

# Show
print(gamma)
print(epsilon)
print(answer)

# --------------------------------------
# Part 2
# --------------------------------------

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
        co2_cand = [e for e in co2_cand if e[i] == m]


# Compute
o2_cand = ''.join(o2_cand)
co2_cand = ''.join(co2_cand)
answer = int(o2_cand, 2) * int(co2_cand, 2)

# Show
print(o2_cand)
print(co2_cand)
print(answer)
