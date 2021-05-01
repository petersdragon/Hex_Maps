from math import sin, cos, pi
import pygame

'''
A single hex tile of the grid in OddQ coordinates
'''
class OddQ_Hex():
    '''
        Comment for the function here
    '''
    def __init__(self, x, y, radius, modify, terrain, offset=0):
        assert (x >= 0 and y >= 0), "OddQ coordinate values must be positive because of where drawing starts"
        self.radius = radius
        self.x = x
        self.y = y
        self.terrain = terrain
        self.vertex_count = 6                        # Number of vertices for the polygon. I want hexes.
        self.draw_start = {'x':self.radius, 'y':self.radius+offset}   # Offset to start drawing at (the zero location)
        self.x_pixel = self.x*modify['x1']*self.radius + self.draw_start['x']
        self.y_pixel = (self.x % 2)*modify['x2']*self.radius + self.y*modify['y']*self.radius + self.draw_start['y']
        self.unit = None

    '''
        Comment for the function here
    '''
    def draw_hex(self, surface, mode, x_offset, y_offset, font=None):
        n, r = self.vertex_count, self.radius
        x, y = (self.x_pixel + x_offset, self.y_pixel + y_offset)   # Determine the total offset for the hex
        pygame.draw.polygon(surface, self.terrain.color, [
            (x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n))
            for i in range(n)])
        pygame.draw.polygon(surface, (0,0,0), [
            (x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n))
            for i in range(n)], 3)

        if mode == "editor": 
            text = font.render("("+str(int(self.x))+","+str(int(self.y))+")", True, (0, 0, 0))
            surface.blit(text, (x - self.radius/3, y - self.radius/8)) # create a text suface object, on which text is drawn.

    '''
        Comment for the function here
    '''
    def add_unit(self):
        pass