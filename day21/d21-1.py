# --- Day 21: Keypad Conundrum ---

# As you teleport onto Santa's Reindeer-class starship, The Historians
# begin to panic: someone from their search party is missing. A quick
# life-form scan by the ship's computer reveals that when the missing
# Historian teleported, he arrived in another part of the ship.

# The door to that area is locked, but the computer can't open it; it
# can only be opened by physically typing the door codes (your puzzle
# input) on the numeric keypad on the door.

# The numeric keypad has four rows of buttons: 789, 456, 123, and
# finally an empty gap followed by 0A. Visually, they are arranged
# like this:

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

# Unfortunately, the area outside the door is currently depressurized
# and nobody can go near the door. A robot needs to be sent instead.

# The robot has no problem navigating the ship and finding the numeric
# keypad, but it's not designed for button pushing: it can't be told to
# push a specific button directly. Instead, it has a robotic arm that
# can be controlled remotely via a directional keypad.

# The directional keypad has two rows of buttons: a gap / ^ (up) / A
# (activate) on the first row and < (left) / v (down) / > (right) on the
# second row. Visually, they are arranged like this:

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

# When the robot arrives at the numeric keypad, its robotic arm is
# pointed at the A button in the bottom right corner. After that, this
# directional keypad remote control must be used to maneuver the robotic
# arm: the up / down / left / right buttons cause it to move its arm
# one button in that direction, and the A button causes the robot to
# briefly move forward, pressing the button being aimed at by the robotic
# arm.

# For example, to make the robot type 029A on the numeric keypad, one
# sequence of inputs on the directional keypad you could use is:

#     < to move the arm from A (its initial position) to 0.
#     A to push the 0 button.
#     ^A to move the arm to the 2 button and push it.
#     >^^A to move the arm to the 9 button and push it.
#     vvvA to move the arm to the A button and push it.

# In total, there are three shortest possible sequences of button presses
# on this directional keypad that would cause the robot to type
# 029A: <A^A>^^AvvvA, <A^A^>^AvvvA, and <A^A^^>AvvvA.

# Unfortunately, the area containing this directional keypad remote control
# is currently experiencing high levels of radiation and nobody can go near
# it. A robot needs to be sent instead.

# When the robot arrives at the directional keypad, its robot arm is
# pointed at the A button in the upper right corner. After that, a second,
# different directional keypad remote control is used to control this
# robot (in the same way as the first robot, except that this one is typing
# on a directional keypad instead of a numeric keypad).

# There are multiple shortest possible sequences of directional keypad
# button presses that would cause this robot to tell the first robot to
# type 029A on the door. One such sequence is v<<A>>^A<A>AvA<^AA>A<vAAA>^A.

# Unfortunately, the area containing this second directional keypad remote
# control is currently -40 degrees! Another robot will need to be sent to
# type on that directional keypad, too.

# There are many shortest possible sequences of directional keypad button
# presses that would cause this robot to tell the second robot to tell the
# first robot to eventually type 029A on the door. One such sequence
# is <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A.

# Unfortunately, the area containing this third directional keypad remote
# control is currently full of Historians, so no robots can find a clear
# path there. Instead, you will have to type this sequence yourself.

# Were you to choose this sequence of button presses, here are all of the
# buttons that would be pressed on your directional keypad, the two robots'
# directional keypads, and the numeric keypad:

# <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
# v<<A>>^A<A>AvA<^AA>A<vAAA>^A
# <A^A>^^AvvvA
# 029A

# In summary, there are the following keypads:

#     One directional keypad that you are using.
#     Two directional keypads that robots are using.
#     One numeric keypad (on a door) that a robot is using.

# It is important to remember that these robots are not designed for button
# pushing. In particular, if a robot arm is ever aimed at a gap where no
# button is present on the keypad, even for an instant, the robot will
# panic unrecoverably. So, don't do that. All robots will initially aim
# at the keypad's A key, wherever it is.

# To unlock the door, five codes will need to be typed on its numeric keypad.
# For example:

# 029A
# 980A
# 179A
# 456A
# 379A

# For each of these, here is a shortest sequence of button presses you could
# type to cause the desired code to be typed on the numeric keypad:

# 029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
# 980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
# 179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
# 456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
# 379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A

# The Historians are getting nervous; the ship computer doesn't remember
# whether the missing Historian is trapped in the area containing a giant
# electromagnet or molten lava. You'll need to make sure that for each of
# the five codes, you find the shortest sequence of button presses necessary.

# The complexity of a single code (like 029A) is equal to the result of
# multiplying these two values:

