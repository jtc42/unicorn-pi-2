import numpy as np
import random
import math


# Constants for the Ising simulation
WIDTH = 16
HEIGHT = 16
J = 1.0  # Coupling constant
H = 0.0  # External field
INITIAL_TEMPERATURE = 2.0  # Starting temperature for annealing
TEMPERATURE = INITIAL_TEMPERATURE  # Current temperature (changes during simulation)
ANNEALING_RATE = 0.05  # Temperature decrease per second
MIN_TEMPERATURE = 0.5  # Minimum temperature

# Initialize grid randomly
_grid = np.random.choice([-1, 1], size=(HEIGHT, WIDTH))
_last_update = -1


def _heatbath_step():
    """
    Implement the heatbath algorithm for the Ising model.
    This will update the entire grid once using the heatbath algorithm.
    """
    global _grid

    # Make a copy of the grid to update
    for _ in range(WIDTH * HEIGHT):
        # Pick a random site
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)

        # Calculate neighbor sum with periodic boundary conditions
        neighbors_sum = (
            _grid[(y - 1) % HEIGHT, x]  # North
            + _grid[(y + 1) % HEIGHT, x]  # South
            + _grid[y, (x - 1) % WIDTH]  # West
            + _grid[y, (x + 1) % WIDTH]  # East
        )

        # Calculate energy difference
        delta_E = 2 * J * neighbors_sum

        # Add external field if present
        if H != 0:
            delta_E += 2 * H

        # Calculate probability according to heatbath algorithm
        r = random.random()
        flip_probability = 1 / (1 + math.exp(-delta_E / TEMPERATURE))

        # Assign new spin based on the probability
        _grid[y, x] = 1 if r < flip_probability else -1


def get_ising_value(t, i, x, y):
    """
    Returns a value between -1.0 and 1.0 representing the spin at position (x, y).
    t: time in seconds (float)
    i: pixel index (unused)
    x, y: pixel coordinates
    """
    global _last_update

    # Update every 0.1 seconds
    step_time = 0.1
    step = int(t // step_time)

    if step != _last_update:
        _heatbath_step()
        _last_update = step

        # Gradually lower the temperature (simulated annealing)
        global TEMPERATURE
        TEMPERATURE = max(MIN_TEMPERATURE, INITIAL_TEMPERATURE - t * ANNEALING_RATE)

    # Get the spin value at the requested position
    xi, yi = int(x) % WIDTH, int(y) % HEIGHT
    spin = _grid[yi, xi]

    return float(spin)


def reset_ising_model(temp=2.0, annealing_rate=None, min_temp=None):
    """
    Reset the Ising model with a new random configuration.

    Args:
        temp: Initial temperature (default: 2.0)
        annealing_rate: Rate at which temperature decreases per second (default: None, keeps current)
        min_temp: Minimum temperature for annealing (default: None, keeps current)
    """
    global _grid, TEMPERATURE, INITIAL_TEMPERATURE, ANNEALING_RATE, MIN_TEMPERATURE
    _grid = np.random.choice([-1, 1], size=(HEIGHT, WIDTH))
    TEMPERATURE = temp
    INITIAL_TEMPERATURE = temp

    if annealing_rate is not None:
        ANNEALING_RATE = annealing_rate

    if min_temp is not None:
        MIN_TEMPERATURE = min_temp
