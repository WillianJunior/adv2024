# --- Day 12: Garden Groups ---

# --- Part Two ---

# Fortunately, the Elves are trying to order so much fence that they
# qualify for a bulk discount!

# Under the bulk discount, instead of using the perimeter to calculate
# the price, you need to use the number of sides each region has. Each
# straight section of fence counts as a side, regardless of how long it is.

# Consider this example again:

# AAAA
# BBCD
# BBCC
# EEEC

# The region containing type A plants has 4 sides, as does each of the
# regions containing plants of type B, D, and E. However, the more
# complex region containing the plants of type C has 8 sides!

# Using the new method of calculating the per-region price by multiplying
# the region's area by its number of sides, regions A through E have
# prices 16, 16, 32, 4, and 12, respectively, for a total price of 80.

# The second example above (full of type X and O plants) would have a
# total price of 436.

# Here's a map that includes an E-shaped region full of type E plants:

# EEEEE
# EXXXX
# EEEEE
# EXXXX
# EEEEE

# The E-shaped region has an area of 17 and 12 sides for a price of 204.
# Including the two regions full of type X plants, this map has a total
# price of 236.

# This map has a total price of 368:

# AAAAAA
# AAABBA
# AAABBA
# ABBAAA
# ABBAAA
# AAAAAA

# It includes two regions full of type B plants (each with 4 sides) and a
# single region full of type A plants (with 4 sides on the outside and 8
#     more sides on the inside, a total of 12 sides). Be especially careful
# when counting the fence around regions like the one full of type A plants;
# in particular, each section of fence has an in-side and an out-side, so
# the fence does not connect across the middle of the region (where the two
#     B regions touch diagonally). (The Elves would have used the Möbius
#     Fencing Company instead, but their contract terms were too one-sided.)

# The larger example from before now has the following updated prices:

#     A region of R plants with price 12 * 10 = 120.
#     A region of I plants with price 4 * 4 = 16.
#     A region of C plants with price 14 * 22 = 308.
#     A region of F plants with price 10 * 12 = 120.
#     A region of V plants with price 13 * 10 = 130.
#     A region of J plants with price 11 * 12 = 132.
#     A region of C plants with price 1 * 4 = 4.
#     A region of E plants with price 13 * 8 = 104.
#     A region of I plants with price 14 * 16 = 224.
#     A region of M plants with price 5 * 6 = 30.
#     A region of S plants with price 3 * 6 = 18.

# Adding these together produces its new total price of 1206.

