import time

import numpy as np
from z3 import Solver, sat, Int, Distinct, And

# Taken from
PROBLEMS = [
    "53  7    6  195    98    6 8   6   34  8 3  17   2   6 6    28    419  5    8  79",
    "       75  4  5   8 17 6   36  2 7 1   5 1   1 5 8  96   1 82 3   4  9  48       ",
    " 9 7 4  1    6 2 8    1 43  6     59   1 3   97     8  52 7    6 8 4    7  5 8 2 ",
    "67 38      921   85    736 1 8  4 7  5 1 8 4  2 6  8 5 175    24   321      61 84",
    "27  15  8   3  7 4    7     5 1   7   9   2   6   2 5     8    6 5  4   8  59  41",
    "8 64 3    5     7     2    32  8  5   8 5 4  1   7  93    4     9     4    6 72 8",
    " 8 9 3 7            2 1 6  8  3 9  5  6   4  5  1 7  9  8 2 5            7 8 1 2 "
]

GROUP_SIZE = 3
GRID_SIZE = GROUP_SIZE**2  # 9

def print_flattened(flattened):
    LINE = "|".join(["%s" * GROUP_SIZE] * GROUP_SIZE)
    SEP = "+".join(["-"  * GROUP_SIZE] * GROUP_SIZE)
    print(SEP)
    for y in range(GRID_SIZE):
        offset = y * GRID_SIZE
        print(LINE % tuple(flattened[offset:offset+GRID_SIZE]))
        if (y+1) % GROUP_SIZE == 0:
            print(SEP)


def as_matrix(flattened):
    return np.array([[flattened[y*GRID_SIZE + x] for x in range(GRID_SIZE)] for y in range(GRID_SIZE)])


def print_matrix(matrix):
    LINE = "|".join(["%s" * GROUP_SIZE] * GROUP_SIZE)
    SEP = "+".join(["-"  * GROUP_SIZE] * GROUP_SIZE)
    print(SEP)
    for y in range(GRID_SIZE):
        offset = y * GRID_SIZE
        print(LINE % tuple(matrix[y]))
        if (y+1) % GROUP_SIZE == 0:
            print(SEP)


def solve_soduko(flattened):
    fact_matrix = as_matrix(flattened)
    symbol_grid = [[Int(f"x_{y+1}{x+1}") for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

    known_facts = [symbol_grid[y][x] == int(fact_matrix[y, x])
                    for y in range(GRID_SIZE) for x in range(GRID_SIZE)
                    if fact_matrix[y, x] != " "]

    numbers = [And(symbol_grid[y][x] >=1, symbol_grid[y][x] <= 9)
                    for y in range(GRID_SIZE) for x in range(GRID_SIZE)]

    unique_rows = [Distinct(symbol_grid[y]) for y in range(GRID_SIZE)]
    unique_columns = [Distinct([symbol_grid[y][x] for y in range(GRID_SIZE)])
                            for x in range(GRID_SIZE)]

    unique_group = []
    for grid_y in range(0, GRID_SIZE, GROUP_SIZE):
        for grid_x in range(0, GRID_SIZE, GROUP_SIZE):
            unique_group.append(Distinct([symbol_grid[grid_y+y][grid_x+x]
                    for y in range(GROUP_SIZE) for x in range(GROUP_SIZE)]))

    s = Solver()
    s.add(known_facts + numbers + unique_rows + unique_columns + unique_group)
    print(s.check())
    m = s.model()
    solution = [[m[symbol_grid[y][x]] for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    return solution

if __name__ =="__main__":
    problem = PROBLEMS[5]
    print_flattened(problem)
    start = time.time()
    solution = solve_soduko(problem)
    print(f"Solved in {time.time()-start}s")
    print_matrix(solution)

