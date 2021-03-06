#!/usr/bin/env python3
# This class originally came from pygame_button
# but I made some changes to it

import pygame

class Button(object):
    """
        A fairly straight forward button class.
    """
    def __init__(self, rect, color, function, **kwargs):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.function = function
        self.clicked = False
        self.hovered = False
        self.hover_text = None
        self.clicked_text = None
        self.process_kwargs(kwargs)
        self.render_text()

    def process_kwargs(self, kwargs):
        """
            Various optional customization you can change by passing kwargs.
        """
        settings = {
            "text": None,
            "font": pygame.font.Font(None, 16),
            "call_on_release": True,
            "hover_color": None,
            "clicked_color": None,
            "font_color": pygame.Color("white"),
            "hover_font_color": None,
            "clicked_font_color": None,
            "click_sound": None,
            "hover_sound": None,
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("Button has no keyword: {}".format(kwarg))
        self.__dict__.update(settings)

    def set_text(self, text):
        """
            Comment on function here
            (Added by Peter Moyer April 26, 2021)
        """
        self.text = text
        self.render_text()

    def render_text(self):
        """
            Pre render the button text.
        """
        if self.text:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.font.render(self.text, True, color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.font.render(self.text, True, color)
            self.text = self.font.render(self.text, True, self.font_color)

    def handle_event(self, event):
        """
            The button needs to be passed events from your program event loop.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def on_click(self, event):
        """
            Comment on function here
        """
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                self.function()

    def on_release(self, event):
        """
            Comment on function here
        """
        if self.clicked and self.call_on_release:
            self.function()
        self.clicked = False

    def check_hover(self):
        """
            Comment on function here
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False

    def update(self, surface):
        """
            Update needs to be called every frame in the main loop.
        """
        color = self.color
        text = self.text
        self.check_hover()
        if self.clicked and self.clicked_color:
            color = self.clicked_color
            if self.clicked_font_color:
                text = self.clicked_text
        elif self.hovered and self.hover_color:
            color = self.hover_color
            if self.hover_font_color:
                text = self.hover_text
        surface.fill(pygame.Color("black"), self.rect)
        surface.fill(color, self.rect.inflate(-4, -4))
        if self.text:
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
