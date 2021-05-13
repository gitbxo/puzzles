
import datetime
import sys


def sudoku_size():
    return 3


def min_val():
    return 1


def max_val():
    return sudoku_size() * sudoku_size()


def copy(puzzle):
    return [list(r) for r in puzzle]


def check_line(line):
    if type(line) != list or len(line) != max_val():
        return False

    for a in line:
        if a is None:
            continue
        if type(a) != int or a < min_val() or a > max_val():
            return False
        if len([x for x in line if x == a]) != 1:
            return False

    return True


def check_row_col(puzzle):
    if type(puzzle) != list or len(puzzle) != max_val():
        return False

    for i in range(min_val() - 1, max_val()):
        if not check_line(puzzle[i]):
            return False
        col = [row[i] for row in puzzle]
        if not check_line(col):
            return False

    return True


def check_square(puzzle):
    if not check_row_col(puzzle):
        return False

    for r in range(min_val() - 1, max_val(), sudoku_size()):
        for c in range(min_val() - 1, max_val(), sudoku_size()):
            square = [row[c:sudoku_size() + c]
                      for row in puzzle[r:sudoku_size() + r]]
            data = []
            for d in square:
                data.extend(d)
            if not check_line(data):
                return False

    return True


def check_solved(puzzle):
    if not check_square(puzzle):
        return False

    for r in puzzle:
        if None in r:
            return False

    return True


def find_open_pos(puzzle):
    open_pos = [0, 1, 1]
    for r, row in enumerate(puzzle):
        if len(set(row)) <= open_pos[0]:
            continue
        for c, val in enumerate(row):
            if val is None:
                open_pos = [len(set(row)), r, c]
                break

    return open_pos[1:]


def find_num(puzzle):
    isolated = find_isolated_row_value(puzzle)
    if isolated:
        return isolated

    isolated = find_isolated_col_value(puzzle)
    if isolated:
        return isolated

    return find_num2(puzzle)


def find_isolated_row_value(puzzle):
    '''Find values that have only one position in a ow'''
    for i in range(min_val() - 1, max_val()):
        row = puzzle[i]
        row_missing = list(
            set(range(min_val(), max_val() + 1)) - set(row))
        for j in sorted(row_missing):
            test_j = []
            for c in range(len(row)):
                if puzzle[i][c] is None:
                    new_puzzle = copy(puzzle)
                    new_puzzle[i][c] = j
                    if check_square(new_puzzle):
                        test_j.append((i, c, j))
            if len(test_j) == 1:
                return test_j[0]

    return None


def find_isolated_col_value(puzzle):
    '''Find values that have only one position in row or column'''
    for i in range(min_val() - 1, max_val()):
        col = [row[i] for row in puzzle]
        col_missing = list(
            set(range(min_val(), max_val() + 1)) - set(col))
        for j in sorted(col_missing):
            test_j = []
            for r in range(len(col)):
                if puzzle[r][i] is None:
                    new_puzzle = copy(puzzle)
                    new_puzzle[r][i] = j
                    if check_square(new_puzzle):
                        test_j.append((r, i, j))
            if len(test_j) == 1:
                return test_j[0]

        row = puzzle[i]
        row_missing = list(
            set(range(min_val(), max_val() + 1)) - set(row))
        for j in sorted(row_missing):
            test_j = []
            for c in range(len(row)):
                if puzzle[i][c] is None:
                    new_puzzle = copy(puzzle)
                    new_puzzle[i][c] = j
                    if check_square(new_puzzle):
                        test_j.append((i, c, j))
            if len(test_j) == 1:
                return test_j[0]

    return None


