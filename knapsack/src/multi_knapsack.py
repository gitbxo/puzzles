'''
Multiple Knapsack problem

This solves the multiple knapsack problem with multiple dimensions
Here we want to maximize the total value for all items
Each item can be in only one knapsack
Each knapsack has limits for how much weight and volume it can carry

To run, use the following command:
  python3 multi_knapsack.py

The flag --print-stack will print the calls to solve_knapsack:
  python3 multi_knapsack.py --print-stack
'''

import sys


PRINT_LOOP = False
PRINT_STACK = False


def check_fit(item, remaining):
  for i in range(len(remaining)):
    check = True
    for r in range(len(item)):
      if item[r] > remaining[i][r]:
        check = False
        break
    if check:
      return i
  return -1


def solve_knapsack(items, capacity):
  '''solve_knapsack

     items is a list of tuples containing: name, value, w1, w2, ...
     capacity is a list of capacities for each knapsack: c1, c2, ...
       The sum of w1 for selected items may not exceed c1
       Similarly, sum of w2 for selected items may not exceed c2, ...
       Items may have a required flag after the name
       If True, only solutions containing the item will be
       considered, e.g. must carry tent to camp.
       Required values beginning with 't' or 'T' are considered True

     returns tuple of selected items and value with remaining capacity
  '''
  if PRINT_STACK:
    print(f'Called solve {[i[0] for i in items]} for {capacity}')
  selected = []
  # First item is value, rest is remaining capacity
  remaining = [0] + [[c for c in k] for k in capacity]
  lookup = {}

  for i in range(len(items)):
    if PRINT_LOOP:
      print(f'Called loop {i} for {items[i]} {[i[0] for i in items]} {selected}')
    required_i = len(items[i]) > 2 + len(capacity[0]) and (
      str(items[i][1]).lower().startswith('t'))
    item_i = (
      items[i][:1] + items[i][-len(capacity[0])-1:]
      if len(items[i]) > 2 + len(capacity[0])
      else items[i])
    first_fit = check_fit(item_i[2:], remaining[1:])
    lookup[item_i[0]] = items[i]

    # Does not fit
    if first_fit < 0 and not selected:
      # if there is nothing selected, skip item
      if required_i:
        # no solution when item i is required, but does not fit
        if PRINT_STACK:
          print(f'cannot fit items {[item_i[0]]} i {i} {first_fit}')
        return ([], ['cannot fit items ' + str([item_i[0]])])
      continue

    max_remaining = []
    max_selected = []
    if first_fit >= 0:
      max_selected = [s for s in selected] + [(first_fit, item_i[0])]
      max_remaining = [remaining[0] + item_i[1]] + [
        [c for c in s] for s in remaining[1:]]
      for r in range(len(capacity[first_fit])):
        max_remaining[first_fit + 1][r] -= item_i[2 + r]

      remaining = max_remaining
      selected = max_selected
      continue

    # Find max of first i items with reduced capacity
    first_fit = check_fit(item_i[2:], capacity)
    while first_fit >= 0:
      if PRINT_LOOP:
        print(f'Called first_fit loop {first_fit} for {items[i]} {max_selected}')
      too_big = False
      new_capacity = [[c for c in k] for k in capacity]
      for c in range(len(capacity[first_fit])):
        new_capacity[first_fit][c] -= item_i[2 + c]
        if new_capacity[first_fit][c] < 0:
          # item i is too big, skip it
          too_big = True
          break

      new_selected, new_remaining = ([], [])
      if not too_big:
        if selected:
          new_remaining = [remaining[0]] + [
            [c for c in s] for s in remaining[1:]]
          new_selected = [s for s in selected]
          for r in range(len(capacity[first_fit])):
            new_remaining[first_fit + 1][r] -= item_i[2 + r]
            if 0 > new_remaining[first_fit + 1][r]:
              new_selected = []

        if not new_selected:
          new_selected, new_remaining = solve_knapsack(items[:i], new_capacity)

      if too_big or len(new_remaining) < 1 + len(capacity):
        next_fit = -1 if first_fit + 1 >= len(capacity) else check_fit(
           item_i[2:], capacity[first_fit+1:])
        if PRINT_LOOP:
          print(f'New first_fit loop {first_fit} {next_fit} {items[i]} {new_selected} {new_remaining}')
        if next_fit < 0:
          # item i is too big, skip it
          break
        first_fit += next_fit + 1
        continue

      new_selected.append((first_fit, item_i[0]))
      new_remaining[0] += item_i[1]
      if not max_remaining or new_remaining[0] > max_remaining[0]:
        max_remaining = new_remaining
        max_selected = new_selected

        # if value increased by item_i[1], we have maxed out
        if new_remaining[0] >= remaining[0] + item_i[1]:
          break

      next_fit = check_fit(item_i[2:], capacity[first_fit+1:])
      if PRINT_STACK:
        print(f'Max first_fit loop {first_fit} {next_fit} {items[i]} {max_remaining} {max_selected}')
      if next_fit < 0:
        break
      first_fit += next_fit + 1

    if max_remaining and (
        (required_i and item_i[0] not in [s[1] for s in selected])
        or max_remaining[0] > remaining[0]):
      remaining = max_remaining
      selected = max_selected

    if required_i and item_i[0] not in [s[1] for s in selected]:
      # no solution when item i is required, but does not fit
      cannot_fit_items = str(
        [j for j in sorted(list(set(
              [s[1] for s in selected] + [item_i[0]])))
           if len(lookup[j]) > 2 + len(capacity[0]) and
           str(lookup[j][1]).lower().startswith('t')]
        )
      if PRINT_STACK:
        print(f'cannot fit items {cannot_fit_items} i {i} {selected}')
      return ([], ['cannot fit items ' + cannot_fit_items])

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
    return ([], ['capacity must be a list of capacities'])
  capacity_type = list(set([type(c).__name__ for c in capacity]))
  if len(capacity_type) != 1 or capacity_type[0] not in ['list', 'tuple']:
    return ([], ['capacity must be a list of list of ints'])
  num_sacks = len(capacity)
  if num_sacks <= 0:
    return ([], ['there must be at least one sack'])
  num_weights = len(capacity[0])
  if num_weights <= 0:
    return ([], ['there must be at least one weight'])
  if min([len(c) for c in capacity]) != num_weights:
    return ([], ['all capacity must have the same number of weights'])
  if max([len(c) for c in capacity]) != num_weights:
    return ([], ['all capacity must have the same number of weights'])

  for cap in capacity:
    cap_type = list(set([type(c).__name__ for c in cap]))
    if len(cap_type) != 1 or cap_type[0] != 'int':
      return ([], ['all weights must be int'])
    if min(cap) <= 0:
      return ([], ['all weights must be +ve'])

  if len(set([i[0] for i in items])) != len(items):
    return ([], ['item names are not unique'])
  for item in items:
    item_type = list(set([type(i).__name__ for i in item[-len(capacity[0])-1:]]))
    if len(item_type) != 1 or item_type[0] != 'int':
      return ([], ['all item values and weights must be int'])
    if item[-len(capacity[0])-1] <= 0:
      return ([], ['all item values must be > 0'])
    if min(item[-len(capacity[0]):]) < 0:
      return ([], ['all item weights must be >= 0'])

  # Use greedy algorithm - sort by max value and then by least weight
  sorted_items = sorted(items, key=lambda x : (-x[-num_weights-1], sum(x[-num_weights:])))
  return solve_knapsack(sorted_items, capacity)


