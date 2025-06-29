import numpy as np
import random
import math


class IsingModel:
    def __init__(
        self,
        width=16,
        height=16,
        J=1.0,
        H=0.0,
        initial_temperature=2.0,
        annealing_rate=0.05,
        min_temperature=0.5,
    ):
        self.width = width
        self.height = height
        self.j = J
        self.h = H
        self.initial_temperature = initial_temperature
        self.temperature = initial_temperature
        self.annealing_rate = annealing_rate
        self.min_temperature = min_temperature
        self._grid = np.random.choice([-1, 1], size=(self.height, self.width))
        self._last_update = -1

    def _heatbath_step(self):
        """
        Implement the heatbath algorithm for the Ising model.
        This will update the entire grid once using the heatbath algorithm.
        """
        # Make a copy of the grid to update
        for _ in range(self.width * self.height):
            # Pick a random site
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            # Calculate neighbor sum with periodic boundary conditions
            neighbors_sum = (
                self._grid[(y - 1) % self.height, x]  # North
                + self._grid[(y + 1) % self.height, x]  # South
                + self._grid[y, (x - 1) % self.width]  # West
                + self._grid[y, (x + 1) % self.width]  # East
            )

            # Calculate energy difference
            delta_E = 2 * self.j * neighbors_sum

            # Add external field if present
            if self.h != 0:
                delta_E += 2 * self.h

            # Calculate probability according to heatbath algorithm
            r = random.random()
            flip_probability = 1 / (1 + math.exp(-delta_E / self.temperature))

            # Assign new spin based on the probability
            self._grid[y, x] = 1 if r < flip_probability else -1

    def get_ising_value(self, t, i, x, y):
        """
        Returns a value between -1.0 and 1.0 representing the spin at position (x, y).
        t: time in seconds (float)
        i: pixel index (unused)
        x, y: pixel coordinates
        """
        # Update every 0.1 seconds
        step_time = 0.1
        step = int(t // step_time)

        if step != self._last_update:
            self._heatbath_step()
            self._last_update = step

            # Gradually lower the temperature (simulated annealing)
            self.temperature = max(
                self.min_temperature,
                self.initial_temperature - t * self.annealing_rate,
            )

        # Get the spin value at the requested position
        xi, yi = int(x) % self.width, int(y) % self.height
        spin = self._grid[yi, xi]

        return float(spin)

    def reset(self, temp=2.0, annealing_rate=None, min_temp=None):
        """
        Reset the Ising model with a new random configuration.

        Args:
            temp: Initial temperature (default: 2.0)
            annealing_rate: Rate at which temperature decreases per second (default: None, keeps current)
            min_temp: Minimum temperature for annealing (default: None, keeps current)
        """
        self._grid = np.random.choice([-1, 1], size=(self.height, self.width))
        self.temperature = temp
        self.initial_temperature = temp

        if annealing_rate is not None:
            self.annealing_rate = annealing_rate

        if min_temp is not None:
            self.min_temperature = min_temp


# Singleton instance for module-level functions
_ising_instance = IsingModel()


def get_ising_value(t, i, x, y):
    return _ising_instance.get_ising_value(t, i, x, y)


def reset_ising_model(temp=2.0, annealing_rate=None, min_temp=None):
    _ising_instance.reset(temp, annealing_rate, min_temp)
    return True
