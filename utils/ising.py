import numpy as np


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
        temporal_window=4,  # Number of grids to average for smoothing
    ):
        self.width = width
        self.height = height
        self.j = J
        self.h = H
        self.initial_temperature = initial_temperature
        self.temperature = initial_temperature
        self.annealing_rate = annealing_rate
        self.min_temperature = min_temperature
        self.temporal_window = temporal_window
        self._grid = np.random.choice([-1, 1], size=(self.height, self.width))
        self._last_update = -1
        self._history = np.empty(
            (self.temporal_window, self.height, self.width), dtype=np.float32
        )
        self._history[0] = self._grid
        self._history_ptr = 1  # Next index to write
        self._history_filled = 1  # Number of valid grids
        self._history_sum = self._grid.astype(np.float32).copy()  # Running sum for mean

    def _heatbath_step(self):
        """
        Vectorized red-black (checkerboard) heatbath update for the Ising model using numpy.
        This preserves asynchronous-like dynamics and avoids checkerboard artifacts.
        """
        grid = self._grid
        for parity in [0, 1]:
            # Calculate neighbor sum with periodic boundary conditions
            neighbors_sum = (
                np.roll(grid, 1, axis=0)  # North
                + np.roll(grid, -1, axis=0)  # South
                + np.roll(grid, 1, axis=1)  # West
                + np.roll(grid, -1, axis=1)  # East
            )
            delta_E = 2 * self.j * neighbors_sum
            if self.h != 0:
                delta_E += 2 * self.h
            flip_prob = 1 / (1 + np.exp(-delta_E / self.temperature))
            rand_vals = np.random.rand(self.height, self.width)
            # Create checkerboard mask for current parity
            mask = np.indices((self.height, self.width)).sum(axis=0) % 2 == parity
            # Only update spins at the current parity
            update = np.where(rand_vals < flip_prob, 1, -1)
            grid = np.where(mask, update, grid)
        self._grid = grid

    def get_ising_value(self, t, i, x, y):
        """
        Returns a value between -1.0 and 1.0 representing the spin at position (x, y).
        t: time in seconds (float)
        i: pixel index (unused)
        x, y: pixel coordinates
        """
        if t != self._last_update:
            self._heatbath_step()

            # Gradually lower the temperature (simulated annealing)
            self.temperature = max(
                self.min_temperature,
                self.initial_temperature - t * self.annealing_rate,
            )
            # Remove the old grid from the sum if buffer is full
            if self._history_filled == self.temporal_window:
                self._history_sum -= self._history[self._history_ptr]
            else:
                self._history_filled += 1
            # Add the new grid to the sum and buffer
            self._history[self._history_ptr] = self._grid
            self._history_sum += self._grid
            self._history_ptr = (self._history_ptr + 1) % self.temporal_window
        # Compute the temporally averaged grid (O(1))
        avg_grid = self._history_sum / self._history_filled
        xi, yi = int(x) % self.width, int(y) % self.height
        spin = avg_grid[yi, xi]

        self._last_update = t  # Update last update time

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

        self._history = np.empty(
            (self.temporal_window, self.height, self.width), dtype=np.float32
        )
        self._history[0] = self._grid
        self._history_ptr = 1
        self._history_filled = 1
        self._history_sum = self._grid.astype(np.float32).copy()


# Singleton instance for module-level functions
_ising_instance = IsingModel()


def get_ising_value(t, i, x, y):
    return _ising_instance.get_ising_value(t, i, x, y)


def reset_ising_model(temp=2.0, annealing_rate=None, min_temp=None):
    _ising_instance.reset(temp, annealing_rate, min_temp)
    return True
