# --- Day 4: Ceres Search ---

# --- Part Two ---

# The Elf looks quizzically at you. Did you misunderstand
# the assignment?

# Looking for the instructions, you flip over the word search
# to find that this isn't actually an XMAS puzzle; it's an X-MAS
# puzzle in which you're supposed to find two MAS in the shape of
# an X. One way to achieve that is like this:

# M.S
# .A.
# M.S

# Irrelevant characters have again been replaced with . in
# the above diagram. Within the X, each MAS can be written
# forwards or backwards.

# Here's the same example from before, but this time all of the
# X-MASes have been kept instead:

# .M.S......
# ..A..MSMS.
# .M.S.MAA..
# ..A.ASMSM.
# .M.S.M....
# ..........
# S.S.S.S.S.
# .A.A.A.A..
# M.M.M.M.M.
# ..........


#   0 1 2 3 4 5 6 7 8 9  
# 0 . M . S . . . . . .
# 1 . . A . . M S M S .
# 2 . M . S . M A A . .
# 3 . . A . A S M S M .
# 4 . M . S . M . . . .
# 5 . . . . . . . . . .
# 6 S . S . S . S . S .
# 7 . A . A . A . A . .
# 8 M . M . M . M . M .
# 9 . . . . . . . . . .

# In this example, an X-MAS appears 9 times.

# Flip the word search from the instructions back over to the word
# search side and try again. How many times does an X-MAS appear?

import numpy as np

inpt = []
with open('input.txt', 'r') as f_in:
    inpt = f_in.readlines()

    # Remove \n
    inpt = [i[:-1] for i in inpt]

h = len(inpt)
w = len(inpt[0])

mat = np.empty((h, w), dtype=np.int32)

for i, line in enumerate(inpt):
    for j, c in enumerate(line):
        if c == 'X':
            mat[i, j] = 0
        elif c == 'M':
            mat[i, j] = 1
        elif c == 'A':
            mat[i, j] = 2
        elif c == 'S':
            mat[i, j] = 3
        else:
            mat[i, j] = -9

xmas = np.array([1, 2, 3])
xmas_len_1 = len(xmas) - 1
xmas_len = len(xmas)


def xmas_ur(i, j):
    line = []
    for x in range(xmas_len):
        line.append(mat[i - x + (xmas_len_1 // 2), j + x - (xmas_len_1 // 2)])

    return all(line == xmas)


def xmas_ul(i, j):
    line = []
    for x in range(xmas_len):
        line.append(mat[i - x + (xmas_len_1 // 2), j - x + (xmas_len_1 // 2)])

    return all(line == xmas)


def xmas_dr(i, j):
    line = []
    for x in range(xmas_len):
        line.append(mat[i + x - (xmas_len_1 // 2), j + x - (xmas_len_1 // 2)])

    return all(line == xmas)


def xmas_dl(i, j):
    line = []
    for x in range(xmas_len):
        line.append(mat[i + x - (xmas_len_1 // 2), j - x + (xmas_len_1 // 2)])

    return all(line == xmas)


count = 0
for i in range(h):
    for j in range(w):
        # check bounds
        if (i < xmas_len_1 // 2) or (i > h - 1 - xmas_len_1 // 2) or (
                j < xmas_len_1 // 2) or (j > w - 1 - xmas_len_1 // 2):
            continue
        
        if xmas_ur(i, j) and (xmas_dr(i,j) or xmas_ul(i,j)):
            count += 1
        if xmas_dl(i, j) and (xmas_dr(i,j) or xmas_ul(i,j)):
            count += 1

print(f'total: {count}')