# --- Day 9: Disk Fragmenter ---

# Another push of the button leaves you in the familiar hallways of
# some friendly amphipods! Good thing you each somehow got your own
# personal mini submarine. The Historians jet away in search of the
# Chief, mostly by driving directly into walls.

# While The Historians quickly figure out how to pilot these things,
# you notice an amphipod in the corner struggling with his computer.
# He's trying to make more contiguous free space by compacting all of
# the files, but his program isn't working; you offer to help.

# He shows you the disk map (your puzzle input) he's already generated.
# For example:

# 2333133121414131402

# The disk map uses a dense format to represent the layout of files and
# free space on the disk. The digits alternate between indicating the
# length of a file and the length of free space.

# So, a disk map like 12345 would represent a one-block file, two blocks
# of free space, a three-block file, four blocks of free space, and
# then a five-block file. A disk map like 90909 would represent three
# nine-block files in a row (with no free space between them).

# Each file on disk also has an ID number based on the order of the
# files as they appear before they are rearranged, starting with ID 0.
# So, the disk map 12345 has three files: a one-block file with ID 0,
# a three-block file with ID 1, and a five-block file with ID 2. Using one
# character for each block where digits are the file ID and . is free
# space, the disk map 12345 represents these individual blocks:

# 0..111....22222

# The first example above, 2333133121414131402, represents these
# individual blocks:

# 00...111...2...333.44.5555.6666.777.888899

# The amphipod would like to move file blocks one at a time from the
# end of the disk to the leftmost free space block (until there are
#     no gaps remaining between file blocks). For the disk map 12345,
# the process looks like this:

# 0..111....22222
# 02.111....2222.
# 022111....222..
# 0221112...22...
# 02211122..2....
# 022111222......

# The first example requires a few more steps:

# 00...111...2...333.44.5555.6666.777.888899
# 009..111...2...333.44.5555.6666.777.88889.
# 0099.111...2...333.44.5555.6666.777.8888..
# 00998111...2...333.44.5555.6666.777.888...
# 009981118..2...333.44.5555.6666.777.88....
# 0099811188.2...333.44.5555.6666.777.8.....
# 009981118882...333.44.5555.6666.777.......
# 0099811188827..333.44.5555.6666.77........
# 00998111888277.333.44.5555.6666.7.........
# 009981118882777333.44.5555.6666...........
# 009981118882777333644.5555.666............
# 00998111888277733364465555.66.............
# 0099811188827773336446555566..............

# The final step of this file-compacting process is to update the filesystem
# checksum. To calculate the checksum, add up the result of multiplying each
# of these blocks' position with the file ID number it contains. The leftmost
# block is in position 0. If a block contains free space, skip it instead.

# Continuing the first example, the first few blocks' position multiplied
# by its file ID number are 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27,
#     4 * 8 = 32, and so on.
# In this example, the checksum is the sum of these, 1928.

# Compact the amphipod's hard drive using the process he requested.
# What is the resulting filesystem checksum? (Be careful copy/pasting
# the input for this puzzle; it is a single, very long line.)

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

    diskmap = [int(n) for n in inpt[0]]
    diskmap = np.array(diskmap, dtype=np.int32)

    # 2d list. each element is a pair of (id, count)
    diskmap2 = []

    cur_id = 0
    is_file = True
    for i in range(len(diskmap)):
        count = diskmap[i]
        if is_file:
            diskmap2.append([cur_id, count])
            cur_id += 1
            is_file = False
        else:
            diskmap2.append([-1, count])
            is_file = True

    # diskmap2 = np.array(diskmap2)
    # Remove 0 count blocks
    diskmap2 = [[b_id, count] for (b_id, count) in diskmap2 if count > 0]
    BLK_ID = 0
    COUNT = 1
    print(diskmap2)
    print()

    left_idx = 0
    right_idx = len(diskmap2) - 1
    while left_idx < right_idx:
        print(f'{left_idx}/{right_idx}')
        # If left point is not a free region: go to next
        if diskmap2[left_idx][BLK_ID] >= 0:
            # print(f'{left_idx}/{right_idx} left not free')
            left_idx += 1
            continue

        # If right point is not a file region: go to prev
        if diskmap2[right_idx][BLK_ID] < 0:
            # print(f'{left_idx}/{right_idx} right not a file')
            diskmap2.pop(right_idx)
            right_idx -= 1
            continue

        n_can_move = diskmap2[left_idx][COUNT]
        count_to_move = diskmap2[right_idx][COUNT]

        if n_can_move > count_to_move:
            # print(f'{left_idx}/{right_idx} more space')
            # More space than files to move

            # Remove free space
            diskmap2[left_idx] = [-1, n_can_move - count_to_move]

            # Create a new file region before the current free region
            file_block = diskmap2.pop(right_idx)
            diskmap2.insert(left_idx, file_block)

            # Move left_idx since the a new file
            # region was created at this position
            left_idx += 1
        elif n_can_move < count_to_move:
            # print(f'{left_idx}/{right_idx} more files')
            # More files than available space here

            # Set the remaining free space as a file space
            diskmap2[left_idx][BLK_ID] = diskmap2[right_idx][BLK_ID]

            # Update file space at the end
            diskmap2[right_idx][COUNT] -= diskmap2[left_idx][COUNT]

            # left_idx got to the next location
            left_idx += 1
        else:
            # print(f'{left_idx}/{right_idx} same')
            # Files and space are the same

            # Set the remaining free space as a file space
            file_block = diskmap2.pop(right_idx)
            diskmap2[left_idx][BLK_ID] = file_block[BLK_ID]

            # Move right_idx since the last block was removed
            right_idx -= 1


        # print(diskmap2)

    checksum = 0
    i = 0
    for [blk_id, count] in diskmap2:
        for _ in range(count):
            checksum += i*blk_id
            i += 1

    print(checksum)



if __name__ == '__main__':
    main()