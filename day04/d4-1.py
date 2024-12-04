# --- Day 4: Ceres Search ---

# "Looks like the Chief's not here. Next!" One of The Historians 
# pulls out a device and pushes the only button on it. After a brief 
# flash, you recognize the interior of the Ceres monitoring station!

# As the search for the Chief continues, a small Elf who lives on the 
# station tugs on your shirt; she'd like to know if you could help her 
# with her word search (your puzzle input). She only has to find one 
# word: XMAS.

# This word search allows words to be horizontal, vertical, diagonal, 
# written backwards, or even overlapping other words. It's a little 
# unusual, though, as you don't merely need to find one instance of 
# XMAS - you need to find all of them. Here are a few ways XMAS might 
# appear, where irrelevant characters have been replaced with .:

# ..X...
# .SAMX.
# .A..A.
# XMAS.S
# .X....

# The actual word search will be full of letters instead. For example:

# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX

# In this word search, XMAS occurs a total of 18 times; here's the same 
# word search again, but where letters not involved in any XMAS have been 
# replaced with .:

# ....XXMAS.
# .SAMXMS...
# ...S..A...
# ..A.A.MS.X
# XMASAMX.MM
# X.....XA.A
# S.S.S.S.SS
# .A.A.A.A.A
# ..M.M.M.MM
# .X.X.XMASX

#   0 1 2 3 4 5 6 7 8 9  
# 0 . . . . X X M A S .
# 1 . S A M X M S . . .
# 2 . . . S . . A . ..
# 3 . . A . A . M S . X
# 4 X M A S A M X . M M
# 5 X . . . . . X A . A
# 6 S . S . S . S . S S
# 7 . A . A . A . A . A
# 8 . . M . M . M . M M
# 9 . X . X . X M A S X

# Take a look at the little Elf's word search. How many times does XMAS appear?

import numpy as np

inpt = []
with open('input.txt', 'r') as f_in:
	inpt = f_in.readlines()
	
	# Remove \n
	inpt = [i[:-1] for i in inpt]


h = len(inpt)
w = len(inpt[0])

mat = np.empty((h,w), dtype=np.int32)

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

xmas = np.array([0,1,2,3])

def xmas_u(i, j):
	# check bounds
	if i < 3:
		return False

	line = mat[i-3:i+1,j]
	line = line[::-1] # reverse
	return all(line == xmas)

def xmas_d(i, j):
	# check bounds
	if i + 3 > h - 1:
		return False

	line = mat[i:i+4,j]
	return all(line == xmas)

def xmas_l(i, j):
	# check bounds
	if j < 3:
		return False

	line = mat[i, j-3:j+1]
	line = line[::-1] # reverse
	return all(line == xmas)

def xmas_r(i, j):
	# check bounds
	if j + 3 > w - 1:
		return False

	line = mat[i, j:j+4]
	return all(line == xmas)

def xmas_ur(i, j):
	# check bounds
	if (i < 3) or (j + 3 > w - 1):
		return False

	line = []
	for x in range(4):
		line.append(mat[i-x, j+x])

	return all(line == xmas)

def xmas_ul(i, j):
	# check bounds
	if (i < 3) or (j < 3):
		return False

	line = []
	for x in range(4):
		line.append(mat[i-x, j-x])

	return all(line == xmas)

def xmas_dr(i, j):
	# check bounds
	if (i + 3 > h - 1) or (j + 3 > w - 1):
		return False

	line = []
	for x in range(4):
		line.append(mat[i+x, j+x])

	return all(line == xmas)

def xmas_dl(i, j):
	# check bounds
	if (i + 3 > h - 1) or (j < 3):
		return False

	line = []
	for x in range(4):
		line.append(mat[i+x, j-x])

	return all(line == xmas)

count = 0
for i in range(h):
	for j in range(w):
		if xmas_u(i, j):
			# print(f'up on {i,j}')
			count += 1
		if xmas_d(i, j):
			# print(f'down on {i,j}')
			count += 1
		if xmas_l(i, j):
			# print(f'left on {i,j}')
			count += 1
		if xmas_r(i, j):
			# print(f'right on {i,j}')
			count += 1

		if xmas_ur(i, j):
			# print(f'ur on {i,j}')
			count += 1
		if xmas_ul(i, j):
			# print(f'ul on {i,j}')
			count += 1
		if xmas_dr(i, j):
			# print(f'dr on {i,j}')
			count += 1
		if xmas_dl(i, j):
			# print(f'dl on {i,j}')
			count += 1

print(f'total: {count}')