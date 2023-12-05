# Libraries
import re
import numpy as np
from pathlib import Path

# Path
path = Path('./data/day01/')

# -----------------------------
# Part 1
# -----------------------------
def part1(input):
    """Solution part 1"""
    # Compute
    numbers = []
    for l in input.split("\n"):
        n1 = re.search(r'(\d)', l).group()
        n2 = re.search(r'(\d)', l[::-1]).group()
        numbers.append(int('%s%s' % (n1, n2)))

    # Return
    return np.sum(numbers)

# -----------------------------
# Part 2
# -----------------------------
# Replacements
r = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

def find_first_and_last_digits(l, map):
    """Find first and last digit (including text)

    It uses look ahead to find the character without consuming
    those characters and a simple map to convert the text to
    number if it was not a digit.
    """
    regexp = '(?=(one|two|three|four|five|six|seven|eight|nine|1|2|3|4|5|6|7|8|9))'
    n = re.findall(regexp, l)
    tmp = [n[0], n[-1]]
    tmp = [e if e.isdigit() else map[e] for e in tmp]
    return int(''.join(tmp))

def part2(input):
    """Solution part 2"""
    numbers = []
    for l in input.split("\n"):
        n = find_first_and_last_digits(l, r)
        numbers.append(n)

    # Return
    return np.sum(numbers)


# -----------------------------------------
# Main
# -----------------------------------------
# Path
path = Path('./data/day01/')

# Load input
with open(path / 'sample02.txt', 'r') as f:
    lines = f.read()

# Show answers
print(part1(lines))
print(part2(lines))
