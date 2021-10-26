'''
    Comment for the file here
'''
import pygame
from utilities import definitions
class Unit():
    '''
        Comment for the class here
    '''
    def __init__(self,team, unit_info, x, y, radius, modify):
        self.team = team
        self.unit_info = unit_info
        self.x = x
        self.y = y
        self.radius = radius
        self.x_pixel = self.x*modify['x1']*self.radius + self.draw_start['x']
        self.y_pixel = (self.x % 2)*modify['x2']*self.radius + self.y*modify['y']*self.radius + self.draw_start['y']
    
    def draw_unit(self, surface, x_offset, y_offset, color=definitions.WHITE, font=None):
        '''
            Comment for the function here
        '''
        #circle(surface, color, center, radius, width=0, draw_top_right=None, draw_top_left=None, draw_bottom_left=None, draw_bottom_right=None)        
        x, y = (self.x_pixel + x_offset, self.y_pixel + y_offset)   # Determine the total offset for the hex
        pygame.draw.circle(surface,color,[x,y],self.radius)
#        text = font.render("("+str(int(self.x))+","+str(int(self.y))+")", True, (0, 0, 0))
        text = font.render(self.unit_info.side + self.unit_info.armor, True, definitions.BLACK)
        surface.blit(text, (x - self.radius/3, y - self.radius/8)) # create a text suface object, on which text is drawn.
#        pygame.draw.circle(surface,color,[x,y],self.radius,3)
#        pygame.draw.polygon(surface, self.terrain.color, [
#            (x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n))
#            for i in range(n)])
#        pygame.draw.polygon(surface, (0,0,0), [
#            (x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n))
#            for i in range(n)], 3)

class UnitInfo():
    '''
        Comment for the class here
    '''
    def __init__(self, side, armor, melee_attack, melee_defend, archer_attack, archer_defend, movement):
        self.side = side
        self.armor = armor
        self.melee_attack = melee_attack
        self.melee_defend = melee_defend
        self.archer_attack = archer_attack
        self.archer_defend = archer_defend
        self.movement = movement
