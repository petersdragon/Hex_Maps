'''
One of my major resources for this project
https://www.redblobgames.com/grids/hexagons/codegen/output/lib.py
Generated code -- CC0 -- No Rights Reserved -- http://www.redblobgames.com/grids/hexagons/ 
For my cubic coordinates, I defined my hexes to be x,z,y instead of x,y,z.
This made it so that both the OddQ x and y value was also the Cubic x and y value
'''
from _typeshed import NoneType
import json
from os import path
from math import sqrt
import pygame
from pygame.constants import DOUBLEBUF
from Hexes.cube_hex import Cube_Hex
from Hexes.oddq_hex import OddQ_Hex
from Hexes.terrain import Terrain
from utilities import definitions


class Hex_Field():
    '''
        Comment for the class here
    '''
    def __init__(self, radius, scrollbars, screen, mode=None, offset=0):
        self.modify = {'x1':1.5, 'x2':sqrt(3)/2, 'y':sqrt(3)} # Modifiers to line the hexes up into a uniform, clean grid
        self.surface = pygame.display.get_surface()
        self.radius = radius         # The radius (pixels from center to vertex) that I want my hexes to have
        self.scrollbar = scrollbars
        self.screen = screen
        self.vertical_hexes = 1
        self.horizontal_hexes = 1
        self.field = []
        self.offset = offset
        self.file_path =  path.join(definitions.UTILITIES, "terrain_info.json")
        self.terrain_list = []
        self.load_terrain_list()
        self.current_terrain = self.terrain_list[0]
        self.new_hex([0,0,self.current_terrain.name])
        self.paint_terrain = False
        
        # The change in coordinates that takes place when moving into a hex that shares an edge
        self.hex_edges = [Cube_Hex(1, 0, -1, self.radius), Cube_Hex(1, -1, 0, self.radius), Cube_Hex(0, -1, 1, self.radius),
             Cube_Hex(-1, 0, 1, self.radius), Cube_Hex(-1, 1, 0, self.radius), Cube_Hex(0, 1, -1, self.radius)]             
        
        # The change in coordinates that takes place when moving into a hex that is straight out from a vertex of the hex
        self.hex_diagonals = [Cube_Hex(2, -1, -1, self.radius), Cube_Hex(1, -2, 1, self.radius), Cube_Hex(-1, -1, 2, self.radius), 
            Cube_Hex(-2, 1, 1, self.radius), Cube_Hex(-1, 2, -1, self.radius), Cube_Hex(1, 1, -2, self.radius)]
        
        self.mode = mode
        sysfont = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(sysfont, 24)

    def add_row(self):
        '''
            Comment for the function here
        '''
        for x in range(self.horizontal_hexes):
            self.field.append(OddQ_Hex(x=x, y=self.vertical_hexes, radius=self.radius, modify=self.modify, terrain=self.terrain_list[0], offset=self.offset))
        self.vertical_hexes += 1

    def add_column(self):
        '''
            Comment for the function here
        '''
        for y in range(self.vertical_hexes):
            self.field.append(OddQ_Hex(x=self.horizontal_hexes, y=y, radius=self.radius, modify=self.modify,terrain=self.terrain_list[0],offset=self.offset))
        self.horizontal_hexes += 1

    def remove_row(self):
        '''
            Comment for the function here
        '''
        if self.vertical_hexes > 1:
            self.vertical_hexes -= 1
            self.field = [hexagon for hexagon in self.field if hexagon.y < self.vertical_hexes]

    def remove_column(self):
        '''
            Comment for the function here
        '''
        if self.horizontal_hexes > 1:
            self.horizontal_hexes -= 1
            self.field = [hexagon for hexagon in self.field if hexagon.x < self.horizontal_hexes]

    def clear_field(self):
        '''
            Comment for the function here
        '''
        self.horizontal_hexes = 1
        self.vertical_hexes = 1
        self.field = [] # Empty the hex field

    def load_terrain_list(self):
        '''
            Comment for the function here
        '''
        with open(self.file_path, newline='') as f:
            obj = json.loads(f.read())
            for terrain in obj:
                self.terrain_list.append(Terrain(**terrain))

    def new_hex(self, data):
        '''
            Comment for the function here
        '''
        if int(data[0])+1 > self.horizontal_hexes:
            self.horizontal_hexes = int(data[0])+1
        if int(data[1])+1 > self.vertical_hexes:
            self.vertical_hexes = int(data[1])+1
        terrain = next(x for x in self.terrain_list if x.name == data[2])
        self.field.append(OddQ_Hex(x=int(data[0]), y=int(data[1]), radius=self.radius, modify=self.modify, offset=self.offset, terrain=terrain))
    
    def update(self, surface):
        '''
            Comment for the function here
        '''
        for hexagon in self.field:
            hexagon.draw_hex(surface, self.mode, self.scrollbar[0].axis, self.scrollbar[1].axis, self.font)
            

    def next_terrain(self):
        '''
            Comment for the function here
        '''
        index = self.terrain_list.index(self.current_terrain)+1
        if index >= len(self.terrain_list):
            index = 0
        self.current_terrain = self.terrain_list[index]
        return self.current_terrain

    def set_terrain_for_name(self, name):
        '''
            Set the terrain based on name.
            Currently utilizes next_terrain function, which was used in the old method. Replace it with a proper search algorithm.
        '''
        if name != self.current_terrain.name:
            initial_terrain = self.current_terrain
            self.next_terrain()
            while initial_terrain != self.current_terrain.name:
                self.next_terrain()
                if self.current_terrain.name == name:
                    return -1

    def hex_clicked(self):
        '''
            Comment for the function here
        '''
        (x, y) = pygame.mouse.get_pos() #get mouse coordinates
        # get the center of the hex, the subtract the positions. If the distance is less than the radius, then the hex was clicked
        for hexagon in self.field:
            x_pos = abs(hexagon.x_pixel + self.scrollbar[0].axis - x)
            y_pos = abs(hexagon.y_pixel + self.scrollbar[1].axis - y)

            distance = sqrt(x_pos**2 + y_pos**2)    # Pythagorean's theorem

            if distance < self.radius*0.8:  # multiply by constant to constrain the radius to inside the visible hex, so that the hexes never overlap their radii
                return hexagon

    def handle_event(self, event):
        '''
            Comment for the function here
        '''
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == definitions.LEFT_CLICK:
            self.paint_terrain = True

        if event.type == pygame.MOUSEMOTION and self.paint_terrain or event.type == pygame.MOUSEBUTTONUP:
            # hex_clicked will return None when the cursor is on the edge of a hex, over no hex, or the user moves the cursor very quickly.
            try:
                hexagon = self.hex_clicked()
                hexagon.terrain = self.current_terrain   # set the terrain type of the hex
            except AttributeError:
                '''
                   Do something useful here.
                '''

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == definitions.RIGHT_CLICK:
            try:
                hexagon = self.hex_clicked()
                if hexagon.unit is None:
                    hexagon.addUnit()
            except AttributeError:
                '''
                   Do something useful here.
                '''

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.add_row()        # Add a row of hexes to the field

            elif event.key == pygame.K_UP:
                self.remove_row()     # Remove a row of hexes from the field

            elif event.key == pygame.K_LEFT:
                self.remove_column()  # Remove a column of hexes from the field

            elif event.key == pygame.K_RIGHT:
                self.add_column()     # Add a row of hexes to the field

        # Always check to see if paint_terrain needs to be false.
        if event.type == pygame.MOUSEBUTTONUP:
            self.paint_terrain = False

    def get_field_dimensions(self):
        '''
            Return how many hexes tall and how many hexes wide the field is
        '''
        field_height = self.vertical_hexes*self.radius*self.modify['y'] + 2*self.radius         # Determine the height of the hex field
        field_width =  self.horizontal_hexes*self.radius*self.modify['x1'] + 1.5*self.radius    # Determine the width of the hex field
        field = {'height':field_height, 'width':field_width}
        return field

    # Return the sum of the coordinates of two hexes
