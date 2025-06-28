import time
import random
from utils.animations import ANIMATIONS

# Use the same colors as main.py
POSITIVE_COLOR = (255, 255, 255)
NEGATIVE_COLOR = (255, 100, 0)

try:
    import unicornhathd
except ImportError:
    print("This script requires the unicornhathd library and hardware.")
    exit(1)

WIDTH, HEIGHT = unicornhathd.get_shape()

DURATION = 5  # seconds per animation


def run_animation(name, func, duration):
    print(f"Running animation: {name}")
    start_time = time.time()
    while time.time() - start_time < duration:
        t = time.time() - start_time
        for y in range(HEIGHT):
            for x in range(WIDTH):
                i = y * WIDTH + x
                value = func(t, i, x, y)
                value = max(-1.0, min(1.0, value))
                # Use POSITIVE_COLOR and NEGATIVE_COLOR for mapping
                if value > 0:
                    r = int(POSITIVE_COLOR[0] * value)
                    g = int(POSITIVE_COLOR[1] * value)
                    b = int(POSITIVE_COLOR[2] * value)
                elif value < 0:
                    r = int(NEGATIVE_COLOR[0] * -value)
                    g = int(NEGATIVE_COLOR[1] * -value)
                    b = int(NEGATIVE_COLOR[2] * -value)
                else:
                    r, g, b = 0, 0, 0
                unicornhathd.set_pixel(x, y, r, g, b)
        unicornhathd.show()
        time.sleep(1.0 / 60)


def main():
    unicornhathd.rotation(0)
    unicornhathd.brightness(0.8)
    try:
        while True:
            anim_list = list(ANIMATIONS.items())
            random.shuffle(anim_list)
            for name, func in anim_list:
                run_animation(name, func, DURATION)
    except KeyboardInterrupt:
        print("Exiting demo...")
        unicornhathd.off()


if __name__ == "__main__":
    main()
