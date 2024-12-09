# --- Day 9: Disk Fragmenter ---
# --- Part Two ---

# Upon completion, two things immediately become clear. First, the
# disk definitely has a lot more contiguous free space, just like
# the amphipod hoped. Second, the computer is running much more slowly!
# Maybe introducing all of that file system fragmentation was a bad idea?

# The eager amphipod already has a new plan: rather than move individual
# blocks, he'd like to try compacting the files on his disk by moving
# whole files instead.

# This time, attempt to move whole files to the leftmost span of free
# space blocks that could fit the file. Attempt to move each file exactly
# once in order of decreasing file ID number starting with the file with
# the highest file ID number. If there is no span of free space to the
# left of a file that is large enough to fit the file, the file does not
# move.

# The first example from above now proceeds differently:

# 00...111...2...333.44.5555.6666.777.888899
# 0099.111...2...333.44.5555.6666.777.8888..
# 0099.1117772...333.44.5555.6666.....8888..
# 0099.111777244.333....5555.6666.....8888..
# 00992111777.44.333....5555.6666.....8888..

# The process of updating the filesystem checksum is the same; now, this
# example's checksum would be 2858.

# Start over, now compacting the amphipod's hard drive using this new method
# instead. What is the resulting filesystem checksum?

import numpy as np
from numba import njit
from collections import defaultdict
from tqdm import tqdm


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

    # Remove 0 count blocks
    diskmap2 = [[b_id, count] for (b_id, count) in diskmap2 if count > 0]
    BLK_ID = 0
    COUNT = 1
    # print(diskmap2)
    # print()

    # left_idx_base = 0
    right_idx = len(diskmap2) - 1
    # while left_idx_base < right_idx:
    pbar = tqdm(total=len(diskmap2))
    while right_idx > 0:
        # If right point is not a file region: go to prev
        if diskmap2[right_idx][BLK_ID] < 0:
            right_idx -= 1
            pbar.update(1)
            continue

        count_to_move = diskmap2[right_idx][COUNT]

        # Try to move the current file
        for left_idx_cur in range(0, right_idx):
            if diskmap2[left_idx_cur][BLK_ID] >= 0:
                continue

            if diskmap2[left_idx_cur][COUNT] > count_to_move:
                # More space than files to move

                # Remove free space
                diskmap2[left_idx_cur][COUNT] -= count_to_move

                # Create a new file region before the current free region
                file_block = diskmap2[right_idx]
                diskmap2.insert(left_idx_cur,
                                [diskmap2[right_idx][BLK_ID], count_to_move])
                diskmap2[right_idx + 1][BLK_ID] = -1

                # Since we popped, we dont need de -=1 later
                right_idx += 1
                pbar.update(-1)

                break

            elif diskmap2[left_idx_cur][COUNT] == count_to_move:
                # Files and space are the same

                # Set the remaining free space as a file space
                diskmap2[left_idx_cur][BLK_ID] = diskmap2[right_idx][BLK_ID]
                diskmap2[right_idx][BLK_ID] = -1

                break

        # Move right_idx since the last block was resolved
        pbar.update(1)
        right_idx -= 1

    pbar.close()
    checksum = 0
    i = 0
    for [blk_id, count] in diskmap2:
        for _ in range(count):
            if blk_id > 0:
                checksum += i * blk_id
            i += 1

    print(checksum)


if __name__ == '__main__':
    main()