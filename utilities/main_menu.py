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
        self.title = definitions.main_menu_font.render(title, False, definitions.BLACK)
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
        new_button = Button((0, 0, button_size[0] + definitions.MENU_BUTTON_BUFFER, button_size[1] + definitions.MENU_BUTTON_BUFFER), definitions.GRAY, function, text=button_text, **definitions.MENU_BUTTON_STYLE)
        #self.game_start_button = Button()
        #self.map_editor_button = Button((x, y, definitions.TEXT_WIDTH/2, definitions.TEXT_HEIGHT), definitions.DARK_GRAY, , text="Edit Map", **definitions.BUTTON_STYLE)
        #self.exit_button = Button()
        self.menu_list.append(new_button)
        self.recenter_menu()

    def add_dropselect(self, options):
        '''
            Comment for Function here
        '''
        #new_dropselect = DropSelect(label, options)
        text_height = definitions.main_menu_font.size('ABCDEFGHIJKLMNOPQRSTUVWXYZ')[1]
        new_option_box = OptionBox(0, 0, definitions.OPTION_BOX_LENGTH, text_height + definitions.MENU_BUTTON_BUFFER, definitions.GRAY, definitions.DARK_GRAY, definitions.main_menu_font, options, self.selected_value)
        self.menu_list.append(new_option_box)
        self.recenter_menu()
        return self.selected_value()

    def selected_value(self):
        '''
            Comment for Function here
        '''


    def update(self):
        '''
            Comment for Function here
        '''
        pygame.draw.rect(self.screen, self.title_color, self.title_top_box)
        pygame.draw.rect(self.screen, self.title_color, self.title_bottom_box)
        self.screen.blit(self.title, self.title_location)
        for obj in self.menu_list:
            obj.update(self.screen)

    def handle_events(self, event_list):
        '''
            Comment for Function here
        '''
        for event in event_list:
            if event.type == pygame.VIDEORESIZE:
                self.recenter_menu()
            
            for obj in self.menu_list:
                obj.handle_event(event)


#class DropSelect():
#    '''
#        Comment for Class here
#    '''
#    def __init__(self, label, options):
#        box_size_x = definitions.main_menu_font.size(label)[0]
#        box_size_y = definitions.main_menu_font.size(label)[1] + definitions.OPTION_BOX_LENGTH
#        self.label = pygame.Rect(0, 0, self.screen.get_width(), definitions.TEXT_HEIGHT)
#
#        box_size_x = definitions.main_menu_font.size(label)[0]
#        option_box = OptionBox(0, 0, box_size_x + definitions.MENU_BUTTON_BUFFER, definitions.OPTION_BOX_LENGTH + definitions.MENU_BUTTON_BUFFER, definitions.GRAY, definitions.DARK_GRAY, definitions.main_menu_font, options, self.selected_value)
#
#    def selected_value(self):
#        '''
#            Comment for Function here
#        '''
#
#    def update(self):
#        '''
#            Comment for Function here
#        '''
#
#    def handle_event(self, event):
#        '''
#            Comment for Function here
#        '''
