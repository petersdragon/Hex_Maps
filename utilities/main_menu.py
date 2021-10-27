'''
    Comment for File here
'''

import pygame
from utilities.option_box import OptionBox
from utilities import definitions
from utilities.option_box import OptionBox
from utilities.button import Button


class MainMenu():
    '''
        Comment for Class here
    '''
    def __init__(self, title, screen):
        self.screen = screen
        self.screen_center = (self.screen.get_width()//2, self.screen.get_height()//2)
        self.title = definitions.main_menu_font.render(title, False, definitions.WHITE)
        self.title_location = (definitions.TEXT_HEIGHT,definitions.TEXT_HEIGHT)
        self.title_top_box = pygame.Rect(0, 0, self.screen.get_width(), definitions.TEXT_HEIGHT)
        self.title_bottom_box = pygame.Rect(0, 0, self.screen.get_width()//4, definitions.TEXT_HEIGHT*2)
        self.title_color = definitions.GRAY
        self.menu_list = []

    def recenter_menu(self):
        '''
            Comment for Function here
        '''
        self.screen_center = (self.screen.get_width()//2, self.screen.get_height()//2)
        text_height = definitions.main_menu_font.size('ABCDEFGHIJKLMNOPQRSTUVWXYZ')[1]
        index = 0
        for obj in self.menu_list:
            obj.rect.centerx = self.screen_center[0]
            obj.rect.centery = self.screen_center[1] + (text_height + definitions.MENU_BUTTON_BUFFER)*index
            index += 1

    def add_button(self, button_text, function):
        '''
            Comment for Function here
        '''
        button_size = definitions.main_menu_font.size(button_text)
        new_button = Button((0, 0, button_size[0] + definitions.MENU_BUTTON_BUFFER, button_size[1] + definitions.MENU_BUTTON_BUFFER), definitions.DARK_GRAY, definitions.GRAY, text=button_text, **definitions.MENU_BUTTON_STYLE)
        #self.game_start_button = Button()
        #self.map_editor_button = Button((x, y, definitions.TEXT_WIDTH/2, definitions.TEXT_HEIGHT), definitions.DARK_GRAY, , text="Edit Map", **definitions.BUTTON_STYLE)
        #self.exit_button = Button()
        self.menu_list.append(new_button)
        self.recenter_menu()

    def add_dropselect(self, options):
        '''
            Comment for Function here
        '''
        #self.map_selection_box = OptionBox(self.load_button.rect.x + self.load_button.rect.width, 0, definitions.TEXT_WIDTH/2, definitions.TEXT_HEIGHT, self.hex_field.current_terrain.color, definitions.GRAY, definitions.menus_font, self.hex_field.terrain_list, self.select_terrain_menu_callback)
        
    def update(self):
        '''
            Comment for Function here
        '''
        pygame.draw.rect(self.screen, self.title_color, self.title_top_box)
        pygame.draw.rect(self.screen, self.title_color, self.title_bottom_box)
        self.screen.blit(self.title, self.title_location)
        for obj in self.menu_list:
            obj.update(self.screen)

    def handle_event(self, event):
        '''
            Comment for Function here
        '''


    # Main menu will have:
    #   A Title
    #   Button for starting a game
    #   Button for Editing a Map
    #   An optionbox for selecting the map
    #   Button to Exit
