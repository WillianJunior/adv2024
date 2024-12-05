# --- Day 5: Print Queue ---

# --- Part Two ---

# While the Elves get to work printing the correctly-ordered 
# updates, you have a little time to fix the rest of them.

# For each of the incorrectly-ordered updates, use the page 
# ordering rules to put the page numbers in the right order. 
# For the above example, here are the three incorrectly-ordered 
# updates and their correct orderings:

#     75,97,47,61,53 becomes 97,75,47,61,53.
#     61,13,29 becomes 61,29,13.
#     97,13,75,29,47 becomes 97,75,47,29,13.

# After taking only the incorrectly-ordered updates and ordering 
# them correctly, their middle page numbers are 47, 29, and 47. 
# Adding these together produces 123.

# Find the updates which are not in the correct order. What do you 
# get if you add up the middle page numbers after correctly ordering 
# just those updates?

from collections import defaultdict

inpt = []
with open('input.txt', 'r') as f_in:
    inpt = f_in.readlines()
    
    # Remove \n
    inpt = [i[:-1] for i in inpt]

p_ord_list = []
p_prods = []
is_p_ord = True
for i in inpt:
    if i == '':
        is_p_ord = False
        continue

    if is_p_ord:
        p_ord_list.append(i)
    else:
        p_prods.append(i)

# # p_prods is INVERTED to preserve 'before' rule
# p_prods = [p.split(',')[::-1] for p in p_prods]

p_prods = [p.split(',') for p in p_prods]
p_prods = [[int(pp) for pp in p] for p in p_prods]


p_ord_list = [o.split('|') for o in p_ord_list]
p_ord_list = [[int(oo) for oo in o] for o in p_ord_list]
# print(p_ord_list)

p_ord = defaultdict(lambda: [])
for [a, b] in p_ord_list:
    p_ord[a].append(b)
# print(p_ord)


summ = 0

for p_prod in p_prods:
    is_rule_broken = True
    is_rule_broken_once = False

    while is_rule_broken:
        is_rule_broken = False
        # print(f'trying {p_prod}')
        for i in range(len(p_prod)):
            cur = p_prod[i]
            prev = p_prod[:i]
            rem = p_prod[i+1:]

            for p_idx, p in enumerate(prev):
                rules = p_ord[cur]
                if p in rules:
                    # print(f'{cur} breaking rule with {p}')
                    is_rule_broken = True
                    is_rule_broken_once = True

                    # Fix p_prod
                    # print(p_prod)
                    p_prod = prev[:p_idx] + [cur] + prev[p_idx+1:] + [p]  + rem
                    # print(f'fixed to: {p_prod}')
                    break

    # Only pages which were fixed are counted
    if is_rule_broken_once:
      summ += p_prod[len(p_prod)//2]

print(summ)

