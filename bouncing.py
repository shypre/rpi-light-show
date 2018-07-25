from np_simplelib import *

FOREGROUND = (0,   255, 0,   INTENSITY)
BACKGROUND = (255, 255, 255, INTENSITY/2)
MIN_DISTANCE = 8

color_idx = 0
while True:
    color = COLORS[color_idx % len(COLORS)]
    set_all(color)
    
    color_idx += 1
    np.show()
    time.sleep(DELAY)
