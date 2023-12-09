# Libraries
import re
import numpy as np
from collections import Counter
from pathlib import Path


def parse(input):
    """Assuming boards have equal lengths.

    .. note: We could remove the mapping to integers
             since we can convert it later using the
             numpy function.

             np.array(m, dtype=int)
    """
    # Parse
    numbers, *boards = input.split("\n\n")
    numbers = list(map(int, numbers.split(",")))
    boards = [
      [list(map(int, re.findall('\d+', l)))
        for l in b.split("\n")]
          for b in boards
    ]

    return numbers, np.array(boards, dtype=int)



def solveboard(numbers, board, stop=None):
    """Solve the board.

    .. note: No need for additional mask! We could use -1 to
             indicate that that number has been drawn. Ensure
             that -1 cannot appear in the bingo card.

    .. note: To save a few iterations, we could also stop given
             a condition, for example that the current board has
             already drawn more numbers compared to the one already
             solved. But not needed.
    """
    mask = np.zeros(board.shape)
    y, z = board.shape
    i = 0
    for n in numbers:
        i+=1
        mask[board == n] = 1
        cols = np.sum(mask, axis=0)
        rows = np.sum(mask, axis=1)

        if y in cols or z in rows:
            break

        #if stop is not None:
        #    if i==stop:
        #        return i+1

    return i, mask, board, n


def part1(input):
    """Solution part 1.

    .. note: This solution runs the demo simultaneously for
             each of the boards using a 3D matrix. This might
             make the code a bit more difficult to understand.
    """
    numbers, boards = parse(input)
    masks = np.zeros(boards.shape)
    x, y, z = boards.shape

    for n in numbers:
        masks[boards == n] = 1
        cols = np.sum(masks, axis=1)
        rows = np.sum(masks, axis=2)

        if y in cols or z in rows:
            break

    # Find board and row/column index
    idxs = np.argwhere(rows == z)
    if len(idxs) == 0:
        idxs = np.argwhere(cols == y)
    bi, cri = idxs[0]

    # Get the winning board and mask
    b = boards[bi, :, :]
    m = masks[bi, :, :]

    # Compute answer
    answer = np.sum(b[m==0]) * n
    return answer


def part1_v2(input):
    """Solution part 1.

    This solution solves all boards and keeps the winner.
    """
    # Load
    numbers, boards = parse(input)
    win = []
    for b in range(boards.shape[0]):
        win.append(solveboard(numbers, boards[b,:,:]))

    # Sort from longest to shortest.
    win = sorted(win, key=lambda x: x[0], reverse=False)
    l, m, b, n = win[0]
    answer = np.sum(b[m == 0]) * n

    # Return
    return answer


def part2(input):
    """Solution part 2.

    This solution solves all boards and keeps the loser.
    """
    # Load
    numbers, boards = parse(input)
    win = []
    for b in range(boards.shape[0]):
        win.append(solveboard(numbers, boards[b,:,:]))

    # Sort from longest to shortest.
    win = sorted(win, key=lambda x: x[0], reverse=True)
    l, m, b, n = win[0]
    answer = np.sum(b[m == 0]) * n

    # Return
    return answer

# ---------------------------------
# Main
# ---------------------------------
# Path
path = Path('./data/day04/')

with open(path / 'sample01.txt', 'r') as f:
    data = f.read()

print(part1(data))
print(part1_v2(data))
print(part2(data))