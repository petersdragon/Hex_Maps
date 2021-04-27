import pygame, pygame_menu
import itertools
from map_editor import Map_Editor_Window

pygame.init()           # Initialize an instance of pygame
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w //2, pygame.display.Info().current_h //2 # Make the initial window half the width and height of the display
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def open_map_editor():
    Map_Editor_Window()

# https://pygame-menu.readthedocs.io/en/4.0.2/
menu = pygame_menu.Menu('LOTR Menu', SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
#menu.add.button('Start', map_editor_window)
menu.add.button('Map Editor', open_map_editor)
menu.add.button('Exit', pygame_menu.events.EXIT)

while True:     # Main update loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:               # Handle program exit event
            pygame.quit()
            exit()

    menu.mainloop(surface)
    pygame.display.flip()

