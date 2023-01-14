from math import inf
from itertools import product
import numpy as np

def get_adjacent(grid: np.ndarray, node: tuple):
    i = node[0]
    j = node[1]
    
    h,w = grid.shape

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
    h,w = grid.shape
    return [(i, j) for i, j in product(range(h), range(w)) if (i, j) not in obstacles]


def dijkstra(grid, src, dest, obstacles):
    Q = get_nodes(grid, obstacles)
    
    grid[src] = 0
    grid[dest] = 0

    dist = {node : inf for node in Q}
    prev = {node : None for node in Q}

    dist[src] = 0

    while Q:
        u = min(Q, key = dist.__getitem__)
        Q.remove(u)

        for v in get_adjacent(grid, u):
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    path = [dest]
    cur = dest

    
    while prev[cur]:
        path.append(prev[cur])
        cur = prev[cur]

    return list(reversed(path))
