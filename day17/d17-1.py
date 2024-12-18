# --- Day 18: RAM Run ---

# You and The Historians look a lot more pixelated than you remember. 
# You're inside a computer at the North Pole!

# Just as you're about to check out your surroundings, a program runs 
# up to you. "This region of memory isn't safe! The User misunderstood 
# what a pushdown automaton is and their algorithm is pushing whole 
# bytes down on top of us! Run!"

# The algorithm is fast - it's going to cause a byte to fall into your 
# memory space once every nanosecond! Fortunately, you're faster, and 
# by quickly scanning the algorithm, you create a list of which bytes 
# will fall (your puzzle input) in the order they'll land in your memory 
# space.

# Your memory space is a two-dimensional grid with coordinates that 
# range from 0 to 70 both horizontally and vertically. However, for the 
# sake of example, suppose you're on a smaller grid with coordinates that 
# range from 0 to 6 and the following list of incoming byte positions:

# 5,4
# 4,2
# 4,5
# 3,0
# 2,1
# 6,3
# 2,4
# 1,5
# 0,6
# 3,3
# 2,6
# 5,1
# 1,2
# 5,5
# 2,5
# 6,5
# 1,4
# 0,4
# 6,4
# 1,1
# 6,1
# 1,0
# 0,5
# 1,6
# 2,0

# Each byte position is given as an X,Y coordinate, where X is the 
# distance from the left edge of your memory space and Y is the distance 
# from the top edge of your memory space.

# You and The Historians are currently in the top left corner of the 
# memory space (at 0,0) and need to reach the exit in the bottom right 
# corner (at 70,70 in your memory space, but at 6,6 in this example). 
# You'll need to simulate the falling bytes to plan out where it will be 
# safe to run; for now, simulate just the first few bytes falling into 
# your memory space.

# As bytes fall into your memory space, they make that coordinate corrupted. 
# Corrupted memory coordinates cannot be entered by you or The Historians, 
# so you'll need to plan your route carefully. You also cannot leave the 
# boundaries of the memory space; your only hope is to reach the exit.

# In the above example, if you were to draw the memory space after the 
# first 12 bytes have fallen (using . for safe and # for corrupted), 
#     it would look like this:

# ...#...
# ..#..#.
# ....#..
# ...#..#
# ..#..#.
# .#..#..
# #.#....

# You can take steps up, down, left, or right. After just 12 bytes 
# have corrupted locations in your memory space, the shortest path 
# from the top left corner to the exit would take 22 steps. Here (marked 
# with O) is one such path:

# OO.#OOO
# .O#OO#O
# .OOO#OO
# ...#OO#
# ..#OO#.
# .#.O#..
# #.#OOOO

# Simulate the first kilobyte (1024 bytes) falling onto your memory space. 
# Afterward, what is the minimum number of steps needed to reach the exit?


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
    print(np.array2string(m, separator='', 
        formatter={'str_kind': lambda x: x}))

def conv_2d(arr, conv_f):
    return [[conv_f(a) for a in line] for line in arr]


def flatten(xss):
    return [x for xs in xss for x in xs]

def get_neighb(pos, shape):
    h, w = shape
    i,j = pos

    ns = []
    if i > 0:
        ns.append((i-1, j))
    if i < h - 1:
        ns.append((i+1, j))
    if j > 0:
        ns.append((i, j-1))
    if j < w - 1:
        ns.append((i, j+1))

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


def print_path(m, path):
    m2 = m.copy()
    h,w = m.shape
    for p in path:
        m2[p] = 99
    for i in range(h):
        for j in range(w):
            if m2[i,j] > sys.maxsize/100:
                m2[i,j] = -10
    print(m2)

def main():
    inpt = []
    with open('input.txt', 'r') as f_in:
        inpt = f_in.readlines()

        # Remove \n
        inpt = [i[:-1] for i in inpt]

    blocks = [eval(x) for x in inpt]

    # coordinates are reversed
    blocks = [(b,a) for (a,b) in blocks]

    w = 71
    h = 71

    start_pos = (0,0)
    end_pos = (h-1,w-1)
    blockage = -1
    max_dist = sys.maxsize

    mem_space = np.full((h,w), max_dist)
    mem_space[start_pos] = 0

    n_corrupted = 1024

    for i in range(n_corrupted):
        mem_space[blocks[i]] = blockage

    dktr2D(mem_space, start_pos, end_pos=None, blockage=blockage)
    new_path = find_path_from_visited(mem_space, start_pos, end_pos)

    print_path(mem_space, new_path)
    print(new_path)
    print(len(new_path)-1)


if __name__ == '__main__':
    main()