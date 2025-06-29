from math import sin, cos, tan, atan2, sqrt, hypot, exp
from utils.game_of_life import get_life_value
from utils.ising import get_ising_value, reset_ising_model

# --- Animation Definitions ---
# Each function now takes (t, i, x, y) and returns a single float.
# The value will be clipped to [-1.0, 1.0] and used for brightness.
ANIMATIONS = {
    "Plasma": lambda t, i, x, y: (
        sin(x * 0.2 + t)
        + sin(y * 0.3 + t)
        + sin(sqrt((x - 7.5) ** 2 + (y - 7.5) ** 2) * 0.3 + t)
    )
    / 3.0,
    "Fireworks": lambda t, i, x, y: (-0.4 / (hypot(x - t % 10, y - t % 8) - t % 2 * 9)),
    "Animated Smooth Noise": lambda t, i, x, y: (cos(t + i + x * y)),
    "Dialogue": lambda t, i, x, y: (1 / 32 * tan((2 * t) / 64 * x * tan(i - x))),
    "Spiral": lambda t, i, x, y: sin(
        atan2(y - 7.5, x - 7.5) * 3 + sqrt((x - 7.5) ** 2 + (y - 7.5) ** 2) - t * 2
    ),
    "Game of Life": lambda t, i, x, y: get_life_value(t, i, x, y),
    "Wave Packet": lambda t, i, x, y: sin(0.5 * x - ((t % 16) - 8) * 2)
    * exp(-((x - 8 - ((t % 16) - 8) * 2) ** 2 + (y - 8) ** 2) / 20),
    "Circular Interference": lambda t, i, x, y: 0.5
    * sin(sqrt((x - 4) ** 2 + (y - 8) ** 2) - t * 2)
    + 0.5 * sin(sqrt((x - 12) ** 2 + (y - 8) ** 2) - t * 2),
    "Bessel Mode": lambda t, i, x, y: (
        sin(sqrt((x - 7.5) ** 2 + (y - 7.5) ** 2) - t * 2)
        * (1.2 - 0.08 * sqrt((x - 7.5) ** 2 + (y - 7.5) ** 2))
    ),
    "Lissajous Figure": lambda t, i, x, y: sin(0.3 * x + t) * cos(0.4 * y - t),
    "Dynamic Magnetic Field": lambda t, i, x, y: sin(
        atan2(y - 7.5, x - 7.5) * 4 + 2 * sin(t + sqrt((x - 7.5) ** 2 + (y - 7.5) ** 2))
    )
    * cos(0.5 * sqrt((x - 7.5) ** 2 + (y - 7.5) ** 2) - t),
    "Quantum Harmonic Oscillator": lambda t, i, x, y: (
        2
        * sin(0.4 * (x - 7.5))
        * sin(0.4 * (y - 7.5))
        * cos(t)
        * exp(-0.03 * ((x - 7.5) ** 2 + (y - 7.5) ** 2))
    ),
    "Double Pendulum Shadow": lambda t, i, x, y: (
        sin(t + sin(0.2 * x) * cos(0.3 * y + t))
        * cos(t + cos(0.2 * y) * sin(0.3 * x - t))
    ),
    "Magnetic Dipole Field": lambda t, i, x, y: (
        (2 * (y - 7.5) ** 2 - (x - 7.5) ** 2)
        / ((x - 7.5) ** 2 + (y - 7.5) ** 2 + 1e-3) ** 1.5
        * sin(2 * t)
    ),
    "Lorenz Slice": lambda t, i, x, y: (
        sin(0.2 * x + 10 * sin(0.1 * y + (0.5 * t)))
        * cos(0.2 * y + 10 * cos(0.1 * x - (0.5 * t)))
    ),
    "Ising Model": lambda t, i, x, y: (
        # Reset on first call with faster annealing
        get_ising_value(t, i, x, y)
        if t > 0.1 or reset_ising_model(3.0, 0.05, 0.5)
        else 0
    ),
    "Ising Model (High Temp)": lambda t, i, x, y: (
        # Reset on first call with higher temperature
        get_ising_value(t, i, x, y)
        if t > 0.1 or reset_ising_model(3.5, 0.05, 0.8)
        else 0
    ),
}