#     The length of the shortest sequence of button presses you need to type
#         on your directional keypad in order to cause the code to be typed on
#         the numeric keypad; for 029A, this would be 68.
#     The numeric part of the code (ignoring leading zeroes); for 029A, this
#         would be 29.

# In the above example, complexity of the five codes can be found by
# calculating 68 * 29, 60 * 980, 68 * 179, 64 * 456, and 64 * 379. Adding
# these together produces 126384.

# Find the fewest number of button presses you'll need to perform in order
# to cause the robot in front of the door to type each code. What is the sum
# of the complexities of the five codes on your list?

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

A_key = 'A'
bad_key = 'X'
up = '^'
down = 'v'
left = '<'
right = '>'

numpad_pos = {
    '7': (0, 0),
    '8': (0, 1),
    '9': (0, 2),
    '4': (1, 0),
    '5': (1, 1),
    '6': (1, 2),
    '1': (2, 0),
    '2': (2, 1),
    '3': (2, 2),
    bad_key: (3, 0),
    '0': (3, 1),
    A_key: (3, 2),
}

arrowpad_pos = {
    bad_key: (0, 0),
    up: (0, 1),
    A_key: (0, 2),
    left: (1, 0),
    down: (1, 1),
    right: (1, 2),
}

# 0  2  9    A
# <A ^A >^^A vvvA

# 3->7
# ^^<<A
# <<^^A


def manh_dist(ini, end):
    max_x = max(ini[0], end[0])
    min_x = min(ini[0], end[0])
    max_y = max(ini[1], end[1])
    min_y = min(ini[1], end[1])
    return (max_x - min_x) + (max_y - min_y)


def get_press_moves(next_code, keypad, cur_pos, next_keypad,
                    next_keypad_cur_pos):
    # print(f'from {cur_pos} to {keypad[next_code]}')
    cur_i, cur_j = cur_pos
    next_pos = keypad[next_code]
    next_i, next_j = next_pos

    # Find required moves
    unordered_next_moves = []
    vert_mov = next_i - cur_i
    horz_mov = next_j - cur_j

    # Do all vert moves
    if vert_mov < 0:
        unordered_next_moves += (-vert_mov) * [up]
    elif vert_mov > 0:
        unordered_next_moves += vert_mov * [down]

    # Do all horz moves
    if horz_mov > 0:
        unordered_next_moves += horz_mov * [right]
    elif horz_mov < 0:
        unordered_next_moves += (-horz_mov) * [left]

    next_moves = []
    while len(unordered_next_moves) > 0:
        # print(f'    unordered_next_moves: {unordered_next_moves}')
        best_dist = 9999
        best_move = None
        for m in unordered_next_moves:
            # Check if going into bad position
            pass  # TODO, if wrong result

            dist = manh_dist(next_keypad_cur_pos, next_keypad[m])
            if dist < best_dist:
                best_dist = dist
                best_move = m

        # Add next move in order
        unordered_next_moves.remove(best_move)
        next_moves.append(best_move)
        # cur_pos = best_move

    # return next_moves, cur_pos
    return next_moves + [A_key]


def get_moves(code, keypad, next_keypad, init_keypad_pos,
              init_next_keypad_pos):
    moves = []
    for c in code:
        new_moves = get_press_moves(c, keypad, init_keypad_pos, next_keypad,
                                    init_next_keypad_pos)
        init_keypad_pos = keypad[c]

        moves += new_moves

    return moves


def main():
    inpt = []
    with open('input.txt', 'r') as f_in:
        inpt = f_in.readlines()

        # Remove \n
        inpt = [i[:-1] for i in inpt]

    ssum = 0
    for code in inpt:
        moves = []
        # code = '379A'
        print(code)
        init_keypad_pos = numpad_pos[A_key]
        init_arrowpad_pos = arrowpad_pos[A_key]

        moves1 = get_moves(code, numpad_pos, arrowpad_pos, init_keypad_pos,
                           init_arrowpad_pos)
        print(''.join(moves1))

        moves2 = get_moves(moves1, arrowpad_pos, arrowpad_pos,
                           init_arrowpad_pos, init_arrowpad_pos)
        print(''.join(moves2))

        moves3 = get_moves(moves2, arrowpad_pos, arrowpad_pos,
                           init_arrowpad_pos, init_arrowpad_pos)
        print(''.join(moves3))

        print(len(moves3), int(code[:-1]))
        print(len(moves3) * int(code[:-1]))
        ssum += len(moves3) * int(code[:-1])

    print(ssum)

    # 121280 too low


if __name__ == '__main__':
    main()