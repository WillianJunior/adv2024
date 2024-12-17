

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

    # xmas_tree = np.zeros((h,w))
    # center = w//2+1
    # side = 0
    # down_count = 0
    # i = 0
    # while i < h:
    #     xmas_tree[i,center+side] = 1
    #     xmas_tree[i,center-side] = 1

    #     i += 1
    #     side += 1
    #     down_count += 1

    #     if down_count == 3:
    #         down_count = 0
    #         side -=2
    #         i -= 1

    # print(xmas_tree)
    # return


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

    from PIL import Image, ImageDraw, ImageFont

    for elapsed_time in tqdm(range(9000)):

        img = Image.new('L', (h, w))
        pixels = img.load()

        for pos, vel in robots:
            # print(pos, vel)
            p_x, p_y = pos
            v_x, v_y = vel

            p_x += v_x*elapsed_time
            p_y += v_y*elapsed_time
            
            p_x = p_x % w
            p_y = p_y % h

            # print(p_x,p_y)

            pixels[p_y, p_x] = 255

        img.save(f'i{elapsed_time}.png')

    # print(q1_count)
    # print(q2_count)
    # print(q3_count)
    # print(q4_count)

    # print(robots)


if __name__ == '__main__':
    main()