from np_simplelib import *
import time
from random import *

def incr_brightness():
    for i in range(NUM_PIXELS):
        choose_color = randint(0,2)
        color = [0, 0, 0]
        color[choose_color] = i
        np.setPixelColorRGB(i, *color)
        np.show()
        time.sleep(0.002)

def rgb_steps():
    pixel_nodes = [0]
    last_pixel_node_distance = 1
    for i in range(1, NUM_PIXELS-7):
        if last_pixel_node_distance <= 6:
            last_pixel_node_distance += 1
            continue
        if random() > 0.5:
            pixel_nodes.append(i)
            last_pixel_node_distance = 1
    pixel_nodes.append(NUM_PIXELS-1)
    pixels_rgb = [[0] * 3 for x in range(NUM_PIXELS)]
    for i in pixel_nodes:
        for j in range(3):
            pixels_rgb[i][j] = randint(1,255)
        pixels_rgb[i] = list(rgb_normalize(*pixels_rgb[i]))
    prev_pos = 0
    for pos in pixel_nodes[1:len(pixel_nodes)]:
        print(prev_pos,pos)
        for i in range(1, pos-prev_pos):
            print(i)
            pixels_rgb[i+prev_pos][0] = int((i*(pixels_rgb[pos][0]-pixels_rgb[prev_pos][0])/(pos-prev_pos))+pixels_rgb[prev_pos][0])
            pixels_rgb[i+prev_pos][1] = int((i*(pixels_rgb[pos][1]-pixels_rgb[prev_pos][1])/(pos-prev_pos))+pixels_rgb[prev_pos][1])
            pixels_rgb[i+prev_pos][2] = int((i*(pixels_rgb[pos][2]-pixels_rgb[prev_pos][2])/(pos-prev_pos))+pixels_rgb[prev_pos][2])
        prev_pos = pos
    for i in range(NUM_PIXELS):
        np.setPixelColorRGB(i, *pixels_rgb[i])
    np.show()

while True:
    rgb_steps()
    time.sleep(1)

