from rpi_ws281x import *
import time
import atexit

# Begin config
NUM_PIXELS = 256
WIDTH = 16
HEIGHT = 16
GPIO_PIN = 18

INTENSITY = 25
# End config


np = PixelStrip(NUM_PIXELS, GPIO_PIN, brightness=INTENSITY, strip_type = ws.WS2811_STRIP_GRB)

np.begin()

np.setBrightness(INTENSITY)

def _atexit():
    print("Clearing the strip")
    set_all((0, 0, 0, 0))
    np.show()
    np._cleanup()
atexit.register(_atexit)

def set_all(color):
    for pixel in range(NUM_PIXELS):
        np.setPixelColorRGB(pixel, color[0], color[1], color[2])
        if len(color) >=4:
            np.setBrightness(color[3])
        
def rgb_normalize(r, g, b):
    maxvalue = max(r, g, b)
    if (maxvalue == 0):
        return r, g, b
    coeff = 255/maxvalue
    return int(r*coeff), int(g*coeff), int(b*coeff)

def RGB(color):
    r = color
