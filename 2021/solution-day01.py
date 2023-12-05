# Libraries
import re
import numpy as np
from pathlib import Path

# Path
path = Path('./data/day01/')

with open(path / 'sample03.txt', 'r') as f:
    lines  = f.read().split("\n")

# --------------------------------
# Part 1
# --------------------------------
# Compute
v = np.array(lines, dtype=int)
r = np.sum((v[1:]-v[:-1])>0)

# Show
print(r)

# --------------------------------
# Part 2
# --------------------------------
count = 0
for i in range(len(v)-3):
    s1 = sum(v[i:i+3])
    s2 = sum(v[i+1:i+1+3])
    if s2 > s1:
        count += 1
print(count)

# --------------------------------
# Part 2
# --------------------------------
# Copied from morgoth1145
#
# .. note: The challenge specifically says that the sum of the
#          three consecutive elements must be larger in order
#          to be considered. This is not checking that. However,
#          it provides the same result.
#
#          (a + b + c) < (b + c + d) => (a < d)

def part2(s):
    nums = list(map(int, s.split()))
    answer = 0
    for i in range(len(nums)-3):
        if nums[i] < nums[i+3]:
            answer += 1
    return answer

print(part2(" ".join(lines)))