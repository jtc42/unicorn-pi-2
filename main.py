#!/usr/bin/env python3

import time
import math
import random
from datetime import datetime
from PIL import Image
import unicornhathd

from utils.digits import DIGITS
from utils.animations import ANIMATIONS

# -- Clock Configuration --
HOUR_COLOR = (255, 255, 255)
MINUTE_COLOR = (255, 100, 0)
BRIGHTNESS = 0.8
ROTATION = 0
FLIP_H = True
FLIP_V = False

# -- Auto-Brightness Configuration --
AUTO_BRIGHTNESS = True  # Set to True to enable auto-brightness
MIN_BRIGHTNESS = 0.05  # Minimum brightness level
MAX_BRIGHTNESS = 0.8  # Maximum brightness level

# -- Animation Configuration --
# A list of minutes to trigger an animation on (e.g., [0] for on the hour)
ANIMATION_TRIGGER_MINUTES = [0, 15, 30, 45]
# How long the animation should run in seconds
ANIMATION_DURATION = 20
# Colors for the new animation rendering mode
POSITIVE_COLOR = HOUR_COLOR
NEGATIVE_COLOR = MINUTE_COLOR


def draw_digit(image, digit, x_offset, y_offset, color):
    """Draws a single 8x8 digit onto the Pillow image."""
    digit_array = DIGITS.get(str(digit), DIGITS["0"])
    for y, row in enumerate(digit_array):
        for x, value in enumerate(row):
            if value > 0:
                pixel_color = (
                    int(color[0] * value),
                    int(color[1] * value),
                    int(color[2] * value),
                )
                image.putpixel((x + x_offset, y + y_offset), pixel_color)


def run_animation(duration, width, height):
    """Selects and runs a random animation using the new float->color method."""
    name, func = random.choice(list(ANIMATIONS.items()))
    print(f"Running animation: {name}")

    start_time = time.time()

    while time.time() - start_time < duration:
        t = time.time() - start_time

        for y_hat in range(height):
            for x_hat in range(width):
                i = y_hat * width + x_hat

                # 1. Get float value from the animation function
                value = func(t, i, x_hat, y_hat)

                # 2. Clip the value to the range [-1.0, 1.0]
                value = max(-1.0, min(1.0, value))

                # 3. Determine color and brightness based on the value
                r, g, b = 0, 0, 0
                if value > 0:
                    brightness = value
                    r = int(POSITIVE_COLOR[0] * brightness)
                    g = int(POSITIVE_COLOR[1] * brightness)
                    b = int(POSITIVE_COLOR[2] * brightness)
                elif value < 0:
                    brightness = abs(value)
                    r = int(NEGATIVE_COLOR[0] * brightness)
                    g = int(NEGATIVE_COLOR[1] * brightness)
                    b = int(NEGATIVE_COLOR[2] * brightness)

                # Apply flipping for consistent orientation
                x_disp = (width - 1) - x_hat if FLIP_H else x_hat
                y_disp = (height - 1) - y_hat if FLIP_V else y_hat

                unicornhathd.set_pixel(x_disp, y_disp, r, g, b)

        unicornhathd.show()
        time.sleep(1.0 / 60)  # Aim for 60fps


def update_auto_brightness(current_hour, current_minute):
    """
    Calculates and sets the Unicorn HAT HD brightness sinusoidally
    based on the current time, mimicking daylight.
    Brightness peaks at midday (12 PM) and is at its minimum at midnight (0 AM/PM).
    """
    if AUTO_BRIGHTNESS:
        hour_float = current_hour + (current_minute / 60.0)

        # Calculate brightness using a cosine wave.
        # Shift the phase so 12 PM (noon) is at the peak (1.0)
        # and 0 AM/PM (midnight) is at the trough (-1.0).
        # cos(x) peaks at x=0, 2pi, etc.
        # cos((hour_float - 12) * pi / 12)
        # At hour_float = 12, (12-12)*pi/12 = 0, cos(0) = 1 (max)
        # At hour_float = 0, (0-12)*pi/12 = -pi, cos(-pi) = -1 (min)
        # At hour_float = 24 (next day 0), (24-12)*pi/12 = pi, cos(pi) = -1 (min)

        # Scale the cosine wave from -1 to 1 to a 0 to 1 range
        sin_brightness = (math.cos((hour_float - 12) * math.pi / 12) + 1) / 2

        # Map this 0-1 value to the desired min/max brightness range
        calculated_brightness = MIN_BRIGHTNESS + (
            sin_brightness * (MAX_BRIGHTNESS - MIN_BRIGHTNESS)
        )

        unicornhathd.brightness(calculated_brightness)
        # print(f"Current brightness set to: {calculated_brightness:.2f} (Hour: {hour_float:.2f})") # Uncomment for debugging
    else:
        # If auto-brightness is off, ensure it uses the default BRIGHTNESS
        unicornhathd.brightness(BRIGHTNESS)


def main():
    """Main function to run the clock."""
    unicornhathd.rotation(ROTATION)
    # Initial brightness set here, but it will be overridden by update_auto_brightness
    unicornhathd.brightness(BRIGHTNESS)
    width, height = unicornhathd.get_shape()

    last_minute = -1
    last_hour = -1  # To trigger brightness update on hour change

    print("Clock running. Press Ctrl+C to exit.")

    try:
        while True:
            now = datetime.now()
            current_hour = now.hour
            current_minute = now.minute

            # Only update brightness if the hour or minute has changed
            if current_hour != last_hour or current_minute != last_minute:
                update_auto_brightness(current_hour, current_minute)

                # Check for animation trigger when the minute changes
                if current_minute in ANIMATION_TRIGGER_MINUTES:
                    run_animation(ANIMATION_DURATION, width, height)
                    # After animation, fall through to redraw the clock immediately

                # Draw the clock
                time_str = now.strftime("%H%M")
                image = Image.new("RGB", (width, height))

                draw_digit(image, time_str[0], 0, 0, HOUR_COLOR)
                draw_digit(image, time_str[1], 8, 0, HOUR_COLOR)
                draw_digit(image, time_str[2], 0, 8, MINUTE_COLOR)
                draw_digit(image, time_str[3], 8, 8, MINUTE_COLOR)

                # Update the Unicorn HAT HD display
                for y_img in range(height):
                    for x_img in range(width):
                        x_hat = (width - 1) - x_img if FLIP_H else x_img
                        y_hat = (height - 1) - y_img if FLIP_V else y_img
                        r, g, b = image.getpixel((x_img, y_img))
                        unicornhathd.set_pixel(x_hat, y_hat, r, g, b)

                unicornhathd.show()
                last_minute = current_minute
                last_hour = (
                    current_hour  # Update last_hour here as well for brightness updates
                )

            time.sleep(1.0)

    except KeyboardInterrupt:
        print("Exiting...")
        unicornhathd.off()


if __name__ == "__main__":
    main()
