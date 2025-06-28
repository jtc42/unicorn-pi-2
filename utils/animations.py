from math import sin, cos, tan, atan, sqrt, hypot
from random import uniform

# --- Animation Definitions ---
# Each function now takes (t, i, x, y) and returns a single float.
# The value will be clipped to [-1.0, 1.0] and used for brightness.
ANIMATIONS = {
    "Sine Wave": lambda t, i, x, y: sin(x * 0.4 + t * 2.0),
    "Plasma": lambda t, i, x, y: (
        sin(x * 0.2 + t)
        + sin(y * 0.3 + t)
        + sin(sqrt((x - 7.5) ** 2 + (y - 7.5) ** 2) * 0.3 + t)
    )
    / 3.0,
    "Expanding Rings": lambda t, i, x, y: cos(
        sqrt((x - 7.5) ** 2 + (y - 7.5) ** 2) * 0.7 - t * 3
    ),
    "Random Noise": lambda t, i, x, y: uniform(-1.0, 1.0),
    "Fireworks": lambda t, i, x, y: (-0.4 / (hypot(x - t % 10, y - t % 8) - t % 2 * 9)),
    "Sierpinski": lambda t, i, x, y: (4 * t & i & x & y),
    "Animated Smooth Noise": lambda t, i, x, y: (cos(t + i + x * y)),
    "3D Checker": lambda t, i, x, y: (
        (((x - 8) / y + t * 5) & 1 ^ 1 / y * 8 & 1) * y / 5
    ),
    "Dialogue": lambda t, i, x, y: (1 / 32 * tan(t / 64 * x * tan(i - x))),
    "Rotation": lambda t, i, x, y: (sin(2 * atan((y - 7.5) / (x - 7.5)) + 5 * t)),
}
