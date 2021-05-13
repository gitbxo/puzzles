'''
Knapsack problem
'''

def check_fit(item, remaining):
  for r in range(1, len(remaining)):
    if item[1 + r] > remaining[r]:
      return False
  return True


def solve_knapsack(items, capacity):
  selected = []
  # First item is value, rest is remaining capacity
  remaining = [0] + [c for c in capacity]
  for i in range(len(items)):
    does_fit = check_fit(items[i], remaining)

    if does_fit:
      for r in range(len(capacity)):
        remaining[1 + r] -= items[i][2 + r]
      remaining[0] += items[i][1]
      selected.append(items[i])
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
    if new_remaining[0] + items[i][1] <= remaining[0]:
      # there is no benefit to include item i
      continue

    remaining = new_remaining
    remaining[0] += items[i][1]
    selected = new_selected + [items[i]]


  return (selected, remaining)



def print_knapsack(sack):
  return f'value = {sack[1]}, items = ' + str([i[0] for i in sack[0]])



if __name__ == '__main__':
  print(print_knapsack(solve_knapsack(
    [('A', 1, 1), ('B', 6, 2), ('C', 10, 3), ('D', 16, 5)], (7,))))
  print(print_knapsack(solve_knapsack(
    [('A', 1, 1), ('B', 6, 2), ('C', 10, 3), ('D', 16, 5)], (6,))))
  print(print_knapsack(solve_knapsack(
    [('A', 1, 1, 3), ('B', 6, 2, 2), ('C', 10, 3, 5), ('D', 16, 5, 4)], (7,7))))


