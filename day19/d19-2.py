# --- Part Two ---

# The staff don't really like some of the towel arrangements 
# you came up with. To avoid an endless cycle of towel rearrangement, 
# maybe you should just give them every possible option.

# Here are all of the different ways the above example's designs 
# can be made:

# brwrr can be made in two different ways: b, r, wr, r or br, wr, r.

# bggr can only be made with b, g, g, and r.

# gbbr can be made 4 different ways:

#     g, b, b, r
#     g, b, br
#     gb, b, r
#     gb, br

# rrbgbr can be made 6 different ways:

#     r, r, b, g, b, r
#     r, r, b, g, br
#     r, r, b, gb, r
#     r, rb, g, b, r
#     r, rb, g, br
#     r, rb, gb, r

# bwurrg can only be made with bwu, r, r, and g.

# brgr can be made in two different ways: b, r, g, r or br, g, r.

# ubwu and bbrgwb are still impossible.

# Adding up all of the ways the towels in this example could be arranged 
# into the desired designs yields 16 (2 + 1 + 4 + 6 + 1 + 2).

# They'll let you into the onsen as soon as you have the list. What do 
# you get if you add up the number of different ways you could make 
# each design?



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

    find_comb_cache = dict()

    def find_comb(tree, towel, level=0):
        cond = False
        end_i = 1

        if towel in find_comb_cache:
            return find_comb_cache[towel]

        all_combs = 0

        if cond: print(f'{level*'  '}find_comb({towel})')

        if len(towel) == 0:
            if cond: print(f'{level*'  '}len 0 OK')
            return all_combs+1

        while end_i <= len(towel):
            has_pattern = navigate_tree(tree, towel[:end_i])

            # Found a pattern in the current range
            if has_pattern:
                if cond: print(f'{level*'  '}has pattern {towel[:end_i]}')

                # Try to find a pattern with the remaining towel
                new_combs = find_comb(tree, towel[end_i:], level+1)
                find_comb_cache[towel[end_i:]] = new_combs
                all_combs += new_combs
                if cond: print(f'{level*'  '}{towel[end_i:]} updated: {all_combs}')

            # Pattern not possible, increment end place
            end_i += 1

        return all_combs


    count = 0
    for towel in towels_list:
        combs = find_comb(patterns_tree, towel)
        count += combs
        print(f'{towel}: {combs}')

    print(count)


if __name__ == '__main__':
    main()