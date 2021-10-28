'''
    Comment for the file here
'''
import os
import csv
import pygame
from Hexes.hex_field import HexField
from utilities.option_box import OptionBox
from Entities.armies import Armies
from utilities.scrollbar_master.scrollbar import ScrollBar
from utilities.button import Button
from utilities.input_box import InputBox
from utilities import definitions

class MapEditorWindow():
    '''
        Comment for the class here
    '''
    def __init__(self, main_menu, file_name='default'):
        '''
            Comment for the function here
        '''
        self.main_menu = main_menu
        self.surface = pygame.display.get_surface()
        self.file_name = file_name  # Name of the map to open
        self.screen = pygame.display.set_mode((self.surface.get_width(), self.surface.get_height()), pygame.RESIZABLE)  # Define the initial screen size and allow the screen to be resized
        self.selection_bar = RectObj(self.screen.get_width(), definitions.TEXT_HEIGHT)
        self.vertical_scrollbar = ScrollBar(0, pygame.display.get_surface(),"vertical")        # Define the initial location and orientation of the scrollbar
        self.horizontal_scrollbar = ScrollBar(0, pygame.display.get_surface(),"horizontal")     # Define the initial location and orientation of the scrollbar
        self.hex_field = HexField([self.horizontal_scrollbar, self.vertical_scrollbar], self.screen, mode="editor", font=definitions.hex_field_font, offset=definitions.TEXT_HEIGHT)
        #self.armies = Armies([self.horizontal_scrollbar, self.vertical_scrollbar], offset= definitions.TEXT_HEIGHT)
        self.user_input_file = InputBox(0, 0, definitions.TEXT_WIDTH, definitions.TEXT_HEIGHT, self.file_name)    # Input text box (holds the name of the map file stored as CSV)
        
        terrain_names = []
        for terrain in self.hex_field.terrain_list:
            terrain_names.append((terrain.name, terrain.color))

        # Place the various buttons in an orderly row
        self.save_button = Button((self.user_input_file.rect.x + self.user_input_file.rect.width, 0, definitions.TEXT_WIDTH/2, definitions.TEXT_HEIGHT), definitions.GRAY, self.save_map, text="Save Map", **definitions.BUTTON_STYLE)
        self.load_button = Button((self.save_button.rect.x + self.save_button.rect.width, 0, definitions.TEXT_WIDTH/2, definitions.TEXT_HEIGHT), definitions.GRAY, self.load_map, text="Load Map", **definitions.BUTTON_STYLE)
        self.select_terrain_menu = OptionBox(self.load_button.rect.x + self.load_button.rect.width, 0, definitions.TEXT_WIDTH/2, definitions.TEXT_HEIGHT, self.hex_field.current_terrain.color, definitions.DARK_GRAY, terrain_names, self.select_terrain_menu_callback)
        self.select_unit_side_menu = OptionBox(self.select_terrain_menu.rect.x + self.select_terrain_menu.rect.width, 0, definitions.TEXT_WIDTH/2, definitions.TEXT_HEIGHT, definitions.GRAY, definitions.DARK_GRAY, terrain_names, self.select_unit_side_menu_callback)
        self.select_unit_type_menu = OptionBox(self.select_unit_side_menu.rect.x + self.select_unit_side_menu.rect.width, 0, definitions.TEXT_WIDTH/2, definitions.TEXT_HEIGHT, definitions.GRAY, definitions.DARK_GRAY, terrain_names, self.select_unit_type_menu_callback)

        self.control_loop()     # Start the loop for the window


    def select_terrain_menu_callback(self):
        '''
        Comment for the function here
        '''
        self.hex_field.set_terrain_for_name(self.select_terrain_menu.get_selected_option()[0])
        self.select_terrain_menu.color = self.hex_field.current_terrain.color

    def select_unit_side_menu_callback(self):
        '''
        Comment for the function here
        '''

    def select_unit_type_menu_callback(self):
        '''
        Comment for the function here
        '''

    #def select_unit_button_callback(self):
    #    '''
    #        Comment for the function here
    #    '''
    #    self.armies.toggle_menu()
        
    def load_map(self):
        '''
            Load the map that has the name matching what is currently in the input text box from a CSV file into memory
        '''
        file_path = os.path.join(definitions.PROGRAM_ROOT, "maps")
        # If the maps folder does not exist, make it
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # Try to load the file. If it fails, don't crash
        try:
            with open( os.path.join(file_path, self.user_input_file.getText() + ".csv"), newline='') as f:
                reader = csv.reader(f,delimiter=',')
                self.hex_field.clear_field()
                for row in reader:
                    self.hex_field.new_hex(row)
            self.screen = pygame.display.set_mode((self.surface.get_width(), self.surface.get_height()), pygame.RESIZABLE)  # Update the screen size and allow the screen to be resized
        except FileNotFoundError:
            # Inform user that "No file was found with that name."
            pass


    def save_map(self):
        '''
            Save the map currently shown on screen to a CSV file named whatever the user currently has in the input text box
        '''
        file_path = os.path.join(definitions.PROGRAM_ROOT, "maps")
        # If the maps folder does not exist, make it
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        
        # Do I need to add a way to sort the hexes by coordinates before writing them to a file?
        with open(os.path.join(file_path, self.user_input_file.getText() + ".csv"), mode='w') as map_file:
            map_writer = csv.writer(map_file, delimiter=',', lineterminator='\r')
            for hexagon in self.hex_field.field:
                map_writer.writerow([hexagon.x,hexagon.y,hexagon.terrain.name])


    def control_loop(self):
        '''
        Window Loop for the Map Editor
        '''
        self.load_map()
        block_events = False
        while True:     # Main update loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # Handle program exit event
                    self.main_menu()            # Instead of going closing the program, go back to the main menu. This needs to be fixed, as it currently calls main() again.

                # handle events for all the objects
                block_events = self.vertical_scrollbar.handle_event(event)    # Scrollbars must be first to avoid triggering other events when in use
                if block_events:
                    block_events = False
                    break
                block_events = self.horizontal_scrollbar.handle_event(event)  # Scrollbars must be first to avoid triggering other events when in use
                if block_events:
                    block_events = False
                    break
                block_events = self.select_terrain_menu.handle_event(event)
                self.hex_field.handle_event(event)
                #self.armies.handle_event(event)
                self.selection_bar.handle_event(event)
                self.user_input_file.handle_event(event)
                self.save_button.handle_event(event)
                self.load_button.handle_event(event)
                self.select_unit_side_menu.handle_event(event)
                self.select_unit_type_menu.handle_event(event)

            self.vertical_scrollbar.image_dimension = self.hex_field.get_field_dimensions()['height']     # Update the scrollbar with a new image height
            self.horizontal_scrollbar.image_dimension = self.hex_field.get_field_dimensions()['width']    # Update the scrollbar with a new image width

            self.screen.fill(definitions.BG_COLOR)  # Draw the background of the screen
            
            # Draw all the objects on the screen
            self.hex_field.update(self.screen)     # Must be first so that the map does not cover any of the other objects
            self.vertical_scrollbar.update(self.screen)
            self.horizontal_scrollbar.update(self.screen)
            #self.armies.update(self.screen)
            self.selection_bar.update(self.screen)
            self.user_input_file.update(self.screen)
            self.save_button.update(self.screen)
            self.load_button.update(self.screen)
            self.select_terrain_menu.update(self.screen)
            self.select_unit_side_menu.update(self.screen)
            self.select_unit_type_menu.update(self.screen)

            pygame.display.flip()


class RectObj():
    '''
    Wrapper for a generic Rect shape from pygame
    '''
    def __init__(self, width, height):
        self.border = pygame.Rect(0, 0, width, height)
    def handle_event(self,event):
        '''
            Comment for the function here
        '''
    def update(self, screen):
        '''
            Comment for the function here
        '''
        pygame.draw.rect(screen, definitions.BLACK, self.border)
