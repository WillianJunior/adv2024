# --- Day 11: Plutonian Pebbles ---

# The ancient civilization on Pluto was known for its ability to
# manipulate spacetime, and while The Historians explore their
# infinite corridors, you've noticed a strange set of physics-defying
# stones.

# At first glance, they seem like normal stones: they're arranged in a
# perfectly straight line, and each stone has a number engraved on it.

# The strange part is that every time you blink, the stones change.

# Sometimes, the number engraved on a stone changes. Other times, a
# stone might split in two, causing all the other stones to shift
# over a bit to make room in their perfectly straight line.

# As you observe them for a while, you find that the stones have a
# consistent behavior. Every time you blink, the stones each simultaneously
# change according to the first applicable rule in this list:

#     If the stone is engraved with the number 0, it is replaced by a stone
#     engraved with the number 1.
#     If the stone is engraved with a number that has an even number of digits,
#     it is replaced by two stones. The left half of the digits are engraved
#     on the new left stone, and the right half of the digits are engraved on
#     the new right stone. (The new numbers don't keep extra leading zeroes:
#     1000 would become stones 10 and 0.)
#     If none of the other rules apply, the stone is replaced by a new stone;
#     the old stone's number multiplied by 2024 is engraved on the new stone.

# No matter how the stones change, their order is preserved, and they stay
# on their perfectly straight line.

# How will the stones evolve if you keep blinking at them? You take a note
# of the number engraved on each stone in the line (your puzzle input).

# If you have an arrangement of five stones engraved with the numbers
# 0 1 10 99 999 and you blink once, the stones transform as follows:

#     The first stone, 0, becomes a stone marked 1.
#     The second stone, 1, is multiplied by 2024 to become 2024.
#     The third stone, 10, is split into a stone marked 1 followed by a
#         stone marked 0.
#     The fourth stone, 99, is split into two stones marked 9.
#     The fifth stone, 999, is replaced by a stone marked 2021976.

# So, after blinking once, your five stones would become an arrangement of
# seven stones engraved with the numbers 1 2024 1 0 9 9 2021976.

# Here is a longer example:

# Initial arrangement:
# 125 17

# After 1 blink:
# 253000 1 7

# After 2 blinks:
# 253 0 2024 14168

# After 3 blinks:
# 512072 1 20 24 28676032

# After 4 blinks:
# 512 72 2024 2 0 2 4 2867 6032

# After 5 blinks:
# 1036288 7 2 20 24 4048 1 4048 8096 28 67 60 32

# After 6 blinks:
# 2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2

# In this example, after blinking six times, you would have 22 stones.
# After blinking 25 times, you would have 55312 stones!

# Consider the arrangement of stones in front of you. How many stones will
# you have after blinking 25 times?

# --- Part Two ---

# The Historians sure are taking a long time. To be fair, 
# the infinite corridors are very large.

# How many stones would you have after blinking a total of 75 times?


import numpy as np
import numba
from numba import jit
from numba.typed import Dict
from collections import defaultdict
from tqdm import tqdm


def flatten(xss):
    return [x for xs in xss for x in xs]


dict_key_type = numba.core.types.Tuple([
    numba.core.types.int64,
    numba.core.types.int64,
])

blink_cache = defaultdict(lambda: -1)
g_blink_cache = Dict.empty(key_type=dict_key_type,
                           value_type=numba.core.types.int64)


def blink(n, blinks, blink_cache):
    # print(f'blink {n}-{blinks}')
    # input()
    if blink_cache[(n, blinks)] != -1:
        # print('cached...')
        return blink_cache[(n, blinks)]

    if blinks == 0:
        blink_cache[(n, blinks)] = 1
        return 1

    # Case 1
    if n == 0:
        # print(f'\tcase1')
        ret = blink(1, blinks - 1, blink_cache)
        blink_cache[(n, blinks)] = ret
        return ret

    # Case 2
    count = 0
    base = 1
    while n / base >= 1:
        count += 1
        base *= 10
    if count % 2 == 0:
        base = int(10**(count / 2))
        left = n // base
        right = n - (left * base)
        # print(f'\tcase2: {left, right}')
        ret = blink(left, blinks - 1, blink_cache) + blink(
            right, blinks - 1, blink_cache)
        blink_cache[(n, blinks)] = ret
        return ret

    # Case 3
    # print(f'\tcase3 {n * 2024}')
    ret = blink(n * 2024, blinks - 1, blink_cache)
    blink_cache[(n, blinks)] = ret
    return ret


# @jit(nopython=True, cache=True)
@jit(nopython=True)
def blink_jit(n, blinks, blink_cache):
    # print(f'blink {n}-{blinks}')
    # input()
    if blink_cache.get((n, blinks), default=-1) != -1:
        # print('cached...')
        return blink_cache[(n, blinks)]

    if blinks == 0:
        blink_cache[(n, blinks)] = 1
        return 1

    # Case 1
    if n == 0:
        # print(f'\tcase1')
        ret = blink_jit(1, blinks - 1, blink_cache)
        blink_cache[(n, blinks)] = ret
        return ret

    # Case 2
    count = 0
    base = 1
    while n / base >= 1:
        count += 1
        base *= 10
    if count % 2 == 0:
        base = int(10**(count / 2))
        left = n // base
        right = n - (left * base)
        # print(f'\tcase2: {left, right}')
        ret = blink_jit(left, blinks - 1, blink_cache) + blink_jit(
            right, blinks - 1, blink_cache)
        blink_cache[(n, blinks)] = ret
        return ret

    # Case 3
    # print(f'\tcase3 {n * 2024}')
    ret = blink_jit(n * 2024, blinks - 1, blink_cache)
    blink_cache[(n, blinks)] = ret
    return ret


def main():
    inpt = []
    with open('input.txt', 'r') as f_in:
        inpt = f_in.readlines()

        # Remove \n
        inpt = [i[:-1] for i in inpt]

    stones = inpt[0].split(' ')
    stones = [int(s) for s in stones]
    print(stones)

    blinks = 75

    lens = 0
    for s in tqdm(stones):
        # lens += blink_jit(s, blinks, g_blink_cache)
        lens += blink(s, blinks, blink_cache)

    # print(f'cache len: {len(g_blink_cache)}')
    # print(f'cache len: {len(blink_cache)}')
    print(lens)

    # Results:
    # numba dict is slower by ~3x
    # also, using cache=True results in segfault...


if __name__ == '__main__':
    main()