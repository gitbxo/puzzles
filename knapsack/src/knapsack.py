'''
Knapsack problem

This solves the multi-dimensional knapsack problem

To run, use the following command:
  python3 knapsack.py
'''

import sys


PRINT_STACK = False


def check_fit(item, remaining):
  for r in range(len(remaining)):
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
    print(f'Called solve {[i[0] for i in items]} for {capacity}')
  selected = []
  # First item is value, rest is remaining capacity
  remaining = [0] + [c for c in capacity]

  for i in range(len(items)):
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

    # Find max of first i items with reduced capacity
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
    new_selected.append(items[i][0])
    new_remaining[0] += items[i][1]
    if new_remaining[0] <= remaining[0]:
      # there is no benefit to include item i
      continue

    remaining = new_remaining
    selected = new_selected

  return (selected, remaining)


def print_knapsack(sack):
  return f'value = {sack[1][0]}, items = ' + str(
    sorted(sack[0]))


if __name__ == '__main__':
  if '--print-stack' in sys.argv:
    PRINT_STACK = True
  
  print(print_knapsack(solve_knapsack(
    [('A', 1, 1), ('B', 6, 2), ('C', 10, 3), ('D', 16, 5)], (7,))))
  print(print_knapsack(solve_knapsack(
    [('A', 1, 1), ('B', 6, 2), ('C', 10, 3), ('D', 16, 5)], (6,))))
  print(print_knapsack(solve_knapsack(
    [('A', 1, 1, 3), ('B', 6, 2, 2), ('C', 10, 3, 5), ('D', 16, 5, 4)],
    (7, 7))))

  print(print_knapsack(solve_knapsack(
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

  print(print_knapsack(solve_knapsack(
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


