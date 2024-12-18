# --- Day 15: Warehouse Woes ---

# You appear back inside your own mini submarine! Each Historian drives 
# their mini submarine in a different direction; maybe the Chief has his 
# own submarine down here somewhere as well?

# You look up to see a vast school of lanternfish swimming past you. 
# On closer inspection, they seem quite anxious, so you drive your mini 
# submarine over to see if you can help.

# Because lanternfish populations grow rapidly, they need a lot of food, 
# and that food needs to be stored somewhere. That's why these lanternfish 
# have built elaborate warehouse complexes operated by robots!

# These lanternfish seem so anxious because they have lost control of the 
# robot that operates one of their most important warehouses! It is currently
#  running amok, pushing around boxes in the warehouse with no regard for 
#  lanternfish logistics or lanternfish inventory management strategies.

# Right now, none of the lanternfish are brave enough to swim up to an 
# unpredictable robot so they could shut it off. However, if you could 
# anticipate the robot's movements, maybe they could find a safe option.

# The lanternfish already have a map of the warehouse and a list of 
# movements the robot will attempt to make (your puzzle input). The 
# problem is that the movements will sometimes fail as boxes are shifted 
# around, making the actual movements of the robot difficult to predict.

# For example:

# ##########
# #..O..O.O#
# #......O.#
# #.OO..O.O#
# #..O@..O.#
# #O#..O...#
# #O..O..O.#
# #.OO.O.OO#
# #....O...#
# ##########

# <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
# vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
# ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
# <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
# ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
# ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
# >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
# <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
# ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
# v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^

# As the robot (@) attempts to move, if there are any boxes (O) in the 
# way, the robot will also attempt to push those boxes. However, if this 
# action would cause the robot or a box to move into a wall (#), nothing 
# moves instead, including the robot. The initial positions of these 
# are shown on the map at the top of the document the lanternfish gave you.

# The rest of the document describes the moves (^ for up, v for down, < for 
# left, > for right) that the robot will attempt to make, in order. (The 
# moves form a single giant sequence; they are broken into multiple lines 
# just to make copy-pasting easier. Newlines within the move sequence 
# should be ignored.)

# Here is a smaller example to get started:

# ########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########

# <^^>>>vv<v>>v<<

# Were the robot to attempt the given sequence of moves, it would 
# push around the boxes as follows:

# Initial state:
# ########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########

# Move <:
# ########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########

# Move ^:
# ########
# #.@O.O.#
# ##..O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########

# Move ^:
# ########
# #.@O.O.#
# ##..O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########

# Move >:
# ########
# #..@OO.#
# ##..O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########

# Move >:
# ########
# #...@OO#
# ##..O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########

# Move >:
# ########
# #...@OO#
# ##..O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########

# Move v:
# ########
# #....OO#
# ##..@..#
# #...O..#
# #.#.O..#
# #...O..#
# #...O..#
# ########

# Move v:
# ########
# #....OO#
# ##..@..#
# #...O..#
# #.#.O..#
# #...O..#
# #...O..#
# ########

# Move <:
# ########
# #....OO#
# ##.@...#
# #...O..#
# #.#.O..#
# #...O..#
# #...O..#
# ########

# Move v:
# ########
# #....OO#
# ##.....#
# #..@O..#
# #.#.O..#
# #...O..#
# #...O..#
# ########

# Move >:
# ########
# #....OO#
# ##.....#
# #...@O.#
# #.#.O..#
# #...O..#
# #...O..#
# ########

# Move >:
# ########
# #....OO#
# ##.....#
# #....@O#
# #.#.O..#
# #...O..#
# #...O..#
# ########

# Move v:
# ########
# #....OO#
# ##.....#
# #.....O#
# #.#.O@.#
# #...O..#
# #...O..#
# ########

# Move <:
# ########
# #....OO#
# ##.....#
# #.....O#
# #.#O@..#
# #...O..#
# #...O..#
# ########

# Move <:
# ########
# #....OO#
# ##.....#
# #.....O#
# #.#O@..#
# #...O..#
# #...O..#
# ########

# The larger example has many more moves; after the robot has finished those 
# moves, the warehouse would look like this:

# ##########
# #.O.O.OOO#
# #........#
# #OO......#
# #OO@.....#
# #O#.....O#
# #O.....OO#
# #O.....OO#
# #OO....OO#
# ##########

# The lanternfish use their own custom Goods Positioning System (GPS for 
#     short) to track the locations of the boxes. The GPS coordinate of a box 
# is equal to 100 times its distance from the top edge of the map plus its 
# distance from the left edge of the map. (This process does not stop at wall 
#     tiles; measure all the way to the edges of the map.)

# So, the box shown below has a distance of 1 from the top edge of the map and
# 4 from the left edge of the map, resulting in a GPS coordinate of 
# 100 * 1 + 4 = 104.

# #######
# #...O..
# #......

