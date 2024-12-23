# --- Day 23: LAN Party ---

# As The Historians wander around a secure area at Easter Bunny
# HQ, you come across posters for a LAN party scheduled for today!
# Maybe you can find it; you connect to a nearby datalink port and
# download a map of the local network (your puzzle input).

# The network map provides a list of every connection between two
# computers. For example:

# kh-tc
# qp-kh
# de-cg
# ka-co
# yn-aq
# qp-ub
# cg-tb
# vc-aq
# tb-ka
# wh-tc
# yn-cg
# kh-ub
# ta-co
# de-co
# tc-td
# tb-wq
# wh-td
# ta-ka
# td-qp
# aq-cg
# wq-ub
# ub-vc
# de-ta
# wq-aq
# wq-vc
# wh-yn
# ka-de
# kh-ta
# co-tc
# wh-qp
# tb-vc
# td-yn

# Each line of text in the network map represents a single
# connection; the line kh-tc represents a connection between the
# computer named kh and the computer named tc. Connections aren't
# directional; tc-kh would mean exactly the same thing.

# LAN parties typically involve multiplayer games, so maybe you can
# locate it by finding groups of connected computers. Start by
# looking for sets of three computers where each computer in the
# set is connected to the other two computers.

# In this example, there are 12 such sets of three inter-connected
# computers:

# aq,cg,yn
# aq,vc,wq
# co,de,ka
# co,de,ta
# co,ka,ta
# de,ka,ta
# kh,qp,ub
# qp,td,wh
# tb,vc,wq
# tc,td,wh
# td,wh,yn
# ub,vc,wq

# If the Chief Historian is here, and he's at the LAN party, it
# would be best to know that right away. You're pretty sure his
# computer's name starts with t, so consider only sets of three
# computers where at least one computer's name starts with t. That
# narrows the list down to 7 sets of three inter-connected computers:

# co,de,ta
# co,ka,ta
# de,ka,ta
# qp,td,wh
# tb,vc,wq
# tc,td,wh
# td,wh,yn

# Find all the sets of three inter-connected computers. How many
# contain at least one computer with a name that starts with t?

import numpy as np
from tqdm import tqdm
from multiprocessing import Pool
from time import time
from numba import jit
from collections import defaultdict
from math import ceil, floor, prod
import sys
from heapq import heapify, heappush, heappop

np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=np.inf)


def main():
    inpt = []
    with open('input.txt', 'r') as f_in:
        inpt = f_in.readlines()

        # Remove \n
        inpt = [i[:-1] for i in inpt]

    edges_dict = defaultdict(lambda: [])
    # hist_edges = defaultdict(lambda: [])

    nodes = set()
    for line in inpt:
        pc1, pc2 = line.split('-')
        edges_dict[pc1].append(pc2)
        edges_dict[pc2].append(pc1)
        nodes.add(pc1)
        nodes.add(pc2)

    nodes = sorted(nodes)
    print(nodes)
    edge_map = np.full((len(nodes), len(nodes)), False)

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            n1 = nodes[i]
            n2 = nodes[j]
            if n1 in edges_dict[n2]:
                edge_map[i,j] = True

    print(edge_map)
    lans = sum(edge_map)
    print(sum(lans)/len(lans))
    print(lans)

    # print(np.argmax(lans))
    # nodes = np.array(nodes)
    # print(sorted(nodes[edge_map[np.argmax(lans)]]))


    # global largest_set_len
    # global largest_set

    # largest_set_len = 0
    # largest_set = None

    # traverse_edges = list(zip(edges_dict.keys(), edges_dict.values()))

    # print(traverse_edges)

    # def full_conn(init_set, new_node):
    #     for n in init_set:
    #         if new_node not in edges_dict[n]:
    #             return False

    #     return True

    # global p_bar
    # p_bar = tqdm(range(len(edges_dict)))

    # full_conn

    # def get_largest_set(edges, cur_set, level=0):
    #     global largest_set_len
    #     global largest_set

    #     # print(edges, cur_set)

    #     for pc in edges_dict:

    #         if pc in cur_set:
    #             continue

    #         if level == 0:
    #             p_bar.update(1)
    #         neigh = edges_dict[pc]
    #         # print(f'{level*"  "}trying {pc} with {neigh}')
    #         if full_conn(cur_set, pc):
    #             # print(f'{pc} is full_conn with {cur_set}')
    #             new_set = cur_set + [pc]

    #             get_largest_set(neigh, new_set, level + 1)

    #     if len(cur_set) > largest_set_len:
    #         largest_set_len = len(cur_set)
    #         largest_set = cur_set
    #         print(f'new largest_set: {sorted(largest_set)}')

    # get_largest_set(edges_dict.keys(), [])

    # print(largest_set_len)
    # print(largest_set)


if __name__ == '__main__':
    main()