def print_knapsack(sack):
  return f'value = {sack[1][0]}, items = ' + str(
    [(k, sorted([s[1] for s in sack[0] if s[0] == k]))
         for k in range(len(sack[1])-1)])


if __name__ == '__main__':
  if '--print-loop' in sys.argv:
    PRINT_LOOP = True
  if '--print-stack' in sys.argv:
    PRINT_STACK = True

  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 1, 1), ('B', 6, 2), ('C', 10, 3), ('D', 16, 5)], [(7,)])))
  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 1, 1), ('B', 6, 2), ('C', 10, 3), ('D', 16, 5)], [(6,)])))
  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 1, 1), ('B', True, 6, 2), ('C', 10, 3), ('D', 16, 5)], [(6,)])))
  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 1, 1, 3), ('B', 6, 2, 2), ('C', 10, 3, 5), ('D', 16, 5, 4)],
    [(7, 7)])))

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
    [(20, 245)]
    )))

  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 2, 1, 20),
     ('B', True, 2, 1, 25),
     ('C', 3, 2, 30),
     ('D', False, 2, 3, 35),
     ('E', 5, 3, 40),
     ('F', 6, 3, 40),
     ('G', 2, 3, 45),
     ('H', 5, 3, 45),
     ('I', 7, 4, 50)],
    [(20, 245)]
    )))

  print(print_knapsack(validate_and_solve_knapsack(
    [('A', 2, 1, 20),
     ('B', False, 2, 1, 25),
     ('C', 3, 2, 30),
     ('D', True, 2, 3, 35),
     ('E', 5, 3, 40),
     ('F', 6, 3, 40),
     ('G', 2, 3, 45),
     ('H', 5, 3, 45),
     ('I', 7, 4, 50)],
    [(20, 245)]
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
    [(300, 300, 100)]
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
    [(300, 300, 100), (300, 300, 100)]
    )))