# The lanternfish would like to know the sum of all boxes' GPS coordinates 
# after the robot finishes moving. In the larger example, the sum of all boxes' 
# GPS coordinates is 10092. In the smaller example, the sum is 2028.

# Predict the motion of the robot and boxes in the warehouse. After the robot is 
# finished moving, what is the sum of all boxes' GPS coordinates?

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
    def print_warehouse(it):
        print(it)
        print(np.array2string(warehouse, separator='', formatter={'str_kind': lambda x: x}))

    # print(warehouse)
    print(moves)
    print_warehouse(-1)

    def can_push_up(i, j, l=0):
        cond = it >= 32
        if cond: print(f'{l*'  '}testing {i,j}')
        if warehouse[i,j] == robot and warehouse[i-1,j] == empty:
            return 1
        if warehouse[i,j] == empty:
            return 1

        box_left_case = warehouse[i,j] == box[0] and (
            (warehouse[i-1,j] == wall) or 
            (warehouse[i-1, j+1] == wall))
        box_right_case = warehouse[i,j] == box[1] and (
            (warehouse[i-1,j] == wall) or 
            (warehouse[i-1, j-1] == wall))

        if box_left_case or box_right_case or warehouse[i-1,j] == wall:
            # No move can be done
            if cond: print(f'{l*'  '}cant move up at {i,j}')
            return -1
        elif warehouse[i-1, j] in box or warehouse[i-1, j-1] in box or warehouse[i-1, j+1] in box:
            # Try to move the box first
            if cond: print(f'{l*'  '}need to test {i-1,j} before')
            ret1 = can_push_up(i-1, j, l+1)
            if warehouse[i-1,j] == box[0]:
                if cond: print(f'{l*'  '}also need to test {i-1,j+1} before')
                if warehouse[i-1,j] == warehouse[i,j]:
                    ret2 = ret1
                else:
                    ret2 = can_push_up(i-1, j+1, l+1)
            else:
                if cond: print(f'{l*'  '}also need to test {i-1,j-1} before')
                if warehouse[i-1,j] == warehouse[i,j]:
                    ret2 = ret1
                else:
                    ret2 = can_push_up(i-1, j-1, l+1)

            if ret1 > 0 and ret2 > 0:
                if cond: print(f'{l*'  '}allowed at {i,j}')
                # There is free space
                return 1
            else:
                # Could not make space
                if cond: print(f'{l*'  '}not allowed {i,j}')
                return -1
        else:
            # There is free space to move up
            if cond: print(f'{l*'  '}is free at {i,j}')
            return 1

    def push_up(i, j,l=0):
        if warehouse[i,j] == robot and warehouse[i-1,j] == empty:
            return 1

        if warehouse[i,j] == empty:
            return 1

        # print(f'{l*'---'} pushing at{i,j}')
        box_left_case = warehouse[i,j] == box[0] and (
            (warehouse[i-1,j] == wall) or 
            (warehouse[i-1, j+1] == wall))
        box_right_case = warehouse[i,j] == box[1] and (
            (warehouse[i-1,j] == wall) or 
            (warehouse[i-1, j-1] == wall))

        if box_left_case or box_right_case:
            # No move can be done
            # print(f'{l*'  '}found wall....')
            return -1
        elif warehouse[i-1, j] in box:
            # Try to move the box first
            # print(f'{l*'  '}need to move {i-1,j} first')
            ret1 = push_up(i-1, j, l+1)
            if warehouse[i-1,j] == box[0]:
                # print(f'{l*'  '}+check left')
                ret2 = push_up(i-1, j+1, l+1)
            else:
                # print(f'{l*'  '}+check right')
                ret2 = push_up(i-1, j-1, l+1)

            if ret1 > 0 and ret2 > 0:
                # push box up
                # print(f'{l*'  '} can push {i-1,j} up now')
                
                # print({i-1,j})
                # print(warehouse[i-1])
                # print(f'cmp: {warehouse[i-1,j]}')
                if warehouse[i-1,j] == box[0]:
                    warehouse[i-2,j] = box[0]
                    warehouse[i-2,j+1] = box[1]
                    warehouse[i-1,j+1] = empty
                else:
                    warehouse[i-2,j] = box[1]
                    warehouse[i-2,j-1] = box[0]
                    warehouse[i-1,j-1] = empty

                warehouse[i-1,j] = empty
                # print(i,j)
                # print(warehouse)

                # Now there is free space
                # print(f'{l*'  '} new free space')
                return 1
            else:
                # Could not make space
                # print(f'{l*'  '} no space')
                return -1
        else:
            # There is free space to move up
            # print(f'{l*'  '} free space')
            return 1

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

    def can_push_down(i, j, l=0):
        if warehouse[i,j] == robot and warehouse[i+1,j] == empty:
            return 1

        if warehouse[i,j] == empty:
            return 1

        box_left_case = warehouse[i,j] == box[0] and (
            (warehouse[i+1,j] == wall) or 
            (warehouse[i+1, j+1] == wall))
        box_right_case = warehouse[i,j] == box[1] and (
            (warehouse[i+1,j] == wall) or 
            (warehouse[i+1, j-1] == wall))

        if box_left_case or box_right_case or warehouse[i+1,j] == wall:
            # No move can be done
            return -1
        elif warehouse[i+1, j] in box or warehouse[i+1, j-1] in box or warehouse[i+1, j+1] in box:
            # Try to move the box first
            ret1 = can_push_down(i+1, j, l+1)
            if warehouse[i+1,j] == empty:
                if warehouse[i,j] == box[0]:
                    ret2 = can_push_down(i+1, j+1, l+1)
                else:
                    ret2 = can_push_down(i+1, j-1, l+1)

            elif warehouse[i+1,j] == box[0]:
                # if it > 93: print(f'{l*'  '}also need to test {i-1,j+1} before')
                if warehouse[i+1,j] == warehouse[i,j]:
                    ret2 = ret1
                else:
                    ret2 = can_push_down(i+1, j+1, l+1)
            elif warehouse[i+1,j]:
                # if it > 93: print(f'{l*'  '}also need to test {i-1,j-1} before')
                if warehouse[i-1,j] == warehouse[i,j]:
                    ret2 = ret1
                else:
                    ret2 = can_push_down(i+1, j-1, l+1)

            if ret1 > 0 and ret2 > 0:
                # There is free space
                return 1
            else:
                # Could not make space
                return -1
        else:
            # There is free space to move up
            return 1

    def push_down(i, j,l=0):
        cond = it >= 309
        
        if warehouse[i,j] == robot and warehouse[i+1,j] == empty:
            if cond: print(f'{l*'---'} robot pushing empty at {i,j}')
            return 1

        if warehouse[i,j] == empty:
            if cond: print(f'{l*'---'} pushing empty at {i,j}')
            return 1

        if cond: print(f'{l*'---'} pushing at{i,j}')
        box_left_case = warehouse[i,j] == box[0] and (
            (warehouse[i+1,j] == wall) or 
            (warehouse[i+1, j+1] == wall))
        box_right_case = warehouse[i,j] == box[1] and (
            (warehouse[i+1,j] == wall) or 
            (warehouse[i+1, j-1] == wall))

        if box_left_case or box_right_case:
            # No move can be done
            if cond: print(f'{l*'  '}found wall....')
            return -1
        elif warehouse[i+1, j] in box or warehouse[i+1, j-1] in box or warehouse[i+1, j+1] in box:
            # Try to move the box first
            print(f'{l*'  '}need to move {i+1,j} first')
            ret1 = push_down(i+1, j, l+1)

            if warehouse[i+1,j] == empty:
                if warehouse[i,j] == box[0]:
                    ret2 = push_down(i+1, j+1, l+1)
                else:
                    ret2 = push_down(i+1, j-1, l+1)

            elif warehouse[i+1,j] == box[0]:
                print(f'{l*'  '}+check left')
                ret2 = push_down(i+1, j+1, l+1)
            else:
                print(f'{l*'  '}+check right')
                ret2 = push_down(i+1, j-1, l+1)

            if ret1 > 0 and ret2 > 0:
                # push box up
                print(f'{l*'  '} can push {i+1,j} down now')
                
                # print({i-1,j})
                # print(warehouse[i+1])
                # print(f'cmp: {warehouse[i+1,j]}')
                if warehouse[i+1,j] == box[0]:
                    warehouse[i+2,j] = box[0]
                    warehouse[i+2,j+1] = box[1]
                    warehouse[i+1,j+1] = empty
                else:
                    warehouse[i+2,j] = box[1]
                    warehouse[i+2,j-1] = box[0]
                    warehouse[i+1,j-1] = empty

                warehouse[i+1,j] = empty
                # print(i,j)
                # print(warehouse)
                print_warehouse(it)

                # Now there is free space
                print(f'{l*'  '} new free space')
                return 1
            else:
                # Could not make space
                print(f'{l*'  '} no space')
                return -1
        else:
            # There is free space to move up
            # print(f'{l*'  '} free space')
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
        print(f'move: {m}')
        if m == up:
            if can_push_up(robot_i, robot_j) > 0:
                print(f'robot {robot_i,robot_j} can push up ')
                push_up(robot_i, robot_j)
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
            if can_push_down(robot_i, robot_j) > 0:
                push_down(robot_i, robot_j)
                warehouse[robot_i, robot_j] = empty
                warehouse[robot_i+1, robot_j] = robot
                robot_i += 1

        else:
            0/0

        # print(warehouse)
        print_warehouse(it)
        it += 1
        # input()
        if it > 309:
            return

    summ = 0
    count = 0
    ww = 0
    for i in range(h):
        for j in range(w):
            if warehouse[i,j] == box[0]:
                summ += 100*i + j
                count += 1
            if warehouse[i,j] == wall:
                ww += 1

    print(summ)
    print(count)
    print(ww)



if __name__ == '__main__':
    main()