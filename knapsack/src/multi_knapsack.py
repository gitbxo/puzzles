'''
Multiple Knapsack problem

This solves the multiple knapsack problem with multiple dimensions
Here we want to maximize the total value for all items
Each item can be in only one knapsack
Each knapsack has limits for how much weight and volume it can carry

To run, use the following command:
  python3 multi_knapsack.py
'''


def check_fit(item, remaining):
  for i in range(len(remaining)):
    check = True
    for r in range(len(remaining[i])):
      if item[2 + r] > remaining[i][r]:
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
  selected = []
  # First item is value, rest is remaining capacity
  remaining = [0] + [[c for c in k] for k in capacity]

  for i in range(len(items)):
    first_fit = check_fit(items[i], remaining[1:])

    if first_fit >= 0:
      for r in range(len(capacity[first_fit])):
        remaining[first_fit + 1][r] -= items[i][2 + r]
      remaining[0] += items[i][1]
      selected.append((first_fit, items[i]))
      continue

    # Does not fit
    if not selected:
      # if there is nothing selected, skip item
      continue

    # Find max of first i items with reduced capacity
    first_fit = check_fit(items[i], capacity)
    while first_fit > 0:
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
        next_fit = check_fit(items[i], capacity[first_fit:])
        if next_fit < 0:
          break
        first_fit += next_fit
        continue

      new_selected, new_remaining = solve_knapsack(items[:i], new_capacity)
      if new_remaining[0] + items[i][1] <= remaining[0]:
        if first_fit + 1 >= len(capacity):
          # there is no benefit to include item i
          break
        next_fit = check_fit(items[i], capacity[first_fit:])
        if next_fit < 0:
          break
        first_fit += next_fit
        continue

      remaining = new_remaining
      remaining[0] += items[i][1]
      selected = new_selected + [(first_fit, items[i])]


  return (selected, remaining)



def print_knapsack(sack):
  return f'value = {sack[1][0]}, items = ' + str([(s[0], s[1][0]) for s in sack[0]])


if __name__ == '__main__':
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


