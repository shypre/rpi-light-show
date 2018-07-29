from np_simplelib import *



COLORS = [
    (255, 255, 255, INTENSITY),
    (255, 0,   0,   INTENSITY),
    (255, 255, 0,   INTENSITY),
    (0,   255, 0,   INTENSITY),
    (0,   255, 255, INTENSITY),
    (0,   0,   255, INTENSITY),
    (255, 0,   255, INTENSITY),
]

color_idx = 0

while True:
    color = COLORS[color_idx % len(COLORS)]
    set_all(color)
    #print(list(map(bin, np._led_data[slice(0,-1)])))
    print(np._led_data[0,-1])
    print(color_idx, "\n")
    color_idx += 1
    np.show()
    time.sleep(DELAY)
    print("\033c")
