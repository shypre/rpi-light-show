#!/usr/bin/env python3
"""
Projects an image on to a LED matrix via GPIO.
"""

import argparse
from PIL import Image
import terminal_output

LED_INTENSITY = 25

def process_image(filename, size):
    im = Image.open(filename)
    out = im.resize((size, size))
    return out

def draw_led_matrix(np, image):
    x = y = 0
    for num, pixel in enumerate(image.getdata()):
        # Tracking x, y is only for debug purposes
        print("Drawing pixel %s\tat (%d, %d)" % (pixel, x, y))

        np.setPixelColorRGB(num, *pixel)

        if x >= (image.width - 1):
            y += 1
            x = 0
        else:
            x += 1
    terminal_output.print_led_grid_np(np._led_data, 16, 16)
    np.show()

def main():
    parser = argparse.ArgumentParser(description='Project an image onto a LED matrix.')
    parser.add_argument('filename', type=str, help='filename of the image to display')
    parser.add_argument('boardsize', type=int, help='the width and height of the LED matrix')
    parser.add_argument('gpionum', type=int, help='the target GPIO pin')

    args = parser.parse_args()
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

    image = process_image(args.filename, args.boardsize)
    draw_led_matrix(np, image)

if __name__ == '__main__':
    main()
