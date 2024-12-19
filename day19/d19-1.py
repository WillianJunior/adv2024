# --- Day 19: Linen Layout ---

# Today, The Historians take you up to the hot springs on Gear 
# Island! Very suspiciously, absolutely nothing goes wrong as 
# they begin their careful search of the vast field of helixes.

# Could this finally be your chance to visit the onsen next door? 
# Only one way to find out.

# After a brief conversation with the reception staff at the onsen 
# front desk, you discover that you don't have the right kind of money 
# to pay the admission fee. However, before you can leave, the staff 
# get your attention. Apparently, they've heard about how you helped 
# at the hot springs, and they're willing to make a deal: if you can 
# simply help them arrange their towels, they'll let you in for free!

# Every towel at this onsen is marked with a pattern of colored 
# stripes. There are only a few patterns, but for any particular 
# pattern, the staff can get you as many towels with that pattern 
# as you need. Each stripe can be white (w), blue (u), black (b), 
# red (r), or green (g). So, a towel with the pattern ggr would 
# have a green stripe, a green stripe, and then a red stripe, in 
# that order. (You can't reverse a pattern by flipping a towel 
#     upside-down, as that would cause the onsen logo to face the 
#     wrong way.)

# The Official Onsen Branding Expert has produced a list of 
# designs - each a long sequence of stripe colors - that they would 
# like to be able to display. You can use any towels you want, but 
# all of the towels' stripes must exactly match the desired design. 
# So, to display the design rgrgr, you could use two rg towels and 
# then an r towel, an rgr towel and then a gr towel, or even a single 
# massive rgrgr towel (assuming such towel patterns were actually 
#     available).

# To start, collect together all of the available towel patterns and 
# the list of desired designs (your puzzle input). For example:

# r, wr, b, g, bwu, rb, gb, br

# brwrr
# bggr
# gbbr
# rrbgbr
# ubwu
# bwurrg
# brgr
# bbrgwb

# The first line indicates the available towel patterns; in this 
# example, the onsen has unlimited towels with a single red stripe (r), 
# unlimited towels with a white stripe and then a red stripe (wr), 
# and so on.

# After the blank line, the remaining lines each describe a design the 
# onsen would like to be able to display. In this example, the first 
# design (brwrr) indicates that the onsen would like to be able to 
# display a black stripe, a red stripe, a white stripe, and then two 
# red stripes, in that order.

# Not all designs will be possible with the available towels. In the 
# above example, the designs are possible or impossible as follows:

#     brwrr can be made with a br towel, then a wr towel, 
#         and then finally an r towel.
#     bggr can be made with a b towel, two g towels, and then an r towel.
#     gbbr can be made with a gb towel and then a br towel.
#     rrbgbr can be made with r, rb, g, and br.
#     ubwu is impossible.
#     bwurrg can be made with bwu, r, r, and g.
#     brgr can be made with br, g, and r.
#     bbrgwb is impossible.

# In this example, 6 of the eight designs are possible with the 
# available towel patterns.

# To get into the onsen as soon as possible, consult your list of towel 
# patterns and desired designs carefully. How many designs are possible?


import numpy as np
from tqdm import tqdm
from multiprocessing import Pool
from time import time
from numba import jit
from collections import defaultdict
from math import ceil, floor, prod
import sys
from heapq import heapify, heappush, heappop

def flatten(xss):
    return [x for xs in xss for x in xs]

def s_pop(s):
    return s[0], s[1:]

class Tree:
    def __init__(self):
        # Dict key: cur_color, val: Tree node
        self.children = dict()

        # Single char
        self.cur_color = None
        
        # Full pattern of chars. If none, then this is
        # not a pattern, just a node in the tree
        self.pattern = None

    def add_pattern(t, pattern, acc=''):
        # print(f'add: {pattern}')
        c, pattern = s_pop(pattern)
        acc += c
        next_node = t.children.get(c, None)

        # New node
        if next_node is None:
            # print('new node')
            next_node = Tree()
            next_node.cur_color = c
            t.children[c] = next_node

        if len(pattern) == 0:
            # print('full pattern')
            # This is a full pattern
            next_node.pattern = acc
        else:
            # print('pattern not done')
            Tree.add_pattern(next_node, pattern, acc)

    def rec_print(self, header='', from_last=False):
        ret = ''

        # Fix last L-shaped edge
        if from_last:
            end_curve = '\u2514' # L
        else:
            end_curve='\u251C' # T

        # Check for root node
        if self.cur_color is not None:
            node_name = self.cur_color
            if self.pattern is not None:
                # Is leaf node
                node_name += ' [' + self.pattern + ']'
            node_name = end_curve + '\u2500' + ' ' + node_name
        else:
            node_name = 'X'

        # Add current node
        ret += header + node_name + '\n'

        # Prep header for children nodes
        next_header = header
        if node_name != 'X':
            if not from_last:
                next_header += '\u2502' + '  '
            else:
                next_header += '   '
        from_last = False

        # Print children nodes
        for i, (c, child) in enumerate(self.children.items()):
            if i == len(self.children)-1:
                # Current child is last node of parent
                from_last = True
            ret += child.rec_print(next_header, from_last)

        return ret

    def __str__(self):
        
        return self.rec_print()

    def __repr__(self):
        return self.__str__()


def main():
    inpt = []
    with open('input.txt', 'r') as f_in:
        inpt = f_in.readlines()

        # Remove \n
        inpt = [i[:-1] for i in inpt]

    patterns = inpt[0].split(',')
    patterns = [p.strip() for p in patterns]
    print(patterns)

    towels_list = inpt[2:]
    print(towels_list)

    patterns_tree = Tree()
    for p in patterns:
        Tree.add_pattern(patterns_tree, p)
    print(patterns_tree)

    def navigate_tree(tree, pattern):
        '''
        Returns true if pattern is in Tree
        '''

        cond = False

        # Empty pattern is success
        if len(pattern) == 0:
            if tree.pattern is not None:
                if cond: print(f'[NT] len 0 for {tree.pattern}')
                return True
            else:
                if cond: print(f'[NT] len 0 for leaf node')
                return False

        # Get first  char
        c, remaining_pattern = s_pop(pattern)
        if cond: print(f'[NT] trying {c}:{remaining_pattern}')

        # Current tree node does not have the char
        if not tree.children.get(c, False):
            if cond: print(f'[NT] {c} not in {tree.children.keys()}')
            return False

        # Follow the tree
        return navigate_tree(tree.children[c], remaining_pattern)

    def find_comb(tree, towel, level=0):
        cond = False
        end_i = 1

        if cond: print(f'{level*'  '}find_comb({towel})')

        if len(towel) == 0:
            if cond: print(f'{level*'  '}len 0 OK')
            return True

        while end_i <= len(towel):
            has_pattern = navigate_tree(tree, towel[:end_i])

            # Found a pattern in the current range
            if has_pattern:
                if cond: print(f'{level*'  '}has pattern {towel[:end_i]}')

                # Try to find a pattern with the remaining towel
                if find_comb(tree, towel[end_i:], level+1):
                    if cond: print(f'{level*'  '}{towel[end_i:]} is OK')
                    return True

            # Pattern not possible, increment end place
            end_i += 1

        # Could not find a pattern
        return False


    count = 0
    for towel in towels_list:
        has_comb = find_comb(patterns_tree, towel)
        print(f'{towel}: {has_comb}')
        if has_comb: count += 1
        # print()

    print(count)


if __name__ == '__main__':
    main()