# --- Day 14: Restroom Redoubt ---

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

    w = 101
    h = 103

    elapsed_time = 100

    robots = []
    for l in inpt:
        [pos, vel] = l.replace('p=','').replace('v=','').split(' ')
        pos = [int(x) for x in pos.split(',')]
        vel = [int(x) for x in vel.split(',')]
        robots.append((pos, vel))

    q1_count = 0
    q2_count = 0
    q3_count = 0
    q4_count = 0

    for pos, vel in robots:
        # print(pos, vel)
        p_x, p_y = pos
        v_x, v_y = vel

        p_x += v_x*elapsed_time
        p_y += v_y*elapsed_time
        
        p_x = p_x % w
        p_y = p_y % h


        # print(f'end: {p_x,p_y}')

        left_q = p_x < w//2
        right_q = p_x > w//2
        up_q = p_y < h//2
        down_q = p_y >  h//2

        if left_q and up_q:
            q1_count += 1
        elif right_q and up_q:
            q2_count += 1
        elif left_q and down_q:
            q3_count += 1
        elif right_q and down_q:
            q4_count += 1

    # print(q1_count)
    # print(q2_count)
    # print(q3_count)
    # print(q4_count)

    print(q1_count*q2_count*q3_count*q4_count)



    # print(robots)


if __name__ == '__main__':
    main()