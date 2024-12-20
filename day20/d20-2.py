# --- Part Two ---

# The programs seem perplexed by your list of cheats. Apparently,
# the two-picosecond cheating rule was deprecated several milliseconds
# ago! The latest version of the cheating rule permits a single cheat
# that instead lasts at most 20 picoseconds.

# Now, in addition to all the cheats that were possible in just two
# picoseconds, many more cheats are possible. This six-picosecond
# cheat saves 76 picoseconds:

# ###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #1#####.#.#.###
# #2#####.#.#...#
# #3#####.#.###.#
# #456.E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############

# Because this cheat has the same start and end positions as the one
# above, it's the same cheat, even though the path taken during the cheat
# is different:

# ###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S12..#.#.#...#
# ###3###.#.#.###
# ###4###.#.#...#
# ###5###.#.###.#
# ###6.E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############

# Cheats don't need to use all 20 picoseconds; cheats can last any
# amount of time up to and including 20 picoseconds (but can still
# only end when the program is on normal track). Any cheat time
# not used is lost; it can't be saved for another cheat later.

# You'll still need a list of the best cheats, but now there are even more
# to choose between. Here are the quantities of cheats in this example that
# save 50 picoseconds or more:

#     There are 32 cheats that save 50 picoseconds.
#     There are 31 cheats that save 52 picoseconds.
#     There are 29 cheats that save 54 picoseconds.
#     There are 39 cheats that save 56 picoseconds.
#     There are 25 cheats that save 58 picoseconds.
#     There are 23 cheats that save 60 picoseconds.
#     There are 20 cheats that save 62 picoseconds.
#     There are 19 cheats that save 64 picoseconds.
#     There are 12 cheats that save 66 picoseconds.
#     There are 14 cheats that save 68 picoseconds.
#     There are 12 cheats that save 70 picoseconds.
#     There are 22 cheats that save 72 picoseconds.
#     There are 4 cheats that save 74 picoseconds.
#     There are 3 cheats that save 76 picoseconds.

# Find the best cheats using the updated cheating rules. How many cheats
# would save you at least 100 picoseconds?

import numpy as np
from tqdm import tqdm
from multiprocessing import Pool
from time import time
from numba import jit
from collections import defaultdict
from math import ceil, floor, prod
import sys
from heapq import heapify, heappush, heappop

np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=np.inf)


def print_mat(m):
    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(linewidth=np.inf)
    print(np.array2string(m, separator='', formatter={'str_kind':
                                                      lambda x: x}))


def conv_2d(arr, conv_f):
    return [[conv_f(a) for a in line] for line in arr]


def flatten(xss):
    return [x for xs in xss for x in xs]


def get_neighb(pos, shape):
    h, w = shape
    i, j = pos

    ns = []
    if i > 0:
        ns.append((i - 1, j))
    if i < h - 1:
        ns.append((i + 1, j))
    if j > 0:
        ns.append((i, j - 1))
    if j < w - 1:
        ns.append((i, j + 1))

    return ns


def dktr2D(visited_dist, start_pos, end_pos=None, blockage=-1):
    # dikstra all paths algorithm for a 2D mat 'visited_dist'
    # 'visited_dist' have its path blocked by a blocking value
    # which cannot be traversed.
    # It is assumed that 'visited_dist' have all unvisited values
    # as max_value and its start position is 0.
    # If end_pos is not none, it will stop when reached

    # max_dist = sys.maxsize
    shape = visited_dist.shape
    # visited_dist = np.full(shape, max_dist)
    # visited_dist[start_pos] = 0
    unvisited_queue = []
    heappush(unvisited_queue, (visited_dist[start_pos], start_pos))

    # Try to find paths while there are options
    while len(unvisited_queue) > 0:
        dist, pos = heappop(unvisited_queue)

        ns = get_neighb(pos, shape)
        for n in ns:
            new_dist = dist + 1
            if visited_dist[n] != blockage and new_dist < visited_dist[n]:
                visited_dist[n] = new_dist
                heappush(unvisited_queue, (new_dist, n))


def find_path_from_visited(visited_dist, start_pos, end_pos, blockage=-1):
    pos = end_pos
    path = [end_pos]
    shape = visited_dist.shape
    while pos != start_pos:
        best_dist = sys.maxsize
        best_next = None
        for n in get_neighb(pos, shape):
            if visited_dist[n] != blockage and visited_dist[n] < best_dist:
                best_dist = visited_dist[n]
                best_next = n

        if best_next == None:
            return []
        else:
            path.append(best_next)
            pos = best_next

    return path


def set_path(m, path, path_val=99):
    m2 = m.copy()
    h, w = m.shape
    for p in path:
        m2[p] = path_val
    for i in range(h):
        for j in range(w):
            if m2[i, j] > sys.maxsize / 100:
                m2[i, j] = -10
    return m2


def main():
    inpt = []
    with open('input.txt', 'r') as f_in:
        inpt = f_in.readlines()

        # Remove \n
        inpt = [i[:-1] for i in inpt]

    racetrack = np.array([list(i) for i in inpt])
    h, w = racetrack.shape

    for i in range(h):
        for j in range(w):
            if racetrack[i, j] == 'S':
                start_pos = (i, j)
            if racetrack[i, j] == 'E':
                end_pos = (i, j)

    wall_char = '#'
    wall = -1
    max_dist = sys.maxsize

    search_space = np.full((h, w), max_dist)
    rev_search_space = np.full((h, w), max_dist)
    search_space[start_pos] = 0

    for i in range(h):
        for j in range(w):
            if racetrack[i, j] == wall_char:
                search_space[i, j] = wall
            else:
                rev_search_space[i, j] = wall

    dktr2D(search_space, start_pos, end_pos=None, blockage=wall)
    new_path = find_path_from_visited(search_space, start_pos, end_pos)

    path_val = 99
    path_space = set_path(search_space, new_path, path_val)
    print(path_space)
    print(new_path)
    print(len(new_path) - 1)

    # Key: (i,j), value: global improvement
    cheat_list = dict()
    cheat_count = 0

    regular_cost = search_space[end_pos]
    new_path.reverse()

    def manh_dist(ini, end):
        max_x = max(ini[0], end[0])
        min_x = min(ini[0], end[0])
        max_y = max(ini[1], end[1])
        min_y = min(ini[1], end[1])
        return (max_x - min_x) + (max_y - min_y)

    cheat_count = 0
    for i in tqdm(range(len(new_path) - 1)):
        cheat_pos_ini = new_path[i]
        for cheat_pos_end in new_path[i + 1:]:
            inter_points_cost = search_space[cheat_pos_end] - search_space[
                cheat_pos_ini]

            if manh_dist(cheat_pos_ini, cheat_pos_end) > 20:
                # print('cannot cheat that much')
                continue

            improvs = 100
            if inter_points_cost - manh_dist(cheat_pos_ini,
                                             cheat_pos_end) < improvs:
                # print('not improved enough that much')
                continue

            # print('improved')
            cheat_count += 1

    print(cheat_count)


if __name__ == '__main__':
    main()