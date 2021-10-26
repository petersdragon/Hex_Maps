'''
    https://stackoverflow.com/questions/19877900/tips-on-adding-creating-a-drop-down-selection-box-in-pygame

'''
import pygame
from utilities import definitions

class OptionBox():
    '''
        Comment for the Class here.
    '''
    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, function, selected = 0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.function = function
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1
        self.clicked = False

    def get_selected_option(self):
        '''
            Comment for the Function here.
        '''
        return self.option_list[self.selected]

    def draw(self, screen):
        '''
            Comment for the Function here.
        '''
        pygame.draw.rect(screen, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(screen, definitions.BLACK, self.rect, 2)
        msg = self.font.render(self.option_list[self.selected].name, 1, definitions.BLACK)
        screen.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, terrain in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(screen, terrain.color, rect)
                msg = self.font.render(terrain.name, 1, definitions.BLACK)
                screen.blit(msg, msg.get_rect(center = rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(screen, definitions.BLACK, outer_rect, 2)

    def update(self, screen):
        '''
            Comment for the Function here.
        '''
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False
        
        self.draw(screen)

    def handle_event(self, event):
        '''
            Comment for the Function here.
        '''
        event_complete = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == definitions.LEFT_CLICK:
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            
            elif self.draw_menu and self.active_option >= 0:
                self.selected = self.active_option
                self.draw_menu = False
                self.function()
                event_complete = True

        return event_complete