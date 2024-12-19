# --- Day 17: Chronospatial Computer ---

# --- Part Two ---

# Digging deeper in the device's manual, you discover the problem: 
# this program is supposed to output another copy of the program! 
# Unfortunately, the value in register A seems to have been corrupted. 
# You'll need to find a new value to which you can initialize register 
# A so that the program's output instructions produce an exact copy of 
# the program itself.

# For example:

# Register A: 2024
# Register B: 0
# Register C: 0

# Program: 0,3,5,4,3,0

# This program outputs a copy of itself if register A is instead 
# initialized to 117440. (The original initial value of register A, 
#     2024, is ignored.)

# What is the lowest positive initial value for register A that causes 
# the program to output a copy of itself?

import numpy as np
from tqdm import tqdm
from multiprocessing import Pool
from time import time
from numba import jit
from collections import defaultdict
from math import ceil, floor, prod
import sys

# np.set_printoptions(threshold=np.inf)
# np.set_printoptions(linewidth=np.inf)


# def print_mat(m):
#     np.set_printoptions(threshold=np.inf)
#     np.set_printoptions(linewidth=np.inf)
#     print(np.array2string(m, separator='', formatter={'str_kind':
#                                                      lambda x: x}))


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

    i = 0
    registers = [-1, -1, -1]
    instructions = []

    for i in range(3):
        registers[i] = int(inpt[i].split(' ')[2])
    registers = np.array(registers)

    instructions = inpt[4].split(' ')[1].split(',')
    instructions = [int(i) for i in instructions]
    gab = instructions.copy()
    instructions = np.array(instructions)

    print(registers)
    print(instructions)

    A = 0
    B = 1
    C = 2

    combo = dict()
    combo[4] = A
    combo[5] = B
    combo[6] = C

    f_ops = dict()

    output = []

    def get_combo(op):
        if op <= 3:
            return op
        else:
            return registers[combo[op]]

    def adv(op, ip):
        registers[A] = registers[A] // 2**get_combo(op)
        return ip + 2, None

    f_ops[0] = adv

    def bxl(op, ip):
        registers[B] = registers[B] ^ op
        return ip + 2, None

    f_ops[1] = bxl

    def bst(op, ip):
        registers[B] = get_combo(op) & 0b0111
        return ip + 2, None

    f_ops[2] = bst

    def jnz(op, ip):
        if registers[A] != 0:
            return op, None
        else:
            return ip + 2, None

    f_ops[3] = jnz

    def bxc(op, ip):
        registers[B] = registers[B] ^ registers[C]
        return ip + 2, None

    f_ops[4] = bxc

    def out(op, ip):
        res = get_combo(op) & 0b0111
        # print(f'{res},', end='')
        output.append(res)
        return ip + 2, res

    f_ops[5] = out

    def bdv(op, ip):
        registers[B] = registers[A] // 2**get_combo(op)
        return ip + 2, None

    f_ops[6] = bdv

    def cdv(op, ip):
        registers[C] = registers[A] // 2**get_combo(op)
        return ip + 2, None

    f_ops[7] = cdv

    
    def run_program(a):
        output = []
        registers[A] = a
        registers[B] = 0
        registers[C] = 0
        ip = 0
        # print(gab)

        gab_i = 0
        while ip < len(instructions):
            # print(f'{ip}: f_op{instructions[ip]} ({instructions[ip + 1]})')
            ip, o = f_ops[instructions[ip]](instructions[ip + 1], ip)
            # print()

            if o is not None:
                # print(f'print: {o}')
                output.append(o)
                if gab[gab_i] == o:
                    gab_i += 1
                else:
                    print(registers)
                    print(gab)
                    print(output)
                    print()
                    return False

        # print('done:')
        # print(gab)
        print(registers)
        if output == gab:
            return True
        else:
            return False

    i = 0
    while not run_program(i):
        i += 1
        # print('.', end='')
        # print(f'{i}')
    print(i)


    print(registers)
    print(output)


if __name__ == '__main__':
    main()