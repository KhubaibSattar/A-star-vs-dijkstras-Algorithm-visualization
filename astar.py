from math import inf, sqrt
from itertools import product
import numpy as np


def get_adjacent(grid: np.ndarray, node: tuple):
    i = node[0]
    j = node[1]

    h, w = grid.shape

    if i < 0 or i >= h or j < 0 or j >= w:
        raise Exception("Out of bounds")

    if grid[i][j] != 0:
        return []

    adjacent = []

    for del_pos in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if 0 <= i + del_pos[0] < w and 0 <= j + del_pos[1] < w:
            if grid[i + del_pos[0]][j + del_pos[1]] == 0:
                adjacent.append((i + del_pos[0], j + del_pos[1]))

    return adjacent


def get_nodes(grid: np.ndarray, obstacles: list):
    h, w = grid.shape
    return [(i, j) for i, j in product(range(h), range(w))
            if (i, j) not in obstacles]


def hypot(x, y):
    return sqrt(x ** 2 + y ** 2)

def heuristic_cost_estimate(src, dest):
    return hypot(dest[0] - src[0], dest[1] - src[1])

def a_star(grid, src, dest, obstacles):
    nodes = get_nodes(grid, obstacles)
    
    grid[src] = 0
    grid[dest] = 0
    
    closed_set = []
    open_set = [src]

    prev = {node : None for node in nodes}

    g_score = {node : inf for node in nodes}
    g_score[src] = 0

    f_score = {node : inf for node in nodes}
    f_score[src] = heuristic_cost_estimate(src, dest)

    while open_set:
        u = min(open_set, key = f_score.__getitem__)
        if u == dest:
            break

        open_set.remove(u)
        closed_set.append(u)

        for v in get_adjacent(grid, u):
            if v in closed_set:
                continue

            if v not in open_set:
                open_set.append(v)

            alt_g = g_score[u] + 1
            if alt_g < g_score[v]:
                g_score[v] = alt_g
                f_score[v] = g_score[v] + heuristic_cost_estimate(v, dest)
                prev[v] = u

    path = [dest]
    cur = dest

    while prev[cur]:
        path.append(prev[cur])
        cur = prev[cur]

    return list(reversed(path))
