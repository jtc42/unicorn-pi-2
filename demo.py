import time
import random
import sys
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

DURATION = 5  # seconds per animation in cycle mode
SINGLE_ANIM_DURATION = 30  # seconds when running a specific animation


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

    # Check if command line arguments were provided
    if len(sys.argv) > 1:
        animation_name = sys.argv[1]

        # Handle help flag and list option
        if animation_name in ["-h", "--help"]:
            print("Unicorn HAT HD Demo Script")
            print("Usage: python demo.py [animation_name] [duration]")
            print()
            print("Options:")
            print("  -h, --help     Show this help message")
            print("  -l, --list     List all available animations")
            print()
            print("Available animations:")
            for name in sorted(ANIMATIONS.keys()):
                print(f"  - {name}")
            print()
            print("Examples:")
            print(
                "  python demo.py                     # Run all animations in a cycle"
            )
            print(
                "  python demo.py 'Ising Model'       # Run only the Ising Model animation"
            )
            print(
                "  python demo.py 'Plasma' 60         # Run Plasma animation for 60 seconds"
            )
            unicornhathd.off()
            return

        # List available animations
        if animation_name in ["-l", "--list"]:
            print("Available animations:")
            for name in sorted(ANIMATIONS.keys()):
                print(f"  - {name}")
            unicornhathd.off()
            return

        # Check if duration was specified
        duration = SINGLE_ANIM_DURATION
        if len(sys.argv) > 2:
            try:
                duration = int(sys.argv[2])
                print(f"Setting duration to {duration} seconds")
            except ValueError:
                print(
                    f"Invalid duration value. Using default: {SINGLE_ANIM_DURATION} seconds"
                )

        # Check if the animation exists
        if animation_name in ANIMATIONS:
            print(f"Running specific animation: {animation_name}")
            try:
                # Run the specified animation until duration expires or user interrupts
                if duration <= 0:  # Run indefinitely for zero or negative duration
                    while True:  # Indefinite loop
                        run_animation(
                            animation_name, ANIMATIONS[animation_name], 60
                        )  # Update every minute
                else:
                    # Run for the specified duration
                    run_animation(animation_name, ANIMATIONS[animation_name], duration)
            except KeyboardInterrupt:
                print("Exiting demo...")
                unicornhathd.off()
        else:
            # Show available animations if the specified one wasn't found
            print(f"Animation '{animation_name}' not found.")
            print("Available animations:")
            for name in sorted(ANIMATIONS.keys()):
                print(f"  - {name}")
            unicornhathd.off()
    else:
        # Default behavior: cycle through all animations
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
