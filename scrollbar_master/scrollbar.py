#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import os


# To find the path to the assests needed by the ScrollBar
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))    

DEPTH = 20    # 20 pixel indent from edge of screen

class ScrollBar(object):
    def __init__(self, image_dimension, screen, orientation="vertical"):
        self.orientation = orientation      # Dictates whether the scrollbar is horizontal or vertical
        self.image_dimension = image_dimension    # Height of the screen that needs to be scrolled
        self.axis = 0     # The offset of the image in the window due to the scrollbar
        self.axis_change = 0   # How much the scrollbar has changed since the last time it was updated
        self.on_bar = False
        self.mouse_diff = 0
        self.window_resize()

        if self.orientation == "vertical":
            self.border = pygame.Rect(screen.get_width()-DEPTH, 0, DEPTH, screen.get_height())
            self.image_1 = pygame.image.load(os.path.join(THIS_FOLDER, 'assets/up.png')).convert()     # Load the image for the scrollbar's up arrow
            self.image_2 = pygame.image.load(os.path.join(THIS_FOLDER, 'assets/down.png')).convert() # Load the image for the scrollbar's down arrow

        elif self.orientation == "horizontal":
            self.border = pygame.Rect(0, screen.get_height()-DEPTH, screen.get_width(),DEPTH)
            self.image_1 = pygame.image.load(os.path.join(THIS_FOLDER, 'assets/left.png')).convert()     # Load the image for the scrollbar's left arrow
            self.image_2 = pygame.image.load(os.path.join(THIS_FOLDER, 'assets/right.png')).convert()   # Load the image for the scrollbar's right arrow

    def check_events(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.window_resize()
        self.event_handler(event)     # Handle a change in the position of the scrollbar

    def window_resize(self):
        self.SCREEN_WIDTH = pygame.display.get_surface().get_width()    # Width of the window to put the scrollbar in the correct place
        self.SCREEN_HEIGHT = pygame.display.get_surface().get_height()  # Height of the window to put the scrollbar in the correct place
        bar_length = 50                                                 # Length of the bit of the bar that can be scrolled

        if self.orientation == "vertical":
            self.bar_rect = pygame.Rect(self.SCREEN_WIDTH - DEPTH, DEPTH, DEPTH, bar_length)                    # scrollbar block location
            self.bar_1 = pygame.Rect(self.SCREEN_WIDTH - DEPTH, 0, DEPTH, DEPTH)                                # bar_1 location, corresponding to image_1
            self.bar_2 = pygame.Rect(self.SCREEN_WIDTH - DEPTH, self.SCREEN_HEIGHT - DEPTH*2, DEPTH, DEPTH)     # bar_2 location, corresponding to image_2
            self.border = pygame.Rect(self.SCREEN_WIDTH - DEPTH, 0, DEPTH, self.SCREEN_HEIGHT)                  # Border to make it so that the image does not appear behind the scrollbar

        elif self.orientation == "horizontal":
            self.bar_rect = pygame.Rect(DEPTH, self.SCREEN_HEIGHT - DEPTH, bar_length, DEPTH)                   # scrollbar block location
            self.bar_1 = pygame.Rect(0,self.SCREEN_HEIGHT - DEPTH, DEPTH, DEPTH)                                # bar_1 location, corresponding to image_1
            self.bar_2 = pygame.Rect(self.SCREEN_WIDTH - DEPTH*2, self.SCREEN_HEIGHT - DEPTH, DEPTH, DEPTH)     # bar_2 location, corresponding to image_2
            self.border = pygame.Rect(0, self.SCREEN_HEIGHT - DEPTH, self.SCREEN_WIDTH, DEPTH)                  # Border to make it so that the image does not appear behind the scrollbar

    def update(self,screen):
        self.axis += self.axis_change
        if self.axis > 0:
            self.axis = 0
        pygame.draw.rect(screen, (0,0,0), self.border)
        pygame.draw.rect(screen, (150,150,150), self.border,3)

        if self.orientation == "vertical":
            height_diff = self.image_dimension - self.SCREEN_HEIGHT # The difference between the height of the image and the height of the screen.
                                                                    # This is used to determine how much the screen can scroll
            if height_diff < 0:             # If the image is smaller than the screen, there is no height difference
                height_diff = 0

            if self.axis < -height_diff:    # If the scrollbar is scrolled farther than the image goes, limit it to keep the image onscreen
                self.axis = -height_diff
            scroll_length = self.SCREEN_HEIGHT - self.bar_rect.height - DEPTH*2
            bar_half_length = self.bar_rect.height / 2 + DEPTH
            
            if self.on_bar:
                pos = pygame.mouse.get_pos()                                # Pixel position of the mouse on the screen
                self.bar_rect.y = pos[1] - self.mouse_diff                  # Determine if the mouse in on the scrollbar
                if self.bar_rect.top < DEPTH:                               # If the scrollbar is cutting into the image, don't let it
                    self.bar_rect.top = DEPTH
                elif self.bar_rect.bottom > (self.SCREEN_HEIGHT - DEPTH):   # If the scrollbar is cutting into the image, don't let it
                    self.bar_rect.bottom = self.SCREEN_HEIGHT - DEPTH
                self.axis = int(height_diff / (scroll_length * 1.0) * (self.bar_rect.centery - bar_half_length) * -1)
            else:
                # Don't crash if the height_diff is exactly zero
                try:
                    self.bar_rect.centery =  scroll_length / (height_diff * 1.0) * (self.axis * -1) + bar_half_length
                except:
                    pass

        elif self.orientation == "horizontal":
            height_diff = self.image_dimension - self.SCREEN_WIDTH  # The difference between the width of the image and the width of the screen.
                                                                    # This is used to determine how much the screen can scroll
            if height_diff < 0:             # If the image is smaller than the screen, there is no height difference
                height_diff = 1
            if self.axis < -height_diff:    # If the scrollbar is scrolled farther than the image goes, limit it to keep the image onscreen
                self.axis = -height_diff
            scroll_length = self.SCREEN_WIDTH - self.bar_rect.width - DEPTH*2
            bar_half_length = self.bar_rect.width / 2 + DEPTH

            if self.on_bar:
                pos = pygame.mouse.get_pos()                            # Pixel position of the mouse on the screen
                self.bar_rect.x = pos[0] - self.mouse_diff              # Determine if the mouse in on the scrollbar
                if self.bar_rect.left < DEPTH:                          # If the scrollbar is cutting into the image, don't let it
                    self.bar_rect.left = DEPTH  
                elif self.bar_rect.right > (self.SCREEN_WIDTH - DEPTH): # If the scrollbar is cutting into the image, don't let it
                    self.bar_rect.right = self.SCREEN_WIDTH - DEPTH
                self.axis = int(height_diff / (scroll_length * 1.0) * (self.bar_rect.centerx - bar_half_length) * -1)
            else:
                try:    # Don't crash if the height_diff is exactly zero
                    self.bar_rect.centerx =  scroll_length / (height_diff * 1.0) * (self.axis * -1) + bar_half_length
                except: # No graphical benefit to setting anything different
                    pass
        self.draw(screen)
        
    def event_handler(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.bar_rect.collidepoint(pos):     # If the mouse is pressing down on the scrollbar, scroll with the mouse
                self.mouse_diff = pos[1] - self.bar_rect.y
                self.on_bar = True
            elif self.bar_1.collidepoint(pos):      # If the mouse is pressing down on image_1, move the scrollbar towards it
                self.axis_change = 5
            elif self.bar_2.collidepoint(pos):      # If the mouse is pressing down on image_2, move the scrollbar towards it
                self.axis_change = -5
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.axis_change = 0
            self.on_bar = False
                
    def draw(self,screen):
        pygame.draw.rect(screen, (197,194,197), self.bar_rect)  # Draw the scrollbar rectangle on the screen
        if self.orientation == "vertical":
            screen.blit(self.image_1,(self.SCREEN_WIDTH - DEPTH,0))                             # Draw the bar_1_image
            screen.blit(self.image_2,(self.SCREEN_WIDTH - DEPTH, self.SCREEN_HEIGHT - DEPTH*2)) # Draw the bar_2_image

        elif self.orientation == "horizontal":
            screen.blit(self.image_1,(0,self.SCREEN_HEIGHT - DEPTH))                            # Draw the bar_1_image
            screen.blit(self.image_2,(self.SCREEN_WIDTH - DEPTH*2, self.SCREEN_HEIGHT - DEPTH)) # Draw the bar_2_image
