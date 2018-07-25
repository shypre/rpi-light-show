from neopixel import *
import time
import atexit

# Begin config
NUM_PIXELS = 144
GPIO_PIN = 18

INTENSITY = 15
DELAY = 0.25
# End config

np = Adafruit_NeoPixel(NUM_PIXELS, GPIO_PIN, brightness=INTENSITY)

np.begin()

def _atexit():
    print("Clearing the strip")
    set_all((0, 0, 0, 0))
    np._cleanup()
atexit.register(_atexit)

def set_all(color):
    for pixel in range(NUM_PIXELS):
        np.setPixelColorRGB(pixel, *color)
