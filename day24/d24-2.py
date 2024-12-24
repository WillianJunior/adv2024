import numpy as np
from tqdm import tqdm
from multiprocessing import Pool
from time import time
from numba import jit
from collections import defaultdict
from math import ceil, floor, prod
import sys
from heapq import heapify, heappush, heappop


def main():
    inpt = []
    with open('input.txt', 'r') as f_in:
        inpt = f_in.readlines()

        # Remove \n
        inpt = [i[:-1] for i in inpt]

    AND = 'AND'
    OR = 'OR'
    XOR = 'XOR'

    ops = {AND: lambda lhs, rhs: lhs & rhs, 
           OR: lambda lhs, rhs: lhs | rhs, 
           XOR: lambda lhs, rhs: lhs ^ rhs, 
          }

    variables = dict()

    for i in range(len(inpt)):
        line = inpt[i]
        if len(line) == 0:
            break

        var, val = line.split(': ')
        variables[var] = int(val)

    all_ops = []
    for i in range(i+1, len(inpt)):
        line = inpt[i].replace('-> ', '')
        lhs, op, rhs, out = line.split(' ')
        all_ops.append((lhs, op, rhs, out))
    
    while len(all_ops) > 0:
        lhs, op, rhs, out = all_ops.pop(0)
        # print(f'trying {lhs, op, rhs, out}')
        if lhs not in variables or rhs not in variables:
            all_ops.append((lhs, op, rhs, out))
            # print('not ready')
            continue
        variables[out] = ops[op](variables[lhs], variables[rhs])

    print(sorted(variables.items()))
    result = []
    x = []
    y = []
    for k in variables.keys():
        if k.startswith('z'):
            result.append(k)
        if k.startswith('x'):
            x.append(k)
        if k.startswith('y'):
            y.append(k)

    result.sort(reverse=True)
    # print(sorted(result, reverse=True))
    
    print('x  :  ' + ''.join([str(variables[r]) for r in x]))
    print('y  :  ' + ''.join([str(variables[r]) for r in y]))
    print('out: ' + ''.join([str(variables[r]) for r in result]))
    

    print(int(''.join([str(variables[r]) for r in result]), base=2))




if __name__ == '__main__':
    main()