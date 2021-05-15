'''
Multiple Knapsack problem

This solves the multiple knapsack problem with multiple dimensions
Here we want to maximize the total value for all items
Each item can be in only one knapsack
Each knapsack has limits for how much weight and volume it can carry

To run, use the following command:
  python3 multi_knapsack.py
'''

import sys


PRINT_STACK = False


def check_fit(item, remaining):
  for i in range(len(remaining)):
    check = True
    for r in range(len(remaining[i])):
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

     returns tuple of selected items and value with remaining capacity
  '''
  if PRINT_STACK:
    print(f'Called solve {[i[0] for i in items]} for {capacity}')
  selected = []
  # First item is value, rest is remaining capacity
  remaining = [0] + [[c for c in k] for k in capacity]

  for i in range(len(items)):
    first_fit = check_fit(items[i][2:], remaining[1:])

    if first_fit >= 0:
      for r in range(len(capacity[first_fit])):
        remaining[first_fit + 1][r] -= items[i][2 + r]
      remaining[0] += items[i][1]
      selected.append((first_fit, items[i][0]))
      continue

    # Does not fit
    if not selected:
      # if there is nothing selected, skip item
      continue

    # Find max of first i items with reduced capacity
    first_fit = check_fit(items[i][2:], capacity)
    while first_fit >= 0:
      too_big = False
      new_capacity = [[c for c in k] for k in capacity]
      for c in range(len(capacity[first_fit])):
        new_capacity[first_fit][c] -= items[i][2 + c]
        if new_capacity[first_fit][c] < 0:
          # item i is too big, skip it
          too_big = True
          break
      if too_big:
        if first_fit + 1 >= len(capacity):
          # item i is too big, skip it
          break
        next_fit = check_fit(items[i][2:], capacity[first_fit+1:])
        if next_fit < 0:
          break
        first_fit += next_fit + 1
        continue

      new_selected, new_remaining = solve_knapsack(items[:i], new_capacity)
      new_selected.append((first_fit, items[i][0]))
      new_remaining[0] += items[i][1]
      if new_remaining[0] <= remaining[0]:
        if first_fit + 1 >= len(capacity):
          # there is no benefit to include item i
          break
        next_fit = check_fit(items[i][2:], capacity[first_fit+1:])
        if next_fit < 0:
          break
        first_fit += next_fit + 1
        continue

      remaining = new_remaining
      selected = new_selected
      break

  return (selected, remaining)


def print_knapsack(sack):
  return f'value = {sack[1][0]}, items = ' + str(
    [(k, sorted([s[1] for s in sack[0] if s[0] == k]))
         for k in range(len(sack[1])-1)])


if __name__ == '__main__':
  if '--print-stack' in sys.argv:
    PRINT_STACK = True
  
  print(print_knapsack(solve_knapsack(
    [('A', 1, 1), ('B', 6, 2), ('C', 10, 3), ('D', 16, 5)], [(7,)])))
  print(print_knapsack(solve_knapsack(
    [('A', 1, 1), ('B', 6, 2), ('C', 10, 3), ('D', 16, 5)], [(6,)])))
  print(print_knapsack(solve_knapsack(
    [('A', 1, 1, 3), ('B', 6, 2, 2), ('C', 10, 3, 5), ('D', 16, 5, 4)],
    [(7, 7)])))

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
    [(20, 245)]
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
    [(300, 300, 100)]
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
    [(300, 300, 100), (300, 300, 100)]
    )))


