'''
Knapsack problem

This solves the multi-dimensional knapsack problem

To run, use the following command:
  python3 knapsack.py

The flag --print-stack will print the calls to solve_knapsack:
  python3 knapsack.py --print-stack
'''

import sys


PRINT_LOOP = False
PRINT_STACK = False


def check_fit(item, remaining):
  for r in range(len(item)):
    if item[r] > remaining[r]:
      return False
  return True


def solve_knapsack(items, capacity):
  '''solve_knapsack

     items is a list of tuples containing: name, value, w1, w2, ...
     capacity is a list of capacities: c1, c2, ...
       The sum of w1 for selected items may not exceed c1
       Similarly, sum of w2 for selected items may not exceed c2, ...

     returns tuple of selected items and value with remaining capacity
  '''
  if PRINT_STACK:
    print(f'Called solve {[i[0] for i in items]} for ' + str(
      capacity if len(capacity) > 1 else capacity[0]))
  selected = []
  # First item is value, rest is remaining capacity
  remaining = [0] + [c for c in capacity]

  if not capacity:
    selected, remaining = ([], ['no capacity provided'])
    if PRINT_STACK:
      print(f'returning {selected} {remaining}')
    return selected, remaining

  if not items:
    selected, remaining = ([], ['no items provided'])
    if PRINT_STACK:
      print(f'returning {selected} {remaining}')
    return selected, remaining

  # Exclude items that don't fit
  items = [i for i in items if check_fit(i[2:], capacity)]
  if not items:
    selected, remaining = ([], ['no items fit'])
    if PRINT_STACK:
      print(f'returning {selected} {remaining}')
    return selected, remaining

  for i in range(len(items)):
    if PRINT_LOOP:
      print(f'Called loop {i} for {items[i]} {[i[0] for i in items]} {selected}')
    does_fit = check_fit(items[i][2:], remaining[1:])

    if does_fit:
      for r in range(len(capacity)):
        remaining[1 + r] -= items[i][2 + r]
      remaining[0] += items[i][1]
      selected.append(items[i][0])
      continue

    # Does not fit
    if not selected:
      # if there is nothing selected, skip item
      continue

    if i == 1 and items[0][1] >= items[i][1]:
      # Does not fit and selected item has higher value
      continue

    # Find max of first i items with reduced capacity
    if PRINT_LOOP:
      print(f'Checking {items[i]} against {selected}')
    too_big = False
    new_capacity = [0] * len(capacity)
    for c in range(len(capacity)):
      new_capacity[c] = capacity[c] - items[i][2 + c]
      if new_capacity[c] < 0:
        # item i is too big, skip it
        too_big = True
        break
    if too_big:
      continue

    new_selected, new_remaining = solve_knapsack(items[:i], new_capacity)
    if new_selected and new_remaining[0] + items[i][1] > remaining[0]:
      # including item i gives more value
      new_selected.append(items[i][0])
      new_remaining[0] += items[i][1]
      remaining = new_remaining
      selected = new_selected

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
  if type(capacity).__name__ not in ['list', 'tuple']:
    return ([], ['capacity must be a list of int'])
  capacity_type = list(set([type(c).__name__ for c in capacity]))
  if len(capacity_type) != 1 or capacity_type[0] != 'int':
    return ([], ['capacity must be a list of int'])
  num_weights = len(capacity)
  if num_weights <= 0:
    return ([], ['there must be at least one weight'])
  if min(capacity) <= 0:
    return ([], ['all weights must be +ve'])

  if not items:
    return ([], ['must have at least one item'])
  if len(set([i[0] for i in items])) != len(items):
    return ([], ['item names are not unique'])
  item_length = [len(i) for i in items]
  if (min(item_length) != num_weights + 2) or (
        max(item_length) != num_weights + 2):
    return ([], [f'items must have name, value and {num_weights} weights'])
  for item in items:
    item_type = list(set([type(i).__name__ for i in item[1:]]))
    if len(item_type) != 1 or item_type[0] != 'int':
      return ([], ['all item values and weights must be int'])
  if min([i[1] for i in items]) <= 0:
    return ([], ['all item values must be > 0'])
  if min([min(i[2:]) for i in items]) < 0:
    return ([], ['all item weights must be >= 0'])

  # Use greedy algorithm - sort by max value and then by least weight
  sorted_items = sorted(items, key=lambda x : (-x[1], sum(x[2:])))
  return solve_knapsack(sorted_items, capacity)


def print_knapsack(sack):
  return f'value = {sack[1][0]}, items = ' + str(
    sorted(sack[0]))


if __name__ == '__main__':
  if '--print-loop' in sys.argv:
    PRINT_LOOP = True
  if '--print-stack' in sys.argv:
    PRINT_STACK = True

  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 1, 1), ('A', 6, 2), ('C', 10, 3), ('D', 16, 5)], (7,))))
  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 3, 3), ('B', 5, 5), ('C', 3, 3)], (6,))))
  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 1, 1), ('B', 6, 2), ('C', 10, 3), ('D', 16, 5)], (7,))))
  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 1, 1), ('B', 6, 2), ('C', 10, 3), ('D', 16, 5)], (6,))))
  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 1, 1, 3), ('B', 6, 2, 2), ('C', 10, 3, 5), ('D', 16, 5, 4)],
    (7, 7))))

  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 2, 1, 20),
     ('B', 2, 1, 25),
     ('C', 3, 2, 30),
     ('D', 2, 3, 35),
     ('E', 5, 3, 40),
     ('F', 6, 3, 40),
     ('G', 2, 3, 45),
     ('H', 5, 3, 45),
     ('I', 7, 4, 50)],
    (20, 245)
    )))

  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 10, 2, 512, 10),
     ('B', 20, 4, 256, 15),
     ('C', 30, 8, 128, 20),
     ('D', 40, 16, 64, 25),
     ('E', 50, 32, 32, 30),
     ('F', 60, 64, 16, 35),
     ('G', 70, 128, 8, 40),
     ('H', 80, 140, 4, 45),
     ('I', 90, 160, 2, 50),
     ('J', 100, 180, 1, 55)],
    (300, 300, 100)
    )))


