import pygame, pygame_menu
from utilities import definitions
from GUI.map_editor import Map_Editor_Window
from os import listdir
from os.path import isfile, join

# Creates a list of tuples where the first element is the file name without the extension, the second is an arbitrary value to force the menu's dropselect to function in the desired fashion
mapfiles = [(file_name.replace('.csv',''),1) for file_name in listdir(join(definitions.PROGRAM_ROOT, "maps")) if isfile(join(definitions.PROGRAM_ROOT, "maps", file_name))]    # Load file names into memory to allow user to select a map

pygame.init()           # Initialize an instance of pygame
SCREEN_WIDTH, SCREEN_HEIGHT = round(pygame.display.Info().current_w/1.1), round(pygame.display.Info().current_h/1.1) # Make the initial window the size of the display
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def open_map_editor():
    Map_Editor_Window(main, map_selection.get_value()[0][0])

# https://pygame-menu.readthedocs.io/en/4.0.2/
menu = pygame_menu.Menu('LOTR Menu', SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
#menu.add.button('Start', open_map_editor)
menu.add.button('Edit Map', open_map_editor)
map_selection = menu.add.dropselect('Select Map', mapfiles, 0)
menu.add.button('Exit', pygame_menu.events.EXIT)

def main():
    while True:     # Main update loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:               # Handle program exit event
                pygame.quit()
                exit()
        # Need to handle resize event. If a map is resized before it is closed, the program returns to the menu but keeps the map's window size.
        menu.mainloop(surface)
        pygame.display.flip()

main()