# --- Day 7: Bridge Repair ---

# The Historians take you to a familiar rope bridge over a 
# river in the middle of a jungle. The Chief isn't on this side 
# of the bridge, though; maybe he's on the other side?

# When you go to cross the bridge, you notice a group of engineers 
# trying to repair it. (Apparently, it breaks pretty frequently.) 
# You won't be able to cross until it's fixed.

# You ask how long it'll take; the engineers tell you that it only 
# needs final calibrations, but some young elephants were playing 
# nearby and stole all the operators from their calibration equations! 
# They could finish the calibrations if only someone could determine 
# which test values could possibly be produced by placing any combination 
# of operators into their calibration equations (your puzzle input).

# For example:

# 190: 10 19
# 3267: 81 40 27
# 83: 17 5
# 156: 15 6
# 7290: 6 8 6 15
# 161011: 16 10 13
# 192: 17 8 14
# 21037: 9 7 18 13
# 292: 11 6 16 20

# Each line represents a single equation. The test value appears 
# before the colon on each line; it is your job to determine whether 
# the remaining numbers can be combined with operators to produce 
# the test value.

# Operators are always evaluated left-to-right, not according to 
# precedence rules. Furthermore, numbers in the equations cannot 
# be rearranged. Glancing into the jungle, you can see elephants holding 
# two different types of operators: add (+) and multiply (*).

# Only three of the above equations can be made true by inserting operators:

#     190: 10 19 has only one position that accepts an operator: 
#         between 10 and 19. Choosing + would give 29, 
#         but choosing * would give the test value (10 * 19 = 190).
#     3267: 81 40 27 has two positions for operators. 
#         Of the four possible configurations of the operators, 
#         two cause the right side to match the test value: 
#         81 + 40 * 27 and 81 * 40 + 27 both equal 3267 
#         (when evaluated left-to-right)!
#     292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.

# The engineers just need the total calibration result, which is the 
# sum of the test values from just the equations that could possibly
# be true. In the above example, the sum of the test values for the three 
# equations listed above is 3749.

# Determine which equations could possibly be true. What is their total 
# calibration result?

import numpy as np

# def is_cal(eq):
#     possible_ops = [int.__add__, int.__mul__]

#     sol, vals = eq
    
#     # Each op is an id, to avoid recursion...
#     n_ops = len(vals)-1
#     all_ops = [-1] * n_ops

#     while True:
#         all_ops[level] += 1
#         if all_ops[level] 

possible_ops = [int.__add__, int.__mul__]
def is_cal_rec(sol, vals, vals_idx, acc):

    # Stopping condition
    if vals_idx >= len(vals):
        if sol == acc:
            return sol
        else:
            return -1

    ret = is_cal_rec(sol, vals, vals_idx+1, acc+vals[vals_idx])
    if ret > 0:
        return ret

    ret = is_cal_rec(sol, vals, vals_idx+1, acc*vals[vals_idx])
    return ret



def main():
    inpt = []
    with open('input.txt', 'r') as f_in:
        inpt = f_in.readlines()

        # Remove \n
        inpt = [i[:-1] for i in inpt]

    equations = []
    for i in inpt:
        i = i.split(':')
        sol = int(i[0])
        vals = [int(x) for x in i[1].split(' ')[1:]]
        equations.append((sol, vals))

    # print(equations)

    summ = 0
    for sol, vals in equations:
        cal = is_cal_rec(sol, vals, 1, vals[0])
        if cal > 0:
            summ += cal

    print(summ)


if __name__ == '__main__':
    main()