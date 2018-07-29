from neopixel import *
import time
import atexit

# Begin config
NUM_PIXELS = 144
GPIO_PIN = 18

INTENSITY = 2
DELAY = 1
# End config


np = Adafruit_NeoPixel(NUM_PIXELS, GPIO_PIN, brightness=INTENSITY)

np.begin()

def _atexit():
    print("Clearing the strip")
    set_all((0, 0, 0, 0))
    np.show()
    np._cleanup()
atexit.register(_atexit)

def set_all(color):
    for pixel in range(NUM_PIXELS):
        np.setPixelColorRGB(pixel, color[0], color[1], color[2])
        np.setBrightness(color[3])
        
def rgb_normalize(r, g, b):
    maxvalue = max(r, g, b)
    if (maxvalue == 0):
        return r, g, b
    coeff = 255/maxvalue
    return int(r*coeff), int(g*coeff), int(b*coeff)
