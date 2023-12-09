# Libraries
import re
from pathlib import Path
from collections import Counter



def parse_line(input):
    """Parse line"""
    low, high = list(map(int, re.findall('\d+', input)))
    letter, password = re.findall('[a-zA-Z]+', input)
    return low, high, letter, password


def parse_line_v2(input):
    """Parse line"""
    match = re.fullmatch(r'(\d+)-(\d+) (.): (.+)', input)
    lo, hi, ch, word = match.groups()
    return int(lo), int(hi), ch, word


def part1(input):
    """Solution part 1"""
    count = 0
    for e in input.split("\n"):
        l, h, char, pwd = parse_line(e)
        c = Counter(pwd)
        if (l <= c[char]) and (c[char] <= h):
            count += 1
    return count


def part2(input):
    """Solution part 2"""
    count = 0
    for e in input.split("\n"):
        p1, p2, char, pwd = parse_line(e)
        if ((pwd[p1-1] == char) and (pwd[p2-1] != char)) or \
           ((pwd[p1-1] != char) and (pwd[p2-1] == char)):
            count += 1
    return count

# -------------------------------------
# Main
# -------------------------------------
# Path
path = Path('data/day02') / 'sample02.txt'

with open(path) as f:
    lines  = f.read()

# Show
print("Part 1: %s" % part1(lines))
print("Part 2: %s" % part2(lines))
