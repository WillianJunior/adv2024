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
    print(np.array2string(m, separator='', 
        formatter={'str_kind': lambda x: x}))

def conv_2d(arr, conv_f):
    return [[conv_f(a) for a in line] for line in arr]


def flatten(xss):
    return [x for xs in xss for x in xs]

def main():
    inpt = []
    with open('input.txt', 'r') as f_in:
        inpt = f_in.readlines()

        # Remove \n
        inpt = [i[:-1] for i in inpt]

    start_char = 'S'
    end_char = 'E'
    path = '.'
    wall = '#'
    up = 'up'
    down = 'down'
    left = 'left'
    right = 'right'

    all_dirs = [up, down, left, right]
    all_dirs_coord = [(-1,0),(1,0),(0,-1),(0,1)]

    # Keys: (x,y)
    # Value: list of next positions with (x,y)
    maze = defaultdict(lambda: [])
    mmap = np.array([list(i) for i in inpt])

    start_pos = (-1,-1)
    end_pos = (-1,-1) # Any direction is fine

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
            if inpt[i-1][j] != wall:
                maze[i,j].append((i-1,j))
            # down edge
            if inpt[i+1][j] != wall:
                maze[i,j].append((i+1,j))
            # left edge
            if inpt[i][j-1] != wall:
                maze[i,j].append((i,j-1))
            # right edge
            if inpt[i][j+1] != wall:
                maze[i,j].append((i,j+1))

    print(maze)

    # Keys: (x,y, direction)
    # Value: best next position with (x,y,direction)
    # and distance value
    all_paths = defaultdict(lambda: sys.maxsize)

    all_paths[*end_pos, up] = 0
    all_paths[*end_pos, right] = 0

    def t_cost(init_dir, end_dir):
        if init_dir == end_dir:
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
        return (a[0]+b[0], a[1]+b[1])

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

    # Empty queue
    queue = []

    all_costs = defaultdict(lambda: sys.maxsize)

    # Add the first position to the right
    queue.append((start_pos, right, 0, 0))
    l=0
    cond = False

    while len(queue) > 0:
        cur_pos, cur_dir, cur_cost, l = queue.pop()
        if cond: print(f'{l*'  '}popping {cur_pos,cur_dir} = {cur_cost}')

        # Try new moves in all directions
        for new_dir, new_pos in zip(all_dirs, all_dirs_coord):
            new_pos = move(new_pos, cur_pos)

            if cond: print(f'{l*'  '}trying to move to {new_pos,new_dir}')

            if mmap[new_pos] == wall:
                if cond: print(f'{l*'  '}{new_pos} is a wall, skipping...')
                continue

            if reverse(cur_dir, new_dir):
                if cond: print(f'{l*'  '}reverse')
                continue

            # Calculate the cost for reaching new_pos
            turn_cost = t_cost(cur_dir, new_dir)
            new_cost = cur_cost + 1 + turn_cost

            if new_cost < all_costs[*new_pos, new_dir]:
                # This is the new best cost
                if cond: print(f'{l*'  '}adding {new_pos,new_dir} = {new_cost}')
                all_costs[*new_pos, new_dir] = new_cost
                queue.append((new_pos, new_dir, new_cost, l+1))


    print(all_costs[*end_pos, up])
    print(all_costs[*end_pos, right])


if __name__ == '__main__':
    main()