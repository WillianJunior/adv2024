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
    box = 'O'
    wall = '#'
    empty = '.'
    up = '^'
    left = '<'
    down = 'v'
    right = '>'

    i = 0
    while len(inpt[i]) > 0:
        warehouse.append(list(inpt[i]))
        r_x = inpt[i].find(robot)
        if r_x >= 0:
            robot_i, robot_j = (i, r_x)
        i += 1

    while i<len(inpt):
        moves += inpt[i]
        i += 1

    warehouse = np.array(warehouse)
    h,w = warehouse.shape

    moves = np.array(moves)


    print(warehouse)
    print(moves)

    def push_up(i, j):
        if warehouse[i-1, j] == wall:
            # No move was done
            return -1
        elif warehouse[i-1, j] == box:
            # Try to move the box first
            ret = push_up(i-1, j)
            if ret > 0:
                # push box up
                warehouse[i-2,j] = box
                warehouse[i-1,j] = empty

                # Now there is free space
                return 1
            else:
                # Could not make space
                return -1
        else:
            # There is free space to move up
            return 1

    def push_left(i, j):
        if warehouse[i, j-1] == wall:
            # No move was done
            return -1
        elif warehouse[i, j-1] == box:
            # Try to move the box first
            ret = push_left(i, j-1)
            if ret > 0:
                # push box
                warehouse[i,j-2] = box
                warehouse[i,j-1] = empty

                # Now there is free space
                return 1
            else:
                # Could not make space
                return -1
        else:
            # There is free space to move up
            return 1

    def push_down(i, j):
        if warehouse[i+1, j] == wall:
            # No move was done
            return -1
        elif warehouse[i+1, j] == box:
            # Try to move the box first
            ret = push_down(i+1, j)
            if ret > 0:
                # push box
                warehouse[i+2,j] = box
                warehouse[i+1,j] = empty

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
        elif warehouse[i, j+1] == box:
            # Try to move the box first
            ret = push_right(i, j+1)
            if ret > 0:
                # push box up
                warehouse[i,j+2] = box
                warehouse[i,j+1] = empty

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
            if push_up(robot_i, robot_j) > 0:
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
            if push_down(robot_i, robot_j) > 0:
                warehouse[robot_i, robot_j] = empty
                warehouse[robot_i+1, robot_j] = robot
                robot_i += 1
        else:
            0/0

        print(warehouse)

    summ = 0
    for i in range(h):
        for j in range(w):
            if warehouse[i,j] == box:
                summ += 100*i + j

    print(summ)



if __name__ == '__main__':
    main()