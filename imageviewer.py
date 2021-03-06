#!/usr/bin/env python3
"""
Projects an image on to a LED matrix via GPIO.
"""

import argparse
from PIL import Image
import traceback

import terminal_output
from simplegrid import *

LED_INTENSITY = 25
VERBOSE = False

def debug_print(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

def process_image(filename, size):
    im = Image.open(filename)
    out = im.resize((size, size))
    out = out.convert("RGB")  # Convert to RGB
    return out

def draw_led_matrix(grid, image):
    x = y = 0
    for num, pixel in enumerate(image.getdata()):
        # Tracking x, y is only for debug purposes
        debug_print("DEBUG: Drawing pixel %s\tat (%d, %d)\tnum=%s" % (pixel, x, y, num))

        grid.set(x, y, pixel)

        if x >= (image.width - 1):
            y += 1
            x = 0
        else:
            x += 1

def main():
    parser = argparse.ArgumentParser(description='Project an image onto a LED matrix.')
    parser.add_argument('filename', type=str, help='filename of the image to display')
    parser.add_argument('boardsize', type=int, help='the width and height of the LED matrix')
    parser.add_argument('gpionum', type=int, help='the target GPIO pin')
    parser.add_argument('--verbose', '-v', action='store_true', help='enables verbose output')

    args = parser.parse_args()
    global VERBOSE
    VERBOSE = args.verbose
    try:
        from rpi_ws281x import PixelStrip
    except ImportError:
        class PixelStrip():
            """PixelStrip stub."""
            def __init__(self, *args, **kwargs):
                print("rpi_ws281x not found - this won't actually draw anything.")

            def begin(self):
                pass

            def setPixelColorRGB(self, *args):
                pass

            def show(self):
                print("Done mock drawing.")

    np = PixelStrip(args.boardsize**2, args.gpionum, brightness=LED_INTENSITY)
    np.begin()

    my_grid = led_grid.LEDGrid(np, grid.SerpentinePattern.TOP_RIGHT, args.boardsize, args.boardsize)

    image = process_image(args.filename, args.boardsize)
    draw_led_matrix(my_grid, image)
    np.show()
    try:
        terminal_output.print_led_grid(my_grid)
    except:
        traceback.print_exc()

if __name__ == '__main__':
    main()
