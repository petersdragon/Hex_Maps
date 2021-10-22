import pygame, pygame_menu
from utilities import definitions
from GUI.map_editor import Map_Editor_Window
from GUI.map_selector import Map_Selector_Window

pygame.init()           # Initialize an instance of pygame

SCREEN_WIDTH, SCREEN_HEIGHT = round(pygame.display.Info().current_w/1.1), round(pygame.display.Info().current_h/1.1) # Make the initial window the size of the display
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def open_map_editor():
    Map_Editor_Window(main)

def open_map_selector():
    Map_Selector_Window()

# https://pygame-menu.readthedocs.io/en/4.0.2/
menu = pygame_menu.Menu('LOTR Menu', SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
#menu.add.button('Start', map_editor_window)
menu.add.button('Map Editor', open_map_editor)
menu.add.button('Select Map (Coming soon)', open_map_selector)
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