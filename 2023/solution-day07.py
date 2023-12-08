# Libraries
import functools
from pathlib import Path
from collections import Counter

HAND_TO_STRENGTH = {
    'five': 7,
    'four': 6,
    'house': 5,
    'three': 4,
    'two': 3,
    'one': 2,
    'high': 1
}

STRENGTH_TO_HAND = {v:k for k,v in HAND_TO_STRENGTH.items()}


def hand_strength(cards, use_joker=False):
    """"""
    if not use_joker:
        return simple_hand_strength(cards)
    return joker_hand_strength(cards)


def simple_hand_strength(cards):
    """
    1. Five of a kind  => len(k) = 1
    2. Four of a kind  => len(k) = 2 & mode = 4
    3. Full house      => len(k) = 2 & mode = 3
    4. Three of a kind => len(k) = 3 & mode = 3
    5. Two pair        => len(k) = 3 & mode = 2
    6. One pair        => len(k) = 4
    7. High card       => len(k) = 5

    """
    c = Counter(cards)
    k = c.keys() # keys
    m = c.most_common(1)[0][1] # mode
    if len(k) == 1:
        return 'five'
    elif (len(k) == 2) & (m == 4):
        return 'four'
    elif (len(k) == 2) & (m == 3):
        return 'house'
    elif (len(k) == 3) & (m == 3):
        return 'three'
    elif (len(k) == 3) & (m == 2):
        return 'two'
    elif len(k) == 4:
        return 'one'
    elif len(k) == 5:
        return 'high'
    else:
        print("==> missed!", cards, c)


def joker_hand_strength(cards):
    """
    What if J can be any value?

        if <five of a kind> => ignore
        if <four of a kind> => cast to mode
        if <full house> => cast to the other
        if <three of a kind>
            if J is mode => cast to other
            if J not mode => cast to mode
        if <two pair>
            if J in pair => cast to pair
            if J alone => cast to pair
        if <one pair>
            if J in pair => cast to other
            if J alone => cast to pair
        if <high card> => ignore

    .. note: We can rewrite the cards, or just return a
             different hand_strength taking into account
             the possible conversions.

    """
    if not 'J' in cards:
        return hand_strength(cards)

    c = Counter(cards)
    k = c.keys()                # keys
    m = c.most_common(1)[0][1]  # key and mode

    if len(k) == 1:                # JJJJJ
        return 'five'
    elif (len(k) == 2) & (m == 4): # JJJJ2 or 2222J
        return 'five'
    elif (len(k) == 2) & (m == 3): # JJJ22 or JJ222
        return 'five'
    elif (len(k) == 3) & (m == 3): # JJJ23 or J2333
        return 'four'
    elif (len(k) == 3) & (m == 2): # JJ223 or J2233
        if cards.count('J') > 1:
            return 'four'
        else:
            return 'house'
    elif len(k) == 4:              # J2344 or JJ234
        return 'three'
    elif len(k) == 5:              # J2345
        return 'one'
    else:
        print("==> missed!", cards, c)


def compare(a, b):
    """Each param is an array with [cards, bid, strength]"""
    if a[-1] == b[-1]:
        for ai, bi in zip(a[0], b[0]):
            if CARDS.index(ai) == CARDS.index(bi):
                continue
            return CARDS.index(ai) > CARDS.index(bi)
        return 0
    else:
        return a[-1] > b[-1]

class Hand:
    """Basic class hand."""
    def __init__(self, v, use_joker=False):
        if isinstance(v, str):
            cards, bid = v.split()
            self.cards = cards
            self.bid = int(bid)
            self.type = hand_strength(cards, use_joker)
            self.strength = HAND_TO_STRENGTH[self.type]

        # Save vector
        self.v = [
            self.cards, self.bid, self.type, self.strength
        ]

    def __lt__(a, b):
        return compare(a.v, b.v)

    def __gt__(a, b):
        return compare(a.v, b.v)

    def __str__(self):
        return str(self.v)

    def __repr__(self):
        return str(self.v)


def part1(input):
    """Solution to part 1."""
    # Get lines
    lines = input.split("\n")
    # Create game
    game = sorted([Hand(h, use_joker=False) for h in lines], reverse=True)
    # Compute score
    answer = 0
    for i, e in enumerate(game):
        answer += e.bid * (i + 1)
    return answer


def part2(input):
    """Solution to part 2."""
    # Get lines
    lines = input.split("\n")
    # Create game
    game = sorted([Hand(h, use_joker=True) for h in lines], reverse=True)
    # Compute score
    answer = 0
    for i, e in enumerate(game):
        answer += e.bid * (i + 1)
    return answer


# -------------------------------------
# Main
# -------------------------------------
# Path
path = Path('data/day07')

with open(path / 'sample02.txt', 'r') as f:
    lines  = f.read()

# Show
CARDS = 'AKQJT98765432'[::-1]
print(part1(lines))
CARDS = 'AKQT98765432J'[::-1]
print(part2(lines))



"""
# For some reason the sorting using functools was
# not working, so the method using the class and
# the __gt__ and __lt__ was used. 

game = []
for l in lines:
    cards, bid = l.split()
    strength = hand_strength(cards)
    game.append([cards, bid, strength])

# For some reason the cmp_to_key is not working.
ordered = sorted(game, key=functools.cmp_to_key(compare))
"""