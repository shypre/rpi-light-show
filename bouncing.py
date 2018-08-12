from np_simplelib import *


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
set_all(BACKGROUND)
while True:
    for n in range(NUM_PIXELS):
        np.setPixelColorRGB((n-1)%(NUM_PIXELS), *BACKGROUND)
        np.setPixelColorRGB(n, *FOREGROUND)
        np.show()
        time.sleep(DELAY)
