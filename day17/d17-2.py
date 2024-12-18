# --- Part Two ---

# The Historians aren't as used to moving around in this pixelated 
# universe as you are. You're afraid they're not going to be fast 
# enough to make it to the exit before the path is completely blocked.

# To determine how fast everyone needs to go, you need to determine 
# the first byte that will cut off the path to the exit.

# In the above example, after the byte at 1,1 falls, there is still 
# a path to the exit:

# O..#OOO
# O##OO#O
# O#OO#OO
# OOO#OO#
# ###OO##
# .##O###
# #.#OOOO

# However, after adding the very next byte (at 6,1), there is no 
# longer a path to the exit:

# ...#...
# .##..##
# .#..#..
# ...#..#
# ###..##
# .##.###
# #.#....

# So, in this example, the coordinates of the first byte that prevents 
# the exit from being reachable are 6,1.

# Simulate more of the bytes that are about to corrupt your memory space. 
# What are the coordinates of the first byte that will prevent the exit 
# from being reachable from your starting position? (Provide the answer 
# as two integers separated by a comma with no other characters.)


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

    n_corrupted = 0
    path = [0]

    while len(path) > 0:
        n_corrupted += 1
        mem_space = np.full((h,w), max_dist)
        mem_space[start_pos] = 0

        print(n_corrupted)
        for i in range(n_corrupted):
            mem_space[blocks[i]] = blockage
        
        dktr2D(mem_space, start_pos, end_pos=None, blockage=blockage)
        path = find_path_from_visited(mem_space, start_pos, end_pos)

        print(blocks[n_corrupted-1])


if __name__ == '__main__':
    main()