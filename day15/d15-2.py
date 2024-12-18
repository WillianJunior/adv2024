# --- Day 15: Warehouse Woes ---

# --- Part Two ---

# The lanternfish use your information to find a safe moment to swim in and 
# turn off the malfunctioning robot! Just as they start preparing a festival 
# in your honor, reports start coming in that a second warehouse's robot is 
# also malfunctioning.

# This warehouse's layout is surprisingly similar to the one you just helped. 
# There is one key difference: everything except the robot is twice as wide! 
# The robot's list of movements doesn't change.

# To get the wider warehouse's map, start with your original map and, for each 
# tile, make the following changes:

#     If the tile is #, the new map contains ## instead.
#     If the tile is O, the new map contains [] instead.
#     If the tile is ., the new map contains .. instead.
#     If the tile is @, the new map contains @. instead.

# This will produce a new warehouse map which is twice as wide and with wide 
# boxes that are represented by []. (The robot does not change size.)

# The larger example from before would now look like this:

# ####################
# ##....[]....[]..[]##
# ##............[]..##
# ##..[][]....[]..[]##
# ##....[]@.....[]..##
# ##[]##....[]......##
# ##[]....[]....[]..##
# ##..[][]..[]..[][]##
# ##........[]......##
# ####################

# Because boxes are now twice as wide but the robot is still the same size 
# and speed, boxes can be aligned such that they directly push two other 
# boxes at once. For example, consider this situation:

# #######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######

# <vv<<^^<<^^

# After appropriately resizing this map, the robot would push around these 
# boxes as follows:

# Initial state:
# ##############
# ##......##..##
# ##..........##
# ##....[][]@.##
# ##....[]....##
# ##..........##
# ##############

# Move <:
# ##############
# ##......##..##
# ##..........##
# ##...[][]@..##
# ##....[]....##
# ##..........##
# ##############

# Move v:
# ##############
# ##......##..##
# ##..........##
# ##...[][]...##
# ##....[].@..##
# ##..........##
# ##############

# Move v:
# ##############
# ##......##..##
# ##..........##
# ##...[][]...##
# ##....[]....##
# ##.......@..##
# ##############

# Move <:
# ##############
# ##......##..##
# ##..........##
# ##...[][]...##
# ##....[]....##
# ##......@...##
# ##############

# Move <:
# ##############
# ##......##..##
# ##..........##
# ##...[][]...##
# ##....[]....##
# ##.....@....##
# ##############

# Move ^:
# ##############
# ##......##..##
# ##...[][]...##
# ##....[]....##
# ##.....@....##
# ##..........##
# ##############

# Move ^:
# ##############
# ##......##..##
# ##...[][]...##
# ##....[]....##
# ##.....@....##
# ##..........##
# ##############

# Move <:
# ##############
# ##......##..##
# ##...[][]...##
# ##....[]....##
# ##....@.....##
# ##..........##
# ##############

# Move <:
# ##############
# ##......##..##
# ##...[][]...##
# ##....[]....##
# ##...@......##
# ##..........##
# ##############

# Move ^:
# ##############
# ##......##..##
# ##...[][]...##
# ##...@[]....##
# ##..........##
# ##..........##
# ##############

# Move ^:
# ##############
# ##...[].##..##
# ##...@.[]...##
# ##....[]....##
# ##..........##
# ##..........##
# ##############

# This warehouse also uses GPS to locate the boxes. For these larger boxes, 
# distances are measured from the edge of the map to the closest edge of the 
# box in question. So, the box shown below has a distance of 1 from the top 
# edge of the map and 5 from the left edge of the map, resulting in a GPS 
# coordinate of 100 * 1 + 5 = 105.

# ##########
# ##...[]...
# ##........

# In the scaled-up version of the larger example from above, after the robot 
# has finished all of its moves, the warehouse would look like this:

# ####################
# ##[].......[].[][]##
# ##[]...........[].##
# ##[]........[][][]##
# ##[]......[]....[]##
# ##..##......[]....##
# ##..[]............##
# ##..@......[].[][]##
# ##......[][]..[]..##
# ####################

# The sum of these boxes' GPS coordinates is 9021.