import numpy as np
from tqdm import tqdm
from multiprocessing import Pool
from time import time
from numba import jit
from collections import defaultdict


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

    garden = np.array(conv_2d(inpt, lambda x: x))
    # garden = np.array(inpt)

    print(garden)
    h, w = garden.shape

    # IWPP for finding unique plots
    unique_garden = np.full((h, w), -1)
    update = 1
    new_plot_id = 0
    while update > 0:
        update = 0

        for i in range(h):
            for j in range(w):
                plot = garden[i, j]

                if i > 0 and garden[i - 1, j] == plot:
                    if unique_garden[i - 1,
                                     j] != -1 and unique_garden[i, j] == -1:
                        unique_garden[i, j] = unique_garden[i - 1, j]
                        update += 1
                        # print(f'{i,j} up: {unique_garden[i,j]}')
                        continue
                    elif unique_garden[i - 1, j] < unique_garden[i, j]:
                        unique_garden[i, j] = unique_garden[i - 1, j]
                        # print(f'{i,j} up---------------------: {unique_garden[i,j]}')
                        update += 1
                        continue

                if j > 0 and garden[i, j - 1] == plot:
                    if unique_garden[i, j -
                                     1] != -1 and unique_garden[i, j] == -1:
                        unique_garden[i, j] = unique_garden[i, j - 1]
                        update += 1
                        # print(f'{i,j} left: {unique_garden[i,j]}')
                        continue
                    elif unique_garden[i, j - 1] < unique_garden[i, j]:
                        unique_garden[i, j] = unique_garden[i, j - 1]
                        # print(f'{i,j} left------------------: {unique_garden[i,j]}')
                        update += 1
                        continue

                if i < h - 1 and garden[i + 1, j] == plot:
                    if unique_garden[i + 1,
                                     j] != -1 and unique_garden[i, j] == -1:
                        unique_garden[i, j] = unique_garden[i + 1, j]
                        update += 1
                        # print(f'{i,j} down: {unique_garden[i,j]}')
                        continue
                    elif unique_garden[i + 1, j] < unique_garden[i, j]:
                        unique_garden[i, j] = unique_garden[i + 1, j]
                        # print(f'{i,j} down-------------------------: {unique_garden[i,j]}')
                        update += 1
                        continue

                if j < w - 1 and garden[i, j + 1] == plot:
                    if unique_garden[i, j +
                                     1] != -1 and unique_garden[i, j] == -1:
                        unique_garden[i, j] = unique_garden[i, j + 1]
                        update += 1
                        # print(f'{i,j} right: {unique_garden[i,j]}')
                        continue
                    elif unique_garden[i, j + 1] < unique_garden[i, j]:
                        unique_garden[i, j] = unique_garden[i, j + 1]
                        # print(f'{i,j} right---------------------: {unique_garden[i,j]}')
                        update += 1
                        continue

                if unique_garden[i, j] == -1:
                    # print(f'----- new {i,j}')
                    unique_garden[i, j] = new_plot_id
                    new_plot_id += 1

    print(unique_garden)

    # Count of corners and areas per plot
    corners = defaultdict(lambda: 0)
    areas = defaultdict(lambda: 0)

    # Checking 4 intersections
    #   |
    # - + -
    #   |

    def is_up_line(i, j, unique_garden):
        return unique_garden[i, j] != unique_garden[i, j + 1]

    def is_down_line(i, j, unique_garden):
        return unique_garden[i + 1, j] != unique_garden[i + 1, j + 1]

    def is_left_line(i, j, unique_garden):
        return unique_garden[i, j] != unique_garden[i + 1, j]

    def is_right_line(i, j, unique_garden):
        return unique_garden[i, j + 1] != unique_garden[i + 1, j + 1]

    for i in range(-1, h):
        for j in range(-1, w):
            up_line = False
            down_line = False
            left_line = False
            right_line = False

            if i < 0:
                if j < 0:
                    down_line = True
                    right_line = True
                elif j < w - 1:
                    left_line = True
                    right_line = True
                    down_line = is_down_line(i, j, unique_garden)
                else:
                    left_line = True
                    down_line = True

            elif i < h - 1:
                if j < 0:
                    up_line = True
                    down_line = True
                    right_line = is_right_line(i, j, unique_garden)
                elif j < w - 1:
                    up_line = is_up_line(i, j, unique_garden)
                    down_line = is_down_line(i, j, unique_garden)
                    left_line = is_left_line(i, j, unique_garden)
                    right_line = is_right_line(i, j, unique_garden)
                else:
                    up_line = True
                    down_line = True
                    left_line = is_left_line(i, j, unique_garden)
            else:
                if j < 0:
                    up_line = True
                    right_line = True
                elif j < w - 1:
                    left_line = True
                    right_line = True
                    up_line = is_up_line(i, j, unique_garden)
                else:
                    up_line = True
                    left_line = True

            if up_line and down_line and left_line and right_line:
                # CASE: all directions
                up_left_plot = unique_garden[i, j]
                down_left_plot = unique_garden[i + 1, j]
                up_right_plot = unique_garden[i, j + 1]
                down_right_plot = unique_garden[i + 1, j + 1]

                corners[up_left_plot] += 1
                corners[down_left_plot] += 1
                corners[up_right_plot] += 1
                corners[down_right_plot] += 1

            elif down_line and left_line and right_line:
                # CASE: 3 directions
                down_left_plot = unique_garden[i + 1, j]
                down_right_plot = unique_garden[i + 1, j + 1]
                corners[down_left_plot] += 1
                corners[down_right_plot] += 1

            elif up_line and left_line and right_line:
                # CASE: 3 directions
                up_left_plot = unique_garden[i, j]
                up_right_plot = unique_garden[i, j + 1]
                corners[up_left_plot] += 1
                corners[up_right_plot] += 1

            elif up_line and down_line and right_line:
                # CASE: 3 directions
                up_right_plot = unique_garden[i, j + 1]
                down_right_plot = unique_garden[i + 1, j + 1]
                corners[up_right_plot] += 1
                corners[down_right_plot] += 1

            elif up_line and down_line and left_line:
                # CASE: 3 directions
                up_left_plot = unique_garden[i, j]
                down_left_plot = unique_garden[i + 1, j]
                corners[up_left_plot] += 1
                corners[down_left_plot] += 1

            else:
                # CASE: 2 directions exclusive (without 4)
                if up_line and left_line:
                    if i >= 0 and i < h and j >= 0 and j < w:
                        up_left_plot = unique_garden[i, j]
                        corners[up_left_plot] += 1

                    if i + 1 >= 0 and i + 1 < h and j + 1 >= 0 and j + 1 < w:
                        down_right_plot = unique_garden[i + 1, j + 1]
                        corners[down_right_plot] += 1

                if up_line and right_line:
                    if i >= 0 and i < h and j + 1 >= 0 and j + 1 < w:
                        up_right_plot = unique_garden[i, j + 1]
                        corners[up_right_plot] += 1

                    if i + 1 >= 0 and i + 1 < h and j >= 0 and j < w:
                        down_left_plot = unique_garden[i + 1, j]
                        corners[down_left_plot] += 1

                if down_line and right_line:
                    if i + 1 >= 0 and i + 1 < h and j + 1 >= 0 and j + 1 < w:
                        down_right_plot = unique_garden[i + 1, j + 1]
                        corners[down_right_plot] += 1

                    if i >= 0 and i < h and j >= 0 and j < w:
                        up_left_plot = unique_garden[i, j]
                        corners[up_left_plot] += 1

                if down_line and left_line:
                    if i + 1 >= 0 and i + 1 < h and j >= 0 and j < w:
                        down_left_plot = unique_garden[i + 1, j]
                        corners[down_left_plot] += 1

                    if i >= 0 and i < h and j + 1 >= 0 and j + 1 < w:
                        up_right_plot = unique_garden[i, j + 1]
                        corners[up_right_plot] += 1

            if i >= 0 and i < h and j >= 0 and j < w:
                areas[unique_garden[i, j]] += 1

    price = 0
    for p, a in zip(corners.values(), areas.values()):
        price += p * a

    # print(f'areas: {areas.values()}')
    # print(f'corners: {corners.values()}')
    print(price)


if __name__ == '__main__':
    main()