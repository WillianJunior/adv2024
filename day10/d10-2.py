# --- Part Two ---

# The reindeer spends a few minutes reviewing your hiking 
# trail map before realizing something, disappearing for a 
# few minutes, and finally returning with yet another slightly-charred 
# piece of paper.

# The paper describes a second way to measure a trailhead called its 
# rating. A trailhead's rating is the number of distinct hiking trails 
# which begin at that trailhead. For example:

# .....0.
# ..4321.
# ..5..2.
# ..6543.
# ..7..4.
# ..8765.
# ..9....

# The above map has a single trailhead; its rating is 3 because there are 
# exactly three distinct hiking trails which begin at that position:

# .....0.   .....0.   .....0.
# ..4321.   .....1.   .....1.
# ..5....   .....2.   .....2.
# ..6....   ..6543.   .....3.
# ..7....   ..7....   .....4.
# ..8....   ..8....   ..8765.
# ..9....   ..9....   ..9....

# Here is a map containing a single trailhead with rating 13:

# ..90..9
# ...1.98
# ...2..7
# 6543456
# 765.987
# 876....
# 987....

# This map contains a single trailhead with rating 227 (because there are 
#     121 distinct hiking trails that lead to the 9 on the right edge and 
#     106 that lead to the 9 on the bottom edge):

# 012345
# 123456
# 234567
# 345678
# 4.6789
# 56789.

# Here's the larger example from before:

# 89010123
# 78121874
# 87430965
# 96549874
# 45678903
# 32019012
# 01329801
# 10456732

# Considering its trailheads in reading order, they have ratings of 
# 20, 24, 10, 4, 1, 4, 5, 8, and 5. The sum of all trailhead ratings in 
# this larger example topographic map is 81.

# You're not sure how, but the reindeer seems to have crafted some tiny 
# flags out of toothpicks and bits of paper and is using them to mark 
# trailheads on your topographic map. What is the sum of the ratings of 
# all trailheads?


import numpy as np
from numba import njit
from collections import defaultdict


def flatten(xss):
    return [x for xs in xss for x in xs]


def move(top_map, t_head):
    # Stopping condition
    if top_map[t_head] == 9:
        # print(f'stop at {t_head}')
        # return set([t_head])
        return 1

    # final_coords = set()
    final_coords = 0

    cur = top_map[t_head]
    # print(f'at {t_head}={cur}')

    # Move in all possible directions
    th_i, th_j = t_head
    moves_next = []
    h, w = top_map.shape
    
    # Up
    if th_i > 0 and top_map[th_i-1, th_j] == cur+1:
        moves_next.append((th_i-1, th_j))
    # Down
    if th_i < h-1 and top_map[th_i+1, th_j] == cur+1:
        moves_next.append((th_i+1, th_j))
    # Left
    if th_j > 0 and top_map[th_i, th_j-1] == cur+1:
        moves_next.append((th_i, th_j-1))
    # Right
    if th_j < w-1 and top_map[th_i, th_j+1] == cur+1:
        moves_next.append((th_i, th_j+1))

    # print(f'next: {moves_next}')
    
    for n in moves_next:
        # print(n)
        # final_coords.update(move(top_map, n))
        final_coords += move(top_map, n)
        # print('...done')

    return final_coords


def main():
    inpt = []
    with open('input.txt', 'r') as f_in:
        inpt = f_in.readlines()

        # Remove \n
        inpt = [i[:-1] for i in inpt]

    inpt = [[int(i) for i in iss] for iss in inpt]
    top_map = np.array(inpt)
    print(top_map)

    # Find all trailheads
    trailheads = zip(*np.where(top_map == 0))

    # Find paths for all trailheads
    count = 0
    for t_head in trailheads:
        rating = move(top_map, t_head)
        # print(f'head {t_head}: {rating}')
        count += rating

    print(count)

if __name__ == '__main__':
    main()