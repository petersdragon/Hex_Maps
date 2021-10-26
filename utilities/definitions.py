'''
    Comment for the file here
'''
from os import path

UTILITIES = path.dirname(path.abspath(__file__))  # Get the path to this file
PROGRAM_ROOT = path.dirname(UTILITIES)               # Get the path to this program

TEXT_HEIGHT = 32        # Define the height of the input text box (it will hold the map file name)
TEXT_WIDTH = 200        # Define the width of the input text box (it will hold the map file name)
BG_COLOR = (0, 0, 0)    # Define the background color of the screen to black
DEPTH = 20

# Mouse input values
LEFT_CLICK = 1
MIDDLE_CLICK = 2
RIGHT_CLICK = 3
SCROLL_UP = 4
SCROLL_DOWN = 5

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255) 
ORANGE = (255, 180, 0)
GRAY = (150,150,150)
DARK_GRAY = (75,75,75)

BUTTON_STYLE = {
    "hover_color": GRAY,
    "clicked_color": GREEN,
    "clicked_font_color": BLACK,
    "hover_font_color": BLACK,
}

TERRAIN_BUTTON_STYLE = {
    "font_color": BLACK
}