#    def hex_add(self, hexA, hexB):
#        return Cube_Hex(hexA.x + hexB.x, hexA.y + hexB.y, hexA.z + hexB.z, self.radius)

    # Subtract the coordinates of hex b from hex a (returns coordinate hexA minus hexB)
#    def hex_subtract(self, hexA, hexB):
#        return Cube_Hex(hexA.x - hexB.x, hexA.y - hexB.y, hexA.z - hexB.z, self.radius)

    # Scale the coordinates of a Cube_Hex_Tile by a constant (returns a*k)
#    def hex_scale(self, hexA, k):
#        return Cube_Hex(hexA.x * k, hexA.y * k, hexA.z * k, self.radius)

    # Returns the change in coordinates when moving across an edge in a given direction
#    def hex_direction(self, direction):
#        return self.hex_edges[direction]

    # Returns the coordinates of the hex adjacent to the current hex in a given edge's direction
#    def hex_edge_neighbor(self, hexagon, direction):
#        return self.hex_add(hexagon, self.hex_direction(direction))

    # Returns the coordinates of the hex adjacent to the current hex in a given vertex's direction 
#    def hex_diagonal_neighbor(self, hexagon, direction):
#        return self.hex_add(hexagon, self.hex_diagonals[direction])

    # Returns the length of the line from the hex to the origin (0,0,0)
#    def hex_length(self, hexagon):
#        return (abs(hexagon.x) + abs(hexagon.y) + abs(hexagon.z)) // 2

    # Returns the coordinate distance between two hexes
#    def hex_distance(self, hexA, hexB):
#        return self.hex_length(self.hex_subtract(hexA, hexB))

#    def cube_to_oddq(cubeHex):
#        col = cubeHex.x
#        row = cubeHex.y + (cubeHex.x - (cubeHex.x&1)) / 2
#        return OffsetCoord(col, row)

#    def oddq_to_cube(self, oddqHex):
#        x = oddqHex.col
#        y = oddqHex.row - (oddqHex.col - (oddqHex.col&1)) / 2
#        z = -x-y
#        return Cube_Hex(x, z, y, self.radius)

#    def oddq_coord_to_cube(self, x, z):
#        return Cube_Hex(x, -x-z, (x-z&1)/2, self.radius)
