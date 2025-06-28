import numpy as np

# 16x16 grid
WIDTH = 16
HEIGHT = 16

# Initialize the grid randomly
_grid = np.random.choice([0, 1], size=(HEIGHT, WIDTH))
_last_update = -1


def _step_life():
    global _grid
    neighbors = sum(
        np.roll(np.roll(_grid, i, 0), j, 1)
        for i in (-1, 0, 1)
        for j in (-1, 0, 1)
        if (i != 0 or j != 0)
    )
    _grid = ((neighbors == 3) | ((neighbors == 2) & (_grid == 1))).astype(int)


def get_life_value(t, i, x, y):
    """
    Returns 1.0 for alive, 0.0 for dead, -1.0 for 'low life' (cell with 1 neighbor).
    t: time in seconds (float)
    i: pixel index (unused)
    x, y: pixel coordinates
    """
    global _last_update
    # Update every 0.2 seconds
    step_time = 0.2
    step = int(t // step_time)
    if step != _last_update:
        _step_life()
        _last_update = step
    xi, yi = int(x) % WIDTH, int(y) % HEIGHT
    alive = _grid[yi, xi]
    # Count neighbors for this cell
    neighbors = sum(
        _grid[(yi + dy) % HEIGHT, (xi + dx) % WIDTH]
        for dy in (-1, 0, 1)
        for dx in (-1, 0, 1)
        if not (dx == 0 and dy == 0)
    )
    if alive:
        return 1.0
    elif neighbors == 1:
        return -1.0
    else:
        return 0.0
