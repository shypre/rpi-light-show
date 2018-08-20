def print_leds_grid(led_matrix):
    width = len(led_matrix)
    height = len(led_matrix[0])
    #Truecolor escape sequences:
    #https://raw.githubusercontent.com/JohnMorales/dotfiles/master/colors/24-bit-color.sh
    for row in led_matrix:
        line = ""
        for led in row:
            line += "\x1b[48;2;{r};{g};{b}m  ".format(r=led[0], g=led[1], b=led[2])
        print(line + "\x1b[0m \n")

def print_leds_strip(led_strip):
    line = ""
    for led in led_strip:
        line += "\x1b[48;2;{r};{g};{b}m  ".format(r=led[0], g=led[1], b=led[2])
    print(line + "\x1b[0m \n")