# Predict the motion of the robot and boxes in this new, scaled-up warehouse. 
# What is the sum of all boxes' final GPS coordinates?


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

    warehouse = []
    moves = []
    robot_i = None
    robot_j = None

    robot = '@'
    new_robot = '@.'
    old_box = 'O'
    box = '[]'
    wall = '#'
    new_wall = '##'
    empty = '.'
    new_empty = '..'
    up = '^'
    left = '<'
    down = 'v'
    right = '>'

    i = 0
    while len(inpt[i]) > 0:
        new_line = str(inpt[i]).replace(old_box, box)
        new_line = new_line.replace(wall, new_wall)
        new_line = new_line .replace(empty, new_empty)
        new_line = new_line.replace(robot, new_robot)

        warehouse.append(list(new_line))

        r_x = new_line.find(robot)
        if r_x >= 0:
            robot_i, robot_j = (i, r_x)
        i += 1

    while i<len(inpt):
        moves += inpt[i]
        i += 1

    warehouse = np.array(warehouse)
    h,w = warehouse.shape

    moves = np.array(moves)

    it = 0
    def print_warehouse(it, warehouse=warehouse):
        print(it)
        print(np.array2string(warehouse, separator='', formatter={'str_kind': lambda x: x}))

    # print(moves)
    # print_warehouse(-1)

    def push_up(warehouse, i, j,l=0):
        cond = False
        if cond: print(f'{l*'   '} pushing {i,j}')
        if warehouse[i,j] == robot:
            if warehouse[i-1,j] == empty:
                if cond: print(f'{l*'   '} robot empty')
                return warehouse
            elif warehouse[i-1,j] == wall:
                if cond: print(f'{l*'   '} robot wall')
                return None
            else:
                if warehouse[i-1,j] == box[0]:
                    w1 = push_up(warehouse, i-1, j, l+1)
                elif warehouse[i-1,j] == box[1]:
                    w1 = push_up(warehouse, i-1, j-1, l+1)

                if cond: print(f'{l*'   '} robot can push')
                return w1

        # Now i,j is a box with '[' in i,j

        if warehouse[i-1,j] == wall or warehouse[i-1,j+1] == wall:
            # There is at least 1 wall blocking the move
            if cond: print(f'{l*'   '} wall above box {i,j}')
            return None

        if warehouse[i-1,j] == empty and warehouse[i-1,j+1] == empty:
            # trivial case with 2 empty spaces above
            if cond: print(f'{l*'   '} all empty above box {i,j}')
            warehouse[i-1,j] = box[0]
            warehouse[i-1,j+1] = box[1]
            warehouse[i,j] = empty
            warehouse[i,j+1] = empty
            # print_warehouse(it, warehouse)

            return warehouse

        if warehouse[i-1,j] == box[0]:
            # Trivial case of aligned boxes: push above first,
            # and if ok, push current
            if cond: print(f'{l*'   '} aligned box above {i,j}')
            warehouse = push_up(warehouse, i-1, j, l+1)
            if warehouse is not None:
                warehouse[i-1,j] = box[0]
                warehouse[i-1,j+1] = box[1]
                warehouse[i,j] = empty
                warehouse[i,j+1] = empty
            return warehouse

        # Now, i,j have a misaligned box in the way

        if warehouse[i-1,j] == box[1]:
            # left case
            if cond: print(f'{l*'   '} misaligned left above box {i,j}')
            warehouse = push_up(warehouse, i-1, j-1, l+1)
            if warehouse is None:
                # print('--------')
                return warehouse
            
        if warehouse[i-1,j+1] == box[0]:
            # right case
            if cond: print(f'{l*'   '} misaligned right above box {i,j}')
            warehouse = push_up(warehouse, i-1, j+1, l+1)
            if warehouse is None:
                return warehouse
        
        if warehouse is not None:        
            warehouse[i-1,j] = box[0]
            warehouse[i-1,j+1] = box[1]
            warehouse[i,j] = empty
            warehouse[i,j+1] = empty

        return warehouse

    def push_down(warehouse, i, j,l=0):
        cond = False
        if cond: print(f'{l*'   '} pushing {i,j}')
        if warehouse[i,j] == robot:
            if warehouse[i+1,j] == empty:
                if cond: print(f'{l*'   '} robot empty')
                return warehouse
            elif warehouse[i+1,j] == wall:
                if cond: print(f'{l*'   '} robot wall')
                return None
            else:
                if warehouse[i+1,j] == box[0]:
                    w1 = push_down(warehouse, i+1, j, l+1)
                elif warehouse[i+1,j] == box[1]:
                    w1 = push_down(warehouse, i+1, j-1, l+1)

                if cond: print(f'{l*'   '} robot can push')
                return w1

        # Now i,j is a box with '[' in i,j

        if warehouse[i+1,j] == wall or warehouse[i+1,j+1] == wall:
            # There is at least 1 wall blocking the move
            if cond: print(f'{l*'   '} wall above box {i,j}')
            return None

        if warehouse[i+1,j] == empty and warehouse[i+1,j+1] == empty:
            # trivial case with 2 empty spaces above
            if cond: print(f'{l*'   '} all empty above box {i,j}')
            warehouse[i+1,j] = box[0]
            warehouse[i+1,j+1] = box[1]
            warehouse[i,j] = empty
            warehouse[i,j+1] = empty
            # print_warehouse(it, warehouse)

            return warehouse

        if warehouse[i+1,j] == box[0]:
            # Trivial case of aligned boxes: push above first,
            # and if ok, push current
            if cond: print(f'{l*'   '} aligned box above {i,j}')
            warehouse = push_down(warehouse, i+1, j, l+1)
            if warehouse is not None:
                warehouse[i+1,j] = box[0]
                warehouse[i+1,j+1] = box[1]
                warehouse[i,j] = empty
                warehouse[i,j+1] = empty
            return warehouse

        # Now, i,j have a misaligned box in the way

        if warehouse[i+1,j] == box[1]:
            # left case
            if cond: print(f'{l*'   '} misaligned left above box {i,j}')
            warehouse = push_down(warehouse, i+1, j-1, l+1)
            if warehouse is None:
                # print('--------')
                return warehouse
            
        if warehouse[i+1,j+1] == box[0]:
            # right case
            if cond: print(f'{l*'   '} misaligned right above box {i,j}')
            warehouse = push_down(warehouse, i+1, j+1, l+1)
            if warehouse is None:
                return warehouse
        
        if warehouse is not None:        
            warehouse[i+1,j] = box[0]
            warehouse[i+1,j+1] = box[1]
            warehouse[i,j] = empty
            warehouse[i,j+1] = empty

        return warehouse

    def push_left(i, j):
        if warehouse[i, j-1] == wall:
            # No move was done
            return -1
        elif warehouse[i, j-1] in box:
            # Try to move the box first
            ret = push_left(i, j-2)
            if ret > 0:
                # push box
                warehouse[i,j-3] = box[0]
                warehouse[i,j-2] = box[1]
                warehouse[i,j-1:j+1] = empty

                # Now there is free space
                return 1
            else:
                # Could not make space
                return -1
        else:
            # There is free space to move up
            return 1


    def push_right(i, j):
        if warehouse[i, j+1] == wall:
            # No move was done
            return -1
        elif warehouse[i, j+1] in box:
            # Try to move the box first
            ret = push_right(i, j+2)
            if ret > 0:
                # push box
                warehouse[i,j+2] = box[0]
                warehouse[i,j+3] = box[1]
                warehouse[i,j:j+2] = empty

                # Now there is free space
                return 1
            else:
                # Could not make space
                return -1
        else:
            # There is free space to move up
            return 1

    for m in moves:
        # print(f'move: {m}')
        if m == up:
            w_new = push_up(warehouse.copy(), robot_i, robot_j)
            if w_new is not None:
                warehouse = w_new
                warehouse[robot_i, robot_j] = empty
                warehouse[robot_i-1, robot_j] = robot
                robot_i -= 1

        elif m == left:
            if push_left(robot_i, robot_j) > 0:
                warehouse[robot_i, robot_j] = empty
                warehouse[robot_i, robot_j-1] = robot
                robot_j -= 1
        elif m == right:
            if push_right(robot_i, robot_j) > 0:
                warehouse[robot_i, robot_j] = empty
                warehouse[robot_i, robot_j+1] = robot
                robot_j += 1
        elif m == down:
            w_new =  push_down(warehouse.copy(),robot_i, robot_j)
            if w_new is not None:
                warehouse = w_new
                warehouse[robot_i, robot_j] = empty
                warehouse[robot_i+1, robot_j] = robot
                robot_i += 1

        else:
            0/0

        # print(warehouse)
        # print_warehouse(it, warehouse)
        it += 1
        # input()
        # if it > 309:
        #     return

    summ = 0
    for i in range(h):
        for j in range(w):
            if warehouse[i,j] == box[0]:
                summ += 100*i + j

    # print_warehouse(it, warehouse)
    print(summ)


if __name__ == '__main__':
    main()