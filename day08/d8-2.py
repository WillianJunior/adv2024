# --- Day 8: Resonant Collinearity ---

# You find yourselves on the roof of a top-secret Easter Bunny installation.

# While The Historians do their thing, you take a look at the familiar huge
# antenna. Much to your surprise, it seems to have been reconfigured to emit
# a signal that makes people 0.1% more likely to buy Easter Bunny brand
# Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

# Scanning across the city, you find that there are actually many such antennas.
# Each antenna is tuned to a specific frequency indicated by a single lowercase
# letter, uppercase letter, or digit. You create a map (your puzzle input) of
# these antennas. For example:

# ............
# ........0...
# .....0......
# .......0....
# ....0.......
# ......A.....
# ............
# ............
# ........A...
# .........A..
# ............
# ............

# The signal only applies its nefarious effect at specific antinodes based
# on the resonant frequencies of the antennas. In particular, an antinode
# occurs at any point that is perfectly in line with two antennas of the
# same frequency - but only when one of the antennas is twice as far away
# as the other. This means that for any pair of antennas with the same
# frequency, there are two antinodes, one on either side of them.

# So, for these two antennas with frequency a, they create the two antinodes
# marked with #:

# ..........
# ...#......
# ..........
# ....a.....
# ..........
# .....a....
# ..........
# ......#...
# ..........
# ..........

# Adding a third antenna with the same frequency creates several more antinodes.
# It would ideally add four antinodes, but two are off the right side of the
# map, so instead it adds only two:

# ..........
# ...#......
# #.........
# ....a.....
# ........a.
# .....a....
# ..#.......
# ......#...
# ..........
# ..........

# Antennas with different frequencies don't create antinodes; A and a count as
# different frequencies. However, antinodes can occur at locations that contain
# antennas. In this diagram, the lone antenna with frequency capital A creates no
# antinodes but has a lowercase-a-frequency antinode at its location:

# ..........
# ...#......
# #.........
# ....a.....
# ........a.
# .....a....
# ..#.......
# ......A...
# ..........
# ..........

# The first example has antennas with two different frequencies, so the antinodes
# they create look like this, plus an antinode overlapping the topmost A-frequency
# antenna:

# ......#....#
# ...#....0...
# ....#0....#.
# ..#....0....
# ....0....#..
# .#....A.....
# ...#........
# #......#....
# ........A...
# .........A..
# ..........#.
# ..........#.

# Because the topmost A-frequency antenna overlaps with a 0-frequency antinode,
# there are 14 total unique locations that contain an antinode within the bounds
# of the map.

# Calculate the impact of the signal. How many unique locations within the bounds
# of the map contain an antinode?

import numpy as np
from numba import njit
from collections import defaultdict


def flatten(xss):
    return [x for xs in xss for x in xs]


def main():
    inpt = []
    with open('input.txt', 'r') as f_in:
        inpt = f_in.readlines()

        # Remove \n
        inpt = [i[:-1] for i in inpt]

    all_antennas = list(set(flatten(inpt)))
    all_antennas.remove('.')

    all_antennas_coords = defaultdict(lambda: [])
    for i, line, in enumerate(inpt):
        for j, point, in enumerate(line):
            if point != '.':
                all_antennas_coords[point].append((i, j))

    # print(all_antennas_coords)

    h = len(inpt)
    w = len(inpt[0])

    antinode_map = np.zeros((h, w), dtype=np.int8)

    for antn, coords in all_antennas_coords.items():
        # print(f'--------------- antenna {antn}')
        while len(coords) > 1:
            (base_i, base_j) = coords.pop(0)
            antinode_map[base_i, base_j] = 1
            # print(f'=== popping {base_i,base_j}')
            for i, j in coords:
                dist_i = base_i - i
                dist_j = base_j - j

                count = 1
                while True:
                    cur_dist_i = count * dist_i
                    cur_dist_j = count * dist_j
                    test1_i = base_i + cur_dist_i
                    test1_j = base_j + cur_dist_j
                    if test1_i < 0 or test1_i >= h or test1_j < 0 or test1_j >= w:
                        break

                    # print(f'antinode1 {base_i,base_i}/{i,j} '
                    #       f'in {test1_i,test1_j}')
                    antinode_map[test1_i, test1_j] = 1
                    count += 1

                count = 1
                while True:
                    cur_dist_i = count * dist_i
                    cur_dist_j = count * dist_j
                    test1_i = base_i - cur_dist_i
                    test1_j = base_j - cur_dist_j
                    if test1_i < 0 or test1_i >= h or test1_j < 0 or test1_j >= w:
                        break

                    # print(f'antinode2 {base_i,base_i}/{i,j} '
                    #       f'in {test1_i,test1_j}')
                    antinode_map[test1_i, test1_j] = 1
                    count += 1

    print(sum(sum(antinode_map)))


if __name__ == '__main__':
    main()