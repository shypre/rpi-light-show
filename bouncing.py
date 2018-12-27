from rpi_ws281x import *
import time
# Begin config
NUM_PIXELS = 144
WIDTH = 16
HEIGHT = 16
GPIO_PIN = 18

INTENSITY = 2
# End config


np = PixelStrip(NUM_PIXELS, GPIO_PIN, brightness=INTENSITY, strip_type = ws.WS2811_STRIP_GRB)

np.begin()

np.setBrightness(INTENSITY)


FOREGROUND = (0,   255, 0)
BACKGROUND = (255, 255, 255)
MIN_DISTANCE = 8

DELAY = 0.05

"""r, g, b, a = 0, 0, 0, 0
while True:
    r = (r + 2) % 256
    g = (g + 7) % 256
    b = (b + 9) % 256
    a = (a + 10) % 256
    r, g, b = rgb_normalize(r, g, b)
    color = (r, g, b, a)
    set_all(color)
    
    np.show()
    time.sleep(DELAY)
"""

def set_all(color):
	for n in range(NUM_PIXELS):
		np.setPixelColorRGB(n, *color)

set_all(BACKGROUND)
np.show()
"""
while True:
    for n in range(NUM_PIXELS):
        np.setPixelColorRGB((n-1)%(NUM_PIXELS), *BACKGROUND)
        np.setPixelColorRGB(n, *FOREGROUND)
        np.show()
        time.sleep(DELAY)
"""
