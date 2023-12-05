# Libraries
import re
import numpy as np
from pathlib import Path

# Path
path = Path('./data/day02/')

with open(path / 'sample02.txt', 'r') as f:
    lines  = f.read().split("\n")

# -----------------------------------
# Part 1
# -----------------------------------
horizontal, depth = 0, 0
for l in lines:
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
print(answer)

# -----------------------------------
# Part 2
# -----------------------------------
horizontal, depth, aim = 0, 0, 0
for l in lines:
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
print(answer)