def find_num2(puzzle):
    for r in range(min_val() - 1, max_val(), sudoku_size()):
        for c in range(min_val() - 1, max_val(), sudoku_size()):
            sq_rows = puzzle[r:sudoku_size() + r]
            square = [row[c:sudoku_size() + c] for row in sq_rows]
            data = []
            for d in square:
                data.extend(d)

            square_missing = list(
                set(range(min_val(), max_val() + 1)) - set(data))
            for i in sorted(square_missing):
                test_i = []
                for r1 in range(r, r + sudoku_size()):
                    for c1 in range(c, c + sudoku_size()):
                        if puzzle[r1][c1] is None:
                            new_puzzle = copy(puzzle)
                            new_puzzle[r1][c1] = i
                            if check_square(new_puzzle):
                                test_i.append((r1, c1, i))
                if len(test_i) == 1:
                    return test_i[0]

            for r1, row in enumerate(sq_rows):
                other_rows = [sq_rows[i] for i in
                              range(sudoku_size()) if i != r1]
                row_intersect = set(other_rows[0]) - set([None])
                for o in other_rows:
                    row_intersect = row_intersect & set(o)
                for c1 in range(c, c + sudoku_size()):
                    if row[c1] is not None:
                        continue
                    all_but_row = list(
                        set(range(min_val(), max_val() + 1))
                        - set(row))
                    if len(all_but_row) == 1:
                        num = all_but_row[0]
                        if num not in data:
                            print(f'all but row: row {r+r1+1} col {c1+1} to {num}')
                            return (r + r1, c1, num)

                    other_minus_square = list(row_intersect - set(data))
                    if (len(set(square[r1])) == sudoku_size()
                            and len(other_minus_square) == 1):
                        num = other_minus_square[0]
                        return (r + r1, c1, num)

                    col = [p[c1] for p in puzzle]
                    all_but_col = list(
                        set(range(min_val(), max_val() + 1))
                        - set(col))
                    if len(all_but_col) == 1:
                        num = all_but_col[0]
                        if num not in data:
                            print(f'all but col: row {r+r1+1} col {c1+1} to {num}')
                            return (r + r1, c1, num)

                    other_cols = [[p[i] for p in puzzle] for i in
                                  range(c, c + sudoku_size()) if i != c1]
                    col_intersect = set(other_cols[0]) - set([None])
                    for o in other_cols:
                        col_intersect = col_intersect & set(o)
                    other_minus_square = list(col_intersect - set(data))
                    if (len(set([s[c1-c] for s in square])) == sudoku_size()
                            and len(other_minus_square) == 1):
                        num = other_minus_square[0]
                        return (r + r1, c1, num)

                    if len(row_intersect & col_intersect) == 1:
                        num = list(row_intersect & col_intersect)[0]
                        if num not in data:
                            return (r + r1, c1, num)
    return None


def try_solve(puzzle):
    if check_solved(puzzle):
        return puzzle
    if not check_square(puzzle):
        return None

    new_puzzle = copy(puzzle)
    found = find_num(puzzle)
    if found:
        print(f'setting row {found[0] + 1} col {found[1] + 1} to {found[2]}')
        new_puzzle[found[0]][found[1]] = found[2]
        return try_solve(new_puzzle)
    (r, c) = find_open_pos(new_puzzle)
    row_missing = list(
        set(range(min_val(), max_val() + 1)) - set(puzzle[r]))
    for i in sorted(row_missing):
        new_puzzle[r][c] = i
        print(f'guessing row {r + 1} col {c + 1} as {i}')
        check = try_solve(new_puzzle)
        if check:
            return check

    return None


if __name__ == '__main__':
    raw = sys.stdin.read()
    puzzle = [[(int(e) if e != '0' else None) for e in r.split()]
              for r in raw.strip().split('\n')]

    for i, row in enumerate(p):
        if i in [3, 6]:
            print('')
        print(str(row))
    print(f'Start at {datetime.datetime.now()}')
    soln = try_solve(p)
    print(f'Stop at {datetime.datetime.now()}')
    if type(soln) != list:
        print(str(soln) + '\n\n')
    else
        for i, row in enumerate(soln):
            if i in [3, 6]:
                print('')
            print(str(row))
        print('\n')

