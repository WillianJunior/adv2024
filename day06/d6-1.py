# --- Day 6: Guard Gallivant ---

# The Historians use their fancy device again, this time to whisk you
# all away to the North Pole prototype suit manufacturing lab... in the
# year 1518! It turns out that having direct access to history is very
# convenient for a group of historians.

# You still have to be careful of time paradoxes, and so it will be
# important to avoid anyone from 1518 while The Historians search
# for the Chief. Unfortunately, a single guard is patrolling this part
# of the lab.

# Maybe you can work out where the guard will go ahead of time so that
# The Historians can search safely?

# You start by making a map (your puzzle input) of the situation.
# For example:

# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#...

# The map shows the current position of the guard with ^ (to indicate
# the guard is currently facing up from the perspective of the map).
# Any obstructions - crates, desks, alchemical reactors, etc. - are
# shown as #.

# Lab guards in 1518 follow a very strict patrol protocol which involves
# repeatedly following these steps:

#     If there is something directly in front of you, turn right 90 degrees.
#     Otherwise, take a step forward.

# Following the above protocol, the guard moves up several times until
# she reaches an obstacle (in this case, a pile of failed suit prototypes):

# ....#.....
# ....^....#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#...

# Because there is now an obstacle in front of the guard, she turns
# right before continuing straight in her new facing direction:

# ....#.....
# ........>#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#...

# Reaching another obstacle (a spool of several very long polymers),
# she turns right again and continues downward:

# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#......v.
# ........#.
# #.........
# ......#...

# This process continues for a while, but the guard eventually leaves
# the mapped area (after walking past a tank of universal solvent):

# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#v..

# By predicting the guard's route, you can determine which specific
# positions in the lab will be in the patrol path. Including the guard's
# starting position, the positions visited by the guard before leaving
# the area are marked with an X:

# ....#.....
# ....XXXXX#
# ....X...X.
# ..#.X...X.
# ..XXXXX#X.
# ..X.X.X.X.
# .#XXXXXXX.
# .XXXXXXX#.
# #XXXXXXX..
# ......#X..

# In this example, the guard will visit 41 distinct positions on your map.

# Predict the path of the guard. How many distinct positions will the guard
# visit before leaving the mapped area?

import numpy as np

inpt = []
with open('input.txt', 'r') as f_in:
    inpt = f_in.readlines()

    # Remove \n
    inpt = [i[:-1] for i in inpt]

h = len(inpt)
w = len(inpt[0])

gmap = np.zeros((h, w), dtype=np.int8)

empty = 0
guard_up = 1
guard_down = 2
guard_left = 3
guard_right = 4
guard_route = 7
crate = 9

# Guard location
guard_i = -1
guard_j = -1

for i, line in enumerate(inpt):
    for j, c in enumerate(line):
        if c == '^':
            gmap[i, j] = 1
            guard_i, guard_j = i, j
        elif c == 'v':
            gmap[i, j] = 2
            guard_i, guard_j = i, j
        elif c == '<':
            gmap[i, j] = 3
            guard_i, guard_j = i, j
        elif c == '>':
            gmap[i, j] = 4
            guard_i, guard_j = i, j
        elif c == '#':
            gmap[i, j] = 9

# # Guard init: stopping condition
# guard_beg_i = guard_i
# guard_beg_j = guard_j
# guard_beg = gmap[guard_i, guard_j]

# # stopping condition debug
# guard_beg_i = 1
# guard_beg_j = 4
# guard_beg = guard_up

print(gmap)


def move(gmap, guard_i, guard_j):
    # print(f'guard at {guard_i,guard_j}')
    # Find next guard position
    if gmap[guard_i, guard_j] == guard_up:
        next_i, next_j = guard_i - 1, guard_j

        # Check exit
        if next_i < 0:
            gmap[guard_i, guard_j] = guard_route
            return -1, -1

        # Check collisions
        # if next_i < 0 or gmap[next_i, next_j] == crate:
        if gmap[next_i, next_j] == crate:
            next_i = guard_i
            next_guard = guard_right
        else:
            next_guard = guard_up
    elif gmap[guard_i, guard_j] == guard_right:
        next_i, next_j = guard_i, guard_j + 1

        # Check exit
        if next_j >= w:
            gmap[guard_i, guard_j] = guard_route
            return -1, -1

        # Check collisions
        # if next_j >= w or gmap[next_i, next_j] == crate:
        if gmap[next_i, next_j] == crate:
            next_j = guard_j
            next_guard = guard_down
        else:
            next_guard = guard_right
    elif gmap[guard_i, guard_j] == guard_down:
        next_i, next_j = guard_i+1, guard_j

        # Check exit
        if next_i >= h:
            gmap[guard_i, guard_j] = guard_route
            return -1, -1

        # Check collisions
        # if next_i >= h or gmap[next_i, next_j] == crate:
        if gmap[next_i, next_j] == crate:
            next_i = guard_i
            next_guard = guard_left
        else:
            next_guard = guard_down
    elif gmap[guard_i, guard_j] == guard_left:
        next_i, next_j = guard_i, guard_j-1

        # Check exit
        if next_j < 0:
            gmap[guard_i, guard_j] = guard_route
            return -1, -1

        # Check collisions
        # if next_j < 0 or gmap[next_i, next_j] == crate:
        if gmap[next_i, next_j] == crate:
            next_j = guard_j
            next_guard = guard_up
        else:
            next_guard = guard_left

    gmap[guard_i, guard_j] = guard_route
    gmap[next_i, next_j] = next_guard
    return next_i, next_j


guard_i, guard_j = move(gmap, guard_i, guard_j)
# print(f'guard after move {guard_i,guard_j}')
# print(gmap)

while guard_i > 0 and guard_j > 0:
    guard_i, guard_j = move(gmap, guard_i, guard_j)
    # print(f'guard after move {guard_i,guard_j}')
    # print(gmap)
    # input()

# import sys
# np.set_printoptions(threshold=sys.maxsize, linewidth=100000,)

# answer is wrong by -1 ???
print(gmap)
print(sum(sum(gmap==guard_route)))

