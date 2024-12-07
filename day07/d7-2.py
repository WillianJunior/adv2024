# --- Part Two ---

# The engineers seem concerned; the total calibration result you gave
# them is nowhere close to being within safety tolerances. Just then,
# you spot your mistake: some well-hidden elephants are holding a third
# type of operator.

# The concatenation operator (||) combines the digits from its left and
# right inputs into a single number. For example, 12 || 345 would become
# 12345. All operators are still evaluated left-to-right.

# Now, apart from the three equations that could be made true using only
# addition and multiplication, the above example has three more equations
# that can be made true by inserting operators:

#     156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
#     7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
#     192: 17 8 14 can be made true using 17 || 8 + 14.

# Adding up all six test values (the three that could be made before using
# only + and * plus the new three that can now be made by also using ||)
# produces the new total calibration result of 11387.

# Using your new knowledge of elephant hiding spots, determine which equations
# could possibly be true. What is their total calibration result?

import numpy as np
from numba import njit


@njit
def is_cal_rec(sol, vals, vals_idx, acc):

    # Stopping condition
    if vals_idx >= len(vals):
        if sol == acc:
            return sol
        else:
            return -1

    # Add option
    ret = is_cal_rec(sol, vals, vals_idx + 1, acc + vals[vals_idx])
    if ret > 0:
        return ret

    # Mul option
    ret = is_cal_rec(sol, vals, vals_idx + 1, acc * vals[vals_idx])
    if ret > 0:
        return ret

    # Concat option
    n = 1
    base = vals[vals_idx]
    while base / 10 >= 1:
        base /= 10
        n += 1

    conc = acc * (10**n) + vals[vals_idx]
    ret = is_cal_rec(sol, vals, vals_idx + 1, conc)
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

    summ = np.int64(0)
    for sol, vals in equations:
        cal = is_cal_rec(sol, np.array(vals), 1, vals[0])
        if cal > 0:
            summ += cal

    print(summ)


if __name__ == '__main__':
    main()