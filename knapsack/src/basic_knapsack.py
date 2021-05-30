'''
Basic Knapsack problem

This solves the basic knapsack problem

To run, use the following command:
  python3 basic_knapsack.py

The flag --print-stack will print the calls to solve_knapsack:
  python3 basic_knapsack.py --print-stack
'''

import sys


PRINT_LOOP = False
PRINT_STACK = False


def find_replace_items(new_item, selected_items, capacity):
  # Need to find items that can be replaced by new_item
  # sum values must be less than new_item
  # maximize weight removed to replace new_item
  max_weight = capacity - new_item[2]
  large_items = [s for s in selected_items if s[2] > max_weight]
  max_value = new_item[1] - 1 - sum([s[1] for s in large_items])
  if max_value <= 0:
    return [] if max_value else large_items
  mod_items = [[s[0], s[2], s[1]] for s in selected_items if s[2] <= max_weight]
  if not mod_items:
    return large_items
  replace_items, _ = solve_knapsack(mod_items, max_value)
  return large_items + [s for s in selected_items if s[0] in replace_items]


def solve_knapsack(items, capacity):
  '''solve_knapsack

     items is a list of tuples containing: name, value, weight
     capacity is the max total weight
       The sum of weight for selected items may not exceed capacity

     returns tuple of selected items and value with remaining capacity
  '''
  if PRINT_STACK:
    print(f'Called solve {[i[0] for i in items]} for {capacity}')

  if not items:
    selected, remaining = ([], ['no items provided'])
    if PRINT_STACK:
      print(f'returning {selected} {remaining}')
    return selected, remaining

  # Exclude items that don't fit
  items = [i for i in items if i[2] <= capacity]
  if not items:
    selected, remaining = ([], ['no items fit'])
    if PRINT_STACK:
      print(f'returning {selected} {remaining}')
    return selected, remaining

  # Use greedy algorithm - sort by least weight and then by max value
  items = sorted(items, key=lambda x : (x[2], -x[1]))

  selected = []
  selected_items = []
  # First item is value, second is remaining capacity
  remaining = [0, capacity]

  replace = True
  while replace:
    replace = False
    for i in range(len(items)):
      if PRINT_LOOP:
        print(f'Called loop {i} for {items[i]} {[i[0] for i in items]} {selected}')

      if items[i][0] in selected:
        continue
      if items[i][2] <= remaining[1]:
        remaining[1] -= items[i][2]
        remaining[0] += items[i][1]
        selected.append(items[i][0])
        selected_items.append(items[i])
        continue

      # Does not fit
      if not selected:
        # if there is nothing selected, skip item
        continue

      if len(selected_items) == 1 and selected_items[0][1] >= items[i][1]:
        # Does not fit and selected item has higher value
        continue

      # Find items to replace
      if PRINT_LOOP:
        print(f'Checking {items[i]} against {selected}')
      replace_items = find_replace_items(items[i], selected_items, capacity)
      replace_weight = sum([s[2] for s in replace_items])
      if replace_items and items[i][2] <= replace_weight + remaining[1]:
        replace = True
        remaining[1] -= items[i][2]
        remaining[0] += items[i][1]
        for r in replace_items:
          remaining[1] += r[2]
          remaining[0] -= r[1]
        selected = [items[i][0]] + list(
          set(selected) - set([r[0] for r in replace_items]))
        selected_items = [items[i]] + [
          s for s in selected_items if s[0] in selected]

  if PRINT_STACK:
    print(f'returning {selected} {remaining}')
  return (selected, remaining)


def validate_and_solve_knapsack(items, capacity):
  '''validate_and_solve_knapsack
     validates parameters and calls solve_knapsack

     items is a list of tuples containing: name, value, w1, w2, ...
     capacity is a list of capacities: c1, c2, ...
       The sum of w1 for selected items may not exceed c1
       Similarly, sum of w2 for selected items may not exceed c2, ...

     returns tuple of selected items and value with remaining capacity
  '''
  if type(capacity).__name__ != 'int' or capacity <= 0:
    return ([], ['capacity must be a positive integer'])

  if not items:
    return ([], ['must have at least one item'])
  if len(set([i[0] for i in items])) != len(items):
    return ([], ['item names are not unique'])
  item_length = [len(i) for i in items]
  if (min(item_length) != 3) or (max(item_length) != 3):
    return ([], ['items must have name, value and weight'])
  for item in items:
    item_type = list(set([type(i).__name__ for i in item[1:]]))
    if len(item_type) != 1 or item_type[0] != 'int':
      return ([], ['all item values and weights must be int'])
  if min([i[1] for i in items]) <= 0:
    return ([], ['all item values must be > 0'])
  if min([i[2] for i in items]) < 0:
    return ([], ['all item weights must be >= 0'])

  return solve_knapsack(items, capacity)


def print_knapsack(sack):
  return f'value = {sack[1][0]}, items = ' + str(
    sorted(sack[0]))


if __name__ == '__main__':
  if '--print-loop' in sys.argv:
    PRINT_LOOP = True
  if '--print-stack' in sys.argv:
    PRINT_STACK = True

  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 1, 1), ('A', 6, 2), ('C', 10, 3), ('D', 16, 5)], 7)))
  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 3, 3), ('B', 5, 5), ('C', 3, 3)], 6)))
  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 1, 1), ('B', 6, 2), ('C', 10, 3), ('D', 16, 5)], 7)))
  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 1, 1), ('B', 6, 2), ('C', 10, 3), ('D', 16, 5)], 6)))
  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 1, 3), ('B', 6, 2), ('C', 10, 5), ('D', 16, 4)], 7)))


