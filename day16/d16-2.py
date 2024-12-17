# --- Day 16: Reindeer Maze ---

# --- Part Two ---

# Now that you know what the best paths look like, you can 
# figure out the best spot to sit.

# Every non-wall tile (S, ., or E) is equipped with places 
# to sit along the edges of the tile. While determining which 
# of these tiles would be the best spot to sit depends on a whole 
# bunch of factors (how comfortable the seats are, how far away 
# the bathrooms are, whether there's a pillar blocking your view, 
# etc.), the most important factor is whether the tile is on one of 
# the best paths through the maze. If you sit somewhere else, 
# you'd miss all the action!

# So, you'll need to determine which tiles are part of any best path 
# through the maze, including the S and E tiles.

# In the first example, there are 45 tiles (marked O) that are part 
# of at least one of the various best paths through the maze:

# ###############
# #.......#....O#
# #.#.###.#.###O#
# #.....#.#...#O#
# #.###.#####.#O#
# #.#.#.......#O#
# #.#.#####.###O#
# #..OOOOOOOOO#O#
# ###O#O#####O#O#
# #OOO#O....#O#O#
# #O#O#O###.#O#O#
# #OOOOO#...#O#O#
# #O###.#.#.#O#O#
# #O..#.....#OOO#
# ###############

# In the second example, there are 64 tiles that are part of at least one of the best paths:

# #################
# #...#...#...#..O#
# #.#.#.#.#.#.#.#O#
# #.#.#.#...#...#O#
# #.#.#.#.###.#.#O#
# #OOO#.#.#.....#O#
# #O#O#.#.#.#####O#
# #O#O..#.#.#OOOOO#
# #O#O#####.#O###O#
# #O#O#..OOOOO#OOO#
# #O#O###O#####O###
# #O#O#OOO#..OOO#.#
# #O#O#O#####O###.#
# #O#O#OOOOOOO..#.#
# #O#O#O#########.#
# #O#OOO..........#
# #################

# Analyze your map further. How many tiles are part of at least 
# one of the best paths through the maze?



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
    # all_dirs_coord = [(1,0),(-1,0),(0,1),(0,-1)]
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

    best_cost = min(all_costs[*end_pos, up], all_costs[*end_pos, right])



    all_map = mmap.copy()
    print_mat(mmap)

    h,w = all_map.shape

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

    for i in range(h):
        for j in range(w):
            if all_map[i,j] == path:
                min_dist = sys.maxsize
                min_path = None
                for d in all_dirs:
                    if all_costs[(i,j,d)] < min_dist:
                        min_dist = all_costs[(i,j,d)]
                        min_path = (i,j,d)
                if min_dist < sys.maxsize:
                    mmap[min_path[0], min_path[1]] = dir_char[min_path[2]]

    print_mat(mmap)

    best_map = all_map.copy()


    def get_best_path(cur_pos, path, cur_cost, expected_cost):
        print(f'cur_pos {cur_pos}')
        if mmap[cur_pos] == end_char:
            print(f'found path: {path + [cur_pos]}')
            return

        for next_pos in maze[cur_pos]:
            # next_pos = move(disp, cur_pos)
            print(f'next: {next_pos}')
            if mmap[next_pos] == wall:
                print(f'wall')
                continue

            new_dir = rev_dir_char[mmap[next_pos]]
            new_cost = cur_cost + all_costs[*next_pos, new_dir]
            print(f'new_cost {new_cost}')
            if new_cost <= expected_cost:
                print(f'will try {next_pos}')
                get_best_path(next_pos, path + [cur_pos], new_cost, expected_cost)

    get_best_path(start_pos, [], 0, best_cost)


if __name__ == '__main__':
    main()