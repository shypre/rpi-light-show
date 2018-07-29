from np_simplelib import *


FOREGROUND = (0,   255, 0,   INTENSITY)
BACKGROUND = (255, 255, 255, INTENSITY/2)
MIN_DISTANCE = 8

r, g, b, a = 0, 0, 0, 0
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

