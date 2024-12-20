# --- Day 20: Race Condition ---

# The Historians are quite pixelated again. This time, a massive,
# black building looms over you - you're right outside the CPU!

# While The Historians get to work, a nearby program sees that you're
# idle and challenges you to a race. Apparently, you've arrived just
# in time for the frequently-held race condition festival!

# The race takes place on a particularly long and twisting code path;
# programs compete to see who can finish in the fewest picoseconds.
# The winner even gets their very own mutex!

# They hand you a map of the racetrack (your puzzle input). For example:

# ###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############

# The map consists of track (.) - including the start (S) and end (E)
# positions (both of which also count as track) - and walls (#).

# When a program runs through the racetrack, it starts at the start
# position. Then, it is allowed to move up, down, left, or right;
# each such move takes 1 picosecond. The goal is to reach the end
# position as quickly as possible. In this example racetrack, the
# fastest time is 84 picoseconds.

# Because there is only a single path from the start to the end and the
# programs all go the same speed, the races used to be pretty boring.
# To make things more interesting, they introduced a new rule to the
# races: programs are allowed to cheat.

# The rules for cheating are very strict. Exactly once during a race,
# a program may disable collision for up to 2 picoseconds. This allows
# the program to pass through walls as if they were regular track. At
# the end of the cheat, the program must be back on normal track again;
# otherwise, it will receive a segmentation fault and get disqualified.

# So, a program could complete the course in 72 picoseconds (saving 12
# picoseconds) by cheating for the two moves marked 1 and 2:

# ###############
# #...#...12....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############

# Or, a program could complete the course in 64 picoseconds (saving
# 20 picoseconds) by cheating for the two moves marked 1 and 2:

# ###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...12..#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############

# This cheat saves 38 picoseconds:

# ###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...#...#
# ###.####1##.###
# #...###.2.#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############

# This cheat saves 64 picoseconds and takes the program
# directly to the end:

# ###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..21...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############

# Each cheat has a distinct start position (the position where the cheat
# is activated, just before the first move that is allowed to go through
# walls) and end position; cheats are uniquely identified by their start
# position and end position.

# In this example, the total number of cheats (grouped by the amount of
# time they save) are as follows:

#     There are 14 cheats that save 2 picoseconds.
#     There are 14 cheats that save 4 picoseconds.
#     There are 2 cheats that save 6 picoseconds.
#     There are 4 cheats that save 8 picoseconds.
#     There are 2 cheats that save 10 picoseconds.
#     There are 3 cheats that save 12 picoseconds.
#     There is one cheat that saves 20 picoseconds.
#     There is one cheat that saves 36 picoseconds.
#     There is one cheat that saves 38 picoseconds.
#     There is one cheat that saves 40 picoseconds.
#     There is one cheat that saves 64 picoseconds.

# You aren't sure what the conditions of the racetrack will be like, so
# to give yourself as many options as possible, you'll need a list of
# the best cheats. How many cheats would save you at least 100 picoseconds?

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
    search_space[start_pos] = 0

    for i in range(h):
        for j in range(w):
            if racetrack[i, j] == wall_char:
                search_space[i, j] = wall

    dktr2D(search_space, start_pos, end_pos=None, blockage=wall)
    new_path = find_path_from_visited(search_space, start_pos, end_pos)

    path_val = 99
    path_space = set_path(search_space, new_path, path_val)
    print(path_space)
    print(new_path)
    print(len(new_path) - 1)

    # Key: (i,j), value: global improvement
    cheat_list = dict()

    def is_horz_cheat(path_space, i, j):
        return path_space[i, j] == wall and path_space[
            i, j - 1] == path_val and path_space[i, j + 1] == path_val

    def is_vert_cheat(path_space, i, j):
        return path_space[i, j] == wall and path_space[
            i - 1, j] == path_val and path_space[i + 1, j] == path_val

    # Attempt to find a -1,99,-1 pattern, i.e., a wall
    # Return the one with the highest diff
    cheat_cost = 2
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            can_cheat = False

            if is_horz_cheat(path_space, i, j):
                if search_space[i, j - 1] < search_space[i, j + 1]:
                    cheat_start_pos = (i, j - 1)
                    cheat_end_pos = (i, j + 1)
                else:
                    cheat_start_pos = (i, j + 1)
                    cheat_end_pos = (i, j - 1)
                can_cheat = True

            if is_vert_cheat(path_space, i, j):
                if search_space[i - 1, j] < search_space[i + 1, j]:
                    cheat_start_pos = (i - 1, j)
                    cheat_end_pos = (i + 1, j)
                else:
                    cheat_start_pos = (i + 1, j)
                    cheat_end_pos = (i - 1, j)
                can_cheat = True

            if can_cheat:
                improv = search_space[cheat_end_pos] - (
                    cheat_cost + search_space[cheat_start_pos])
                cheat_list[i, j] = improv

    print(cheat_list)
    print(sum(np.array(list(cheat_list.values()))>=100))


if __name__ == '__main__':
    main()