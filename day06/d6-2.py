# --- Day 6: Guard Gallivant ---

# --- Part Two ---

# While The Historians begin working around the guard's patrol route,
# you borrow their fancy device and step outside the lab. From the
# safety of a supply closet, you time travel through the last few months
# and record the nightly status of the lab's guard post on the walls of
# the closet.

# Returning after what seems like only a few seconds to The Historians,
# they explain that the guard's patrol area is simply too large for them
# to safely search the lab without getting caught.

# Fortunately, they are pretty sure that adding a single new obstruction
# won't cause a time paradox. They'd like to place the new obstruction in
# such a way that the guard will get stuck in a loop, making the rest of
# the lab safe to search.

# To have the lowest chance of creating a time paradox, The Historians would
# like to know all of the possible positions for such an obstruction. The
# new obstruction can't be placed at the guard's starting position - the
# guard is there right now and would notice.

# In the above example, there are only 6 different positions where a new
# obstruction would cause the guard to get stuck in a loop. The diagrams
# of these six situations use O to mark the new obstruction, | to show a
# position where the guard moves up/down, - to show a position where the
# guard moves left/right, and + to show a position where the guard moves
# both up/down and left/right.

# Option one, put a printing press next to the guard's starting position:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ....|..#|.
# ....|...|.
# .#.O^---+.
# ........#.
# #.........
# ......#...

# Option two, put a stack of failed suit prototypes in the bottom
# right quadrant of the mapped area:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# ......O.#.
# #.........
# ......#...

# Option three, put a crate of chimney-squeeze prototype fabric next to
# the standing desk in the bottom right quadrant:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# .+----+O#.
# #+----+...
# ......#...

# Option four, put an alchemical retroencabulator near the bottom left corner:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# ..|...|.#.
# #O+---+...
# ......#...

# Option five, put the alchemical retroencabulator a bit to the right instead:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# ....|.|.#.
# #..O+-+...
# ......#...

# Option six, put a tank of sovereign glue right next to the tank of
# universal solvent:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# .+----++#.
# #+----++..
# ......#O..

# It doesn't really matter what you choose to use as an obstacle so long
# as you and The Historians can put it into position without the guard
# noticing. The important thing is having enough options that you can find
# one that minimizes time paradoxes, and in this example, there are 6
# different positions you could choose.

# You need to get the guard stuck in a loop by adding a single new obstruction.
# How many different positions could you choose for this obstruction?

import numpy as np
from tqdm import tqdm
from multiprocessing import Pool
from time import time
from numba import jit

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

# Using a bit mask:
# most sig. is sign
# 3 least sig is for guard loc
# remaining 4 is for masking already ran direction
guard_route_up = 0b00001000
guard_route_down = 0b00010000
guard_route_left = 0b00100000
guard_route_right = 0b01000000

# Obstacles is largest value (non negative)
crate = 127

guard_mask = 0b00000111
route_mask = 0b01111000

@jit(nopython=True)
def move(gmap, guard_i, guard_j):
    # Find next guard position
    cur_guard = gmap[guard_i, guard_j] & guard_mask
    # print(f'{gmap[guard_i, guard_j]}')
    # print(f'guard {cur_guard} at {guard_i,guard_j}')

    cur_route = None

    # Up ----------------------------------------
    if cur_guard == guard_up:
        next_i, next_j = guard_i - 1, guard_j

        # Check exit
        if next_i < 0:
            return -1, -1

        # Check loop
        if gmap[guard_i, guard_j] & guard_route_up > 0:
            # print('loop up')
            return -2, -2

        # Check collisions
        if gmap[next_i, next_j] == crate:
            next_i = guard_i
            next_guard = guard_right
        else:
            cur_route = guard_route_up
            next_guard = guard_up

    # Right --------------------------------------
    elif cur_guard == guard_right:
        next_i, next_j = guard_i, guard_j + 1

        # Check exit
        if next_j >= w:
            return -1, -1

        # Check loop
        if gmap[guard_i, guard_j] & guard_route_right > 0:
            # print('loop right')
            return -2, -2

        # Check collisions
        if gmap[next_i, next_j] == crate:
            next_j = guard_j
            next_guard = guard_down
        else:
            cur_route = guard_route_right
            next_guard = guard_right

    # Down --------------------------------------
    elif cur_guard == guard_down:
        next_i, next_j = guard_i + 1, guard_j

        # Check exit
        if next_i >= h:
            return -1, -1

        # Check loop
        if gmap[guard_i, guard_j] & guard_route_down > 0:
            # print('loop down')
            return -2, -2

        # Check collisions
        if gmap[next_i, next_j] == crate:
            next_i = guard_i
            next_guard = guard_left
        else:
            cur_route = guard_route_down
            next_guard = guard_down

    # Left -------------------------------------
    elif cur_guard == guard_left:
        next_i, next_j = guard_i, guard_j - 1

        # Check exit
        if next_j < 0:
            return -1, -1

        # Check loop
        if gmap[guard_i, guard_j] & guard_route_left > 0:
            # print('loop left')
            return -2, -2

        # Check collisions
        if gmap[next_i, next_j] == crate:
            next_j = guard_j
            next_guard = guard_up
        else:
            cur_route = guard_route_left
            next_guard = guard_left

    # Remove guard value
    gmap[guard_i, guard_j] -= cur_guard

    # Add mask for passing direction
    # If making a curve, no new route is added
    if cur_route is not None:
        gmap[guard_i, guard_j] |= cur_route

    # Add guard direction to next position
    gmap[next_i, next_j] += next_guard

    return next_i, next_j


def single_try(gmap_test, new_crate, guard_i, guard_j):
    gmap_test[new_crate] = crate

    while True:
        guard_i, guard_j = move(gmap_test, guard_i, guard_j)

        # Check if exit
        if guard_i == -1 and guard_j == -1:
            return 0

        # Check if loop
        if guard_i == -2 and guard_j == -2:
            return 1


def main():
    # Guard location
    guard_i = -1
    guard_j = -1

    for i, line in enumerate(inpt):
        for j, c in enumerate(line):
            if c == '^':
                gmap[i, j] = guard_up
                guard_i, guard_j = i, j
            elif c == 'v':
                gmap[i, j] = guard_down
                guard_i, guard_j = i, j
            elif c == '<':
                gmap[i, j] = guard_left
                guard_i, guard_j = i, j
            elif c == '>':
                gmap[i, j] = guard_right
                guard_i, guard_j = i, j
            elif c == '#':
                gmap[i, j] = crate

    # Guard init: stopping condition
    guard_beg_i = guard_i
    guard_beg_j = guard_j

    all_creates = []
    for i in range(h):
        for j in range(w):
            if gmap[i, j] == empty:
                all_creates.append((i, j))

    def parallel(gmap, all_creates, guard_i, guard_j):
        # Numpy copy is lazy, thankfully....
        tries = [[gmap.copy(), nc, guard_i, guard_j] for nc in all_creates]

        p = Pool(16)
        ret = p.starmap(single_try, tqdm(tries))
        print(sum(ret))

    def serial(gmap, all_creates, guard_i, guard_j):
        count = 0
        for new_crate in tqdm(all_creates):
            # Reset the map
            gmap_test = gmap.copy()
            guard_i = guard_beg_i
            guard_j = guard_beg_j

            count += single_try(gmap_test, new_crate, guard_i, guard_j)
        print(count)

    # Test all possible creates positions
    t0 = time()
    serial(gmap, all_creates, guard_i, guard_j)
    # parallel(gmap, all_creates, guard_i, guard_j)
    t1 = time()

    print(f'ran in {t1-t0:.2f}')

    # serialized time: 7m41s: 461s
    # parallel time  8 procs:  64s
    # parallel time 16 procs:  57s

    # serialized numba: 17.38s
    # parallel 8 procs:  3.27s
    # parallel 16 procs: 3.48s
if __name__ == '__main__':
    main()