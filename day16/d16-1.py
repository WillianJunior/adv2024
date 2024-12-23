# --- Day 16: Reindeer Maze ---

# It's time again for the Reindeer Olympics! This year, the big
# event is the Reindeer Maze, where the Reindeer compete for the
# loright score.

# You and The Historians arrive to search for the Chief right as
# the event is about to start. It wouldn't hurt to watch a little,
# right?

# The Reindeer start on the Start Tile (marked S) facing East and
# need to reach the End Tile (marked E). They can move forward one
# tile at a time (increasing their score by 1 point), but never
# into a wall (#). They can also rotate clockwise or counterclockwise
#     90 degrees at a time (increasing their score by 1000 points).

# To figure out the best place to sit, you start by grabbing a map
# (your puzzle input) from a nearby kiosk. For example:

# ###############
# #.......#....E#
# #.#.###.#.###.#
# #.....#.#...#.#
# #.###.#####.#.#
# #.#.#.......#.#
# #.#.#####.###.#
# #...........#.#
# ###.#.#####.#.#
# #...#.....#.#.#
# #.#.#.###.#.#.#
# #.....#...#.#.#
# #.###.#.#.#.#.#
# #S..#.....#...#
# ###############

# There are many paths through this maze, but taking any of the best
# paths would incur a score of only 7036. This can be achieved by taking
# a total of 36 steps forward and turning 90 degrees a total of 7 times:

# ###############
# #.......#....E#
# #.#.###.#.###^#
# #.....#.#...#^#
# #.###.#####.#^#
# #.#.#.......#^#
# #.#.#####.###^#
# #..>>>>>>>>v#^#
# ###^#.#####v#^#
# #>>^#.....#v#^#
# #^#.#.###.#v#^#
# #^....#...#v#^#
# #^###.#.#.#v#^#
# #S..#.....#>>^#
# ###############

# Here's a second example:

# #################
# #...#...#...#..E#
# #.#.#.#.#.#.#.#.#
# #.#.#.#...#...#.#
# #.#.#.#.###.#.#.#
# #...#.#.#.....#.#
# #.#.#.#.#.#####.#
# #.#...#.#.#.....#
# #.#.#####.#.###.#
# #.#.#.......#...#
# #.#.###.#####.###
# #.#.#...#.....#.#
# #.#.#.#####.###.#
# #.#.#.........#.#
# #.#.#.#########.#
# #S#.............#
# #################

# In this maze, the best paths cost 11048 points; following one such
# path would look like this:

# #################
# #...#...#...#..E#
# #.#.#.#.#.#.#.#^#
# #.#.#.#...#...#^#
# #.#.#.#.###.#.#^#
# #>>v#.#.#.....#^#
# #^#v#.#.#.#####^#
# #^#v..#.#.#>>>>^#
# #^#v#####.#^###.#
# #^#v#..>>>>^#...#
# #^#v###^#####.###
# #^#v#>>^#.....#.#
# #^#v#^#####.###.#
# #^#v#^........#.#
# #^#v#^#########.#
# #S#>>^..........#
# #################

# Note that the path shown above includes one 90 degree turn as the very
# first move, rotating the Reindeer from facing East to facing North.

# Analyze your map carefully. What is the loright score a Reindeer
# could possibly get?

import numpy as np
from tqdm import tqdm
from multiprocessing import Pool
from time import time
from numba import jit
from collections import defaultdict
from math import ceil, floor, prod
import sys

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


left = '<'
right = '>'
down = 'v'
up = '^'
turn_cost = 1000


def get_dir(p1, p2):
    # From p1->p2
    if p1[0] == p2[0]:
        if p1[1] > p2[1]:
            return left
        else:
            return right
    else:
        if p1[0] > p2[0]:
            return up
        else:
            return down


def is_reverse_dir(d1, d2):
    if (d1 == up and d2 == down) or (d2 == up and d1 == down):
        return True
    if (d1 == left and d2 == right) or (d2 == left and d1 == right):
        return True
    return False


def get_turn_cost(prev_pos, cur_pos, next_pos):
    d1 = get_dir(prev_pos, cur_pos)
    d2 = get_dir(cur_pos, next_pos)
    if d1 == d2:
        return 1
    if is_reverse_dir(d1, d2):
        return 2 * turn_cost + 1
    return turn_cost + 1


def dktr2D(visited_dist, start_pos, end_pos=None, blockage=-1):
    # dikstra all paths algorithm for a 2D mat 'visited_dist'
    # 'visited_dist' have its path blocked by a blocking value
    # which cannot be traversed.
    # It is assumed that 'visited_dist' have all unvisited values
    # as max_value and its start position is 0.
    # If end_pos is not none, it will stop when reached

    # This means: start pos direction is right
    prev_start_pos = (start_pos[0], start_pos[1] - 1)

    shape = visited_dist.shape
    unvisited_queue = []
    heappush(unvisited_queue,
             (visited_dist[start_pos], prev_start_pos, start_pos))

    # Try to find paths while there are options
    while len(unvisited_queue) > 0:
        dist, prev_pos, cur_pos = heappop(unvisited_queue)

        ns = get_neighb(cur_pos, shape)
        for next_pos in ns:
            new_dist = dist + get_turn_cost(prev_pos, cur_pos, next_pos)
            if visited_dist[next_pos] != blockage and new_dist < visited_dist[
                    next_pos]:
                visited_dist[next_pos] = new_dist
                heappush(unvisited_queue, (new_dist, cur_pos, next_pos))


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

    start_char = 'S'
    end_char = 'E'
    path_char = '.'
    wall_char = '#'

    max_cost = sys.maxsize
    wall = -1

    maze = np.array([list(i) for i in inpt])
    h, w = maze.shape

    search_space = np.full((h, w), wall)

    for i in range(h):
        for j in range(w):
            if maze[i, j] == path_char:
                # print(maze[i,j])
                search_space[i, j] = max_cost
            elif maze[i, j] == start_char:
                start_pos = i, j
                search_space[start_pos] = 0
            elif maze[i, j] == end_char:
                end_pos = i, j
                search_space[i, j] = max_cost

    # print(set_path(search_space, []))

    dktr2D(search_space, start_pos, end_pos=None, blockage=wall)

    # print(set_path(search_space, []))
    print(end_pos, search_space[end_pos])


if __name__ == '__main__':
    main()