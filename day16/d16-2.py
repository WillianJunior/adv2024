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


start_char = 'S'
end_char = 'E'
path = '.'
wall = '#'
up = 'up'
down = 'down'
left = 'left'
right = 'right'
ok = 'OK'

dir_char = dict()
dir_char[up] = '^'
dir_char[down] = 'v'
dir_char[left] = '<'
dir_char[right] = '>'

rev_dir_char = dict()
rev_dir_char['^'] = up
rev_dir_char['v'] = down
rev_dir_char['<'] = left
rev_dir_char['>'] = right
rev_dir_char['S'] = right
rev_dir_char['E'] = ok

all_dirs = [up, down, left, right]
all_dirs_coord = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def get_move(c1, c2):
    # from c1 to c2
    if c1[0] + 1 == c2[0]:
        return dir_char[down]
    if c1[0] - 1 == c2[0]:
        return dir_char[up]
    if c1[1] + 1 == c2[1]:
        return dir_char[right]
    if c1[1] - 1 == c2[1]:
        return dir_char[left]


def t_cost(init_dir, end_dir):
    if init_dir == end_dir:
        return 0

    if end_dir == ok:
        return 0

    if init_dir == up:
        if end_dir == left or end_dir == right:
            return 1000
        else:
            return 2000
    elif init_dir == down:
        if end_dir == left or end_dir == right:
            return 1000
        else:
            return 2000
    elif init_dir == left:
        if end_dir == up or end_dir == down:
            return 1000
        else:
            return 2000
    elif init_dir == right:
        if end_dir == up or end_dir == down:
            return 1000
        else:
            return 2000


def move(a, b):
    return (a[0] + b[0], a[1] + b[1])


def reverse(d1, d2):
    if d1 == up and d2 == down:
        return True
    if d1 == down and d2 == up:
        return True
    if d1 == left and d2 == right:
        return True
    if d1 == right and d2 == left:
        return True

    return False


def print_all_path(mmap, all_costs):
    all_map = mmap.copy()
    h, w = all_map.shape
    for i in range(h):
        for j in range(w):
            if all_map[i, j] == path:
                min_dist = sys.maxsize
                min_path = None
                for d in all_dirs:
                    if all_costs[(i, j, d)] < min_dist:
                        min_dist = all_costs[(i, j, d)]
                        min_path = (i, j, d)
                if min_dist < sys.maxsize:
                    all_map[min_path[0], min_path[1]] = dir_char[min_path[2]]

    print_mat(all_map)


def print_path(mmap, path, best_cost):
    all_map = mmap.copy()
    prev = path[0]
    cost = -1
    for p in path:
        # print(cost)
        # print_mat(all_map)
        # input()
        cost += 1
        if all_map[p] == start_char:
            prev = p
            continue

        all_map[p] = get_move(prev, p)
        cost += t_cost(rev_dir_char[all_map[prev]], rev_dir_char[all_map[p]])
        prev = p

    print(cost)
    if cost == best_cost:
        print(path)
        print(len(path))
        print_mat(all_map)
        print(cost)


def main():
    inpt = []
    with open('input.txt', 'r') as f_in:
        inpt = f_in.readlines()

        # Remove \n
        inpt = [i[:-1] for i in inpt]

    # Keys: (x,y)
    # Value: list of next positions with (x,y)
    maze = defaultdict(lambda: [])
    mmap = np.array([list(i) for i in inpt])

    start_pos = (-1, -1)
    end_pos = (-1, -1)  # Any direction is fine

    for i, l in enumerate(inpt):
        for j, c in enumerate(l):
            if c == wall:
                continue

            if c == start_char:
                # start_pos = (i, j, right)
                start_pos = (i, j)
            if c == end_char:
                end_pos = (i, j)

            # Add edges to graph

            # up edge
            if inpt[i - 1][j] != wall:
                maze[i, j].append((i - 1, j))
            # down edge
            if inpt[i + 1][j] != wall:
                maze[i, j].append((i + 1, j))
            # left edge
            if inpt[i][j - 1] != wall:
                maze[i, j].append((i, j - 1))
            # right edge
            if inpt[i][j + 1] != wall:
                maze[i, j].append((i, j + 1))

    # print(maze)

    # Keys: (x,y, direction)
    # Value: best next position with (x,y,direction)
    # and distance value
    # all_paths = defaultdict(lambda: sys.maxsize)

    # x = (*end_pos, up)
    # all_paths[x] = 0
    # x = (*end_pos, right)
    # all_paths[x] = 0

    # Empty queue
    queue = []

    all_costs = defaultdict(lambda: sys.maxsize)

    # Add the first position to the right
    queue.append((start_pos, right, 0, [start_pos], 0))
    l = 0
    cond = False
    all_paths = []

    while len(queue) > 0:
        cur_pos, cur_dir, cur_cost, cur_path, l = queue.pop()
        if cond: print(f"{l*'  '}popping {cur_pos,cur_dir} = {cur_cost}")

        if cur_pos == end_pos:
            all_paths.append(cur_path)

        # Try new moves in all directions
        for new_dir, new_pos in zip(all_dirs, all_dirs_coord):
            new_pos = move(new_pos, cur_pos)

            if cond: print(f"{l*'  '}trying to move to {new_pos,new_dir}")

            if mmap[new_pos] == wall:
                if cond: print(f"{l*'  '}{new_pos} is a wall, skipping...")
                continue

            if reverse(cur_dir, new_dir):
                if cond: print(f"{l*'  '}reverse")
                continue

            # Calculate the cost for reaching new_pos
            turn_cost = t_cost(cur_dir, new_dir)
            new_cost = cur_cost + 1 + turn_cost

            x = (*new_pos, new_dir)
            if new_cost < all_costs[x]:
                # This is the new best cost
                if cond:
                    print(f"{l*'  '}adding {new_pos,new_dir} = {new_cost}")
                all_costs[x] = new_cost
                new_path = cur_path + [cur_pos]
                queue.append((new_pos, new_dir, new_cost, new_path, l + 1))

    x = *end_pos, up
    c_up = all_costs[x]
    c_right = all_costs[x]

    best_cost = min(c_up, c_right)
    print(best_cost)

    print_all_path(mmap, all_costs)

    for p in all_paths:
        print_path(mmap, p, best_cost)


if __name__ == '__main__':
    main()