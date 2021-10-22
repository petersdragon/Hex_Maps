import pygame, pygame_menu, csv, os
from Hexes.hex_field import Hex_Field
from Entities.armies import Armies
from utilities.scrollbar_master.scrollbar import ScrollBar
from utilities.button import Button
from utilities.input_box import InputBox
from utilities import definitions

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 180, 0)
GRAY = (150,150,150)
DARK_GRAY = (75,75,75)
BUTTON_STYLE = {
    "hover_color": GRAY,
    "clicked_color": GREEN,
    "clicked_font_color": BLACK,
    "hover_font_color": BLACK,
}
TERRAIN_BUTTON_STYLE = {
    "font_color": BLACK
}

file_text_height = 32   # Define the height of the input text box (it will hold the map file name)
file_text_width = 200   # Define the width of the input text box (it will hold the map file name)
bg_color = (0, 0, 0)    # Define the background color of the screen to black        

'''
    Comment for the class here
'''
class Map_Editor_Window():
    '''
        Comment for the function here
    '''
    def __init__(self, main_menu, file_name='default'):
        self.main_menu = main_menu
        self.surface = pygame.display.get_surface()
        self.file_name = file_name  # Name of the map to open
        self.objects = []           # List to more easily render objects in the Control Loop
        self.screen = pygame.display.set_mode((self.surface.get_width(), self.surface.get_height()), pygame.RESIZABLE)  # Define the initial screen size and allow the screen to be resized
        self.selection_bar = RectObj(self.screen.get_width(), file_text_height)
        self.vertical_scrollbar = ScrollBar(0, pygame.display.get_surface(),"vertical")        # Define the initial location and orientation of the scrollbar
        self.horizontal_scrollbar = ScrollBar(0, pygame.display.get_surface(),"horizontal")     # Define the initial location and orientation of the scrollbar
        self.hex_field = Hex_Field(50, [self.horizontal_scrollbar, self.vertical_scrollbar], mode="editor", offset=file_text_height)
        self.armies = Armies([self.horizontal_scrollbar, self.vertical_scrollbar], offset=file_text_height)
        self.user_input_file = InputBox(0, 0, file_text_width, file_text_height, self.file_name)    # Input text box (holds the name of the map file stored as CSV)
        
        # Place the various buttons in an orderly row
        self.save_button = Button((self.user_input_file.rect.x + self.user_input_file.rect.width, 0, file_text_width/2, file_text_height), DARK_GRAY, self.save_map, text="Save Map", **BUTTON_STYLE)
        self.load_button = Button((self.save_button.rect.x + self.save_button.rect.width, 0, file_text_width/2, file_text_height), DARK_GRAY, self.load_map, text="Load Map", **BUTTON_STYLE)
        self.select_terrain_button = Button((self.load_button.rect.x + self.load_button.rect.width, 0, file_text_width/2, file_text_height), self.hex_field.current_terrain.color, self.select_terrain_button_callback, text=self.hex_field.current_terrain.name, **TERRAIN_BUTTON_STYLE)
        self.select_unit_button = Button((self.select_terrain_button.rect.x + self.select_terrain_button.rect.width, 0, file_text_width/2, file_text_height), DARK_GRAY, self.select_unit_button_callback, text= "Add Unit", **BUTTON_STYLE)
        
        # Add the objects to the list to be rendered easily in the Control Loop
        self.objects.append(self.hex_field)
        self.objects.append(self.armies)
        self.objects.append(self.selection_bar)
        self.objects.append(self.vertical_scrollbar)
        self.objects.append(self.horizontal_scrollbar)
        self.objects.append(self.user_input_file)
        self.objects.append(self.save_button)
        self.objects.append(self.load_button)
        self.objects.append(self.select_terrain_button)
        self.objects.append(self.select_unit_button)
        
        self.control_loop()     # Start the loop for the window

    '''
        Comment for the function here
    '''
    def select_terrain_button_callback(self):
        self.hex_field.next_terrain()
        self.select_terrain_button.color = self.hex_field.current_terrain.color
        self.select_terrain_button.set_text(self.hex_field.current_terrain.name)

    '''
        Comment for the function here
    '''
    def select_unit_button_callback(self):
        self.armies.toggle_menu()
        
    '''
        Load the map that has the name matching what is currently in the input text box from a CSV file into memory
    '''
    def load_map(self):
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
        except:
            pass

    '''
        Save the map currently shown on screen to a CSV file named whatever the user currently has in the input text box
    '''
    def save_map(self):
        file_path = os.path.join(definitions.PROGRAM_ROOT, "maps")
        # If the maps folder does not exist, make it
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        
        # Do I need to add a way to sort the hexes by coordinates before writing them to a file?
        with open(os.path.join(file_path, self.user_input_file.getText() + ".csv"), mode='w') as map_file:
            map_writer = csv.writer(map_file, delimiter=',', lineterminator='\r')
            for hexagon in self.hex_field.field:
                map_writer.writerow([hexagon.x,hexagon.y,hexagon.terrain.name])

    '''
        Window Loop for the Map Editor
    '''
    def control_loop(self):
        self.load_map()
        while True:     # Main update loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # Handle program exit event
                    self.main_menu()            # Instead of going closing the program, go back to the main menu
                
                for obj in self.objects:        # handle events for all the objects
                    obj.handle_event(event)

            self.vertical_scrollbar.image_dimension = self.hex_field.get_field_dimensions()['height']     # Update the scrollbar with a new image height
            self.horizontal_scrollbar.image_dimension = self.hex_field.get_field_dimensions()['width']    # Update the scrollbar with a new image width

            self.screen.fill(bg_color)  # Draw the background of the screen
            for obj in self.objects:    # Draw all the objects on the screen
                obj.update(self.screen)
            
            pygame.display.flip()

'''
    Wrapper for a generic Rect shape from pygame
'''
class RectObj():
    def __init__(self, width, height):
        self.border = pygame.Rect(0, 0, width, height)
    def handle_event(self,event):
        pass
    def update(self,screen):
        pygame.draw.rect(screen, BLACK, self.border)
