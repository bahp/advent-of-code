# Libraries
import re
import numpy as np
from pathlib import Path

# --------------------------------
# Part 1
# --------------------------------
def part1(input):
    """Solution part 1"""
    lines = input.split("\n")
    v = np.array(lines, dtype=int)
    r = np.sum((v[1:]-v[:-1])>0)
    return r


# --------------------------------
# Part 2
# --------------------------------
def part2(input):
    """Solution part 2"""
    lines = input.split("\n")
    v = np.array(lines, dtype=int)
    count = 0
    for i in range(len(v)-3):
        s1 = sum(v[i:i+3])
        s2 = sum(v[i+1:i+1+3])
        if s2 > s1:
            count += 1
    return count

# --------------------------------
# Part 2
# --------------------------------
# Copied from morgoth1145
#
# .. note: The challenge specifically says that the sum of the
#          three consecutive elements must be larger in order
#          to be considered. This method is not checking that.
#          However, it provides the same result because...
#
#          (a + b + c) < (b + c + d) => (a < d)

def part2_ext(input):
    nums = list(map(int, input.split()))
    answer = 0
    for i in range(len(nums)-3):
        if nums[i] < nums[i+3]:
            answer += 1
    return answer


# ---------------------------------
# Main
# ---------------------------------

# Path
path = Path('./data/day01/')

# Load
with open(path / 'sample02.txt', 'r') as f:
    data  = f.read()

# Answers
print(part1(data))
print(part2(data))
print(part2_ext(data))
