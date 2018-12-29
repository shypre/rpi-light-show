def color_to_rgb(color):
    if isinstance(color, tuple):  # Newer LEDGrid stores (r, g, b) tuple
        return color
    elif not isinstance(color, int):  # Invalid color data
        return (0,0,0)
    b = color & 255
    g = (color >> 8) & 255
    r = (color >> 16) & 255
    return (r,g,b)

def print_led_strip(led_strip):
    line = ""
    for led in led_strip:
        red, green, blue = color_to_rgb(led)
        line += "\x1b[48;2;{r};{g};{b}m  ".format(r=red, g=green, b=blue)
    print(line + "\x1b[0m\x1b[K\n")

'''
def print_led_matrix(led_matrix, first_row_lefttoright = False):
    #Truecolor escape sequences:
    #https://raw.githubusercontent.com/JohnMorales/dotfiles/master/colors/24-bit-color.sh
    for j in range(len(led_matrix)):
        line = ""
        for i in range(len(led_matrix[0])):
            line += "\x1b[48;2;{r};{g};{b}m  ".format(r=led_matrix.get(i, j)[0], g=led_matrix.get(i, j)[1], b=led_matrix.get(i, j)[2])
        print(line + "\x1b[0m\x1b[K")
    print("\n\n", end='')
'''

def print_led_grid(led_grid, first_row_lefttoright = False):
    #Truecolor escape sequences:
    #https://raw.githubusercontent.com/JohnMorales/dotfiles/master/colors/24-bit-color.sh
    for j in range(led_grid.height):
        line = ""
        for i in range(led_grid.width):
            red, green, blue = color_to_rgb(led_grid.get(i, j))
            line += "\x1b[48;2;{r};{g};{b}m  ".format(r=red, g=green, b=blue)
        print(line + "\x1b[0m\x1b[K")
    print("\n", end='')

def print_led_grid_np(led_grid_1d, width, height, first_row_lefttoright = False):
    #Truecolor escape sequences:
    #https://raw.githubusercontent.com/JohnMorales/dotfiles/master/colors/24-bit-color.sh
    for j in range(height):
        line = ""
        for i in range(width):
            red, green, blue = color_to_rgb(led_grid_1d[width*j + i])
            line += "\x1b[48;2;{r};{g};{b}m  ".format(r=red, g=green, b=blue)
        print(line + "\x1b[0m\x1b[K")
    print("\n", end='')
