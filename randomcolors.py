from np_simplelib import *

import random
import time

COLORS = [
    (255, 255, 255),
    (255, 0,   0  ),
    (255, 255, 0  ),
    (0,   255, 0  ),
    (0,   255, 255),
    (0,   0,   255),
    (255, 0,   255),
]

DELAY = 0.01

color_idx = 0

FROM_END = False
LAST_COLOR = COLORS[0]
while True:
    FROM_END = not FROM_END
    target = range(NUM_PIXELS)
    if FROM_END:
        target = reversed(target)

    for pixel in target:
        # Choose a random color only some of the time
        if random.random() > 0.5:
            # Pick a defined color
            #LAST_COLOR = random.choice(COLORS)
            # Randomly generate an RGB color
            LAST_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        np.setPixelColorRGB(pixel, *LAST_COLOR)
        time.sleep(DELAY)
        np.show()
