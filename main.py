'''
    Comment for the file here
'''
from os import listdir
from os.path import isfile, join
import pygame
import pygame_menu
from utilities import definitions
from utilities.main_menu import MainMenu
from GUI.map_editor import MapEditorWindow

pygame.init()           # Initialize an instance of pygame

# Creates a list of tuples where the first element is the file name without the extension, the "1" is an arbitrary value to force the menu's dropselect to function in the desired fashion
mapfiles = [(file_name.replace('.csv',''),1) for file_name in listdir(join(definitions.PROGRAM_ROOT, "maps")) if isfile(join(definitions.PROGRAM_ROOT, "maps", file_name))]    # Load file names into memory to allow user to select a map

# Make the initial window the size of the display
SCREEN_WIDTH = round(pygame.display.Info().current_w/1.1)
SCREEN_HEIGHT = round(pygame.display.Info().current_h/1.1)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

def open_map_editor():
    '''
        Comment for the function here
    '''
    MapEditorWindow(main, map_selection.get_value()[0][0])

# https://pygame-menu.readthedocs.io/en/4.0.2/
menu = pygame_menu.Menu('LOTR Menu', SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
#menu.add.button('Start', open_map_editor)
menu.add.button('Edit Map', open_map_editor)
map_selection = menu.add.dropselect('Select Map', mapfiles, 0)
menu.add.button('Exit', pygame_menu.events.EXIT)

main_menu = MainMenu('LOTR Menu', screen)
main_menu.add_button('Edit Maps', open_map_editor)
main_menu.add_button('Exit', pygame_menu.events.EXIT)

def main():
    '''
        Comment for the function here
    '''
    while True:     # Main update loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:               # Handle program exit event
                pygame.quit()
                exit()

            elif event.type == pygame.VIDEORESIZE:
                main_menu.recenter_menu()
                pass
        # Need to handle resize event. Also, if a map is resized before it is closed, the program returns to the menu but keeps the map's window size.
        #menu.mainloop(screen)
        main_menu.update()
        pygame.display.flip()

main()
