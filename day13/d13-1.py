# --- Day 13: Claw Contraption ---

# Next up: the lobby of a resort on a tropical island. The Historians 
# take a moment to admire the hexagonal floor tiles before spreading out.

# Fortunately, it looks like the resort has a new arcade! Maybe you can 
# win some prizes from the claw machines?

# The claw machines here are a little unusual. Instead of a joystick or 
# directional buttons to control the claw, these machines have two buttons 
# labeled A and B. Worse, you can't just put in a token and play; it costs 
# 3 tokens to push the A button and 1 token to push the B button.

# With a little experimentation, you figure out that each machine's buttons 
# are configured to move the claw a specific amount to the right (along 
#     the X axis) and a specific amount forward (along the Y axis) each time 
# that button is pressed.

# Each machine contains one prize; to win the prize, the claw must be 
# positioned exactly above the prize on both the X and Y axes.

# You wonder: what is the smallest number of tokens you would have to spend 
# to win as many prizes as possible? You assemble a list of every machine's 
# button behavior and prize location (your puzzle input). For example:

# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400

# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176

# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=7870, Y=6450

# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=18641, Y=10279

# This list describes the button configuration and prize location of four 
# different claw machines.

# For now, consider just the first claw machine in the list:

#     Pushing the machine's A button would move the claw 94 units along the X 
#     axis and 34 units along the Y axis.

#     Pushing the B button would move the claw 22 units along the X axis 
#     and 67 units along the Y axis.

#     The prize is located at X=8400, Y=5400; this means that from the claw's 
#     initial position, it would need to move exactly 8400 units along the X 
#     axis and exactly 5400 units along the Y axis to be perfectly aligned 
#     with the prize in this machine.

# The cheapest way to win the prize is by pushing the A button 80 times and 
# the B button 40 times. This would line up the claw along the X axis (because 
#     80*94 + 40*22 = 8400) and along the Y axis (because 80*34 + 40*67 = 5400). 
# Doing this would cost 80*3 tokens for the A presses and 40*1 for the B 
# presses, a total of 280 tokens.

# For the second and fourth claw machines, there is no combination of A and B 
# presses that will ever win a prize.

# For the third claw machine, the cheapest way to win the prize is by pushing 
# the A button 38 times and the B button 86 times. Doing this would cost a 
# total of 200 tokens.

# So, the most prizes you could possibly win is two; the minimum tokens you 
# would have to spend to win all (two) prizes is 480.

# You estimate that each button would need to be pressed no more than 100 
# times to win a prize. How else would someone be expected to play?

# Figure out how to win as many prizes as possible. What is the fewest tokens 
# you would have to spend to win all possible prizes?


import numpy as np
from tqdm import tqdm
from multiprocessing import Pool
from time import time
from numba import jit
from collections import defaultdict
from math import ceil, floor


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

    bt_A = 0
    bt_B = 1
    prize_pos = 2

    A_price = 3
    B_price = 1

    machines = []
    machine = []
    line_count = 0
    for l in inpt:
        if len(l) == 0:
            machines.append(machine)
            machine = []
            continue

        vals = l.split(':')[1].replace('X','').replace(
            'Y','').replace('=','').replace('+','').split(',')
        vals = [int(v) for v in vals]

        machine.append(tuple(vals))

    print(machines)
    print(len(machines))

    all_cost = 0
    for (A, B, prize_pos) in machines:
        A_price = 3
        B_price = 1

        A_press = (prize_pos[0]*B[1] - prize_pos[1]*B[0]) / (A[0]*B[1] - A[1]*B[0])
        B_press = (A[0]*prize_pos[1] - A[1]*prize_pos[0]) / (A[0]*B[1] - A[1]*B[0])

        if (floor(A_press)*A[0] + floor(B_press)*B[0] == prize_pos[0] and 
            floor(A_press)*A[1] + floor(B_press)*B[1] == prize_pos[1]):

            all_cost += A_press*A_price + B_press*B_price

    print(all_cost)




if __name__ == '__main__':
    main()