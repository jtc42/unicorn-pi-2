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
    Returns 1.0 for alive, -1.0 for dead. Updates the grid every 0.2s.
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
    return 1.0 if _grid[int(y) % HEIGHT, int(x) % WIDTH] else -1.0
