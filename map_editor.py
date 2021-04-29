import pygame, pygame_menu, csv, sys, os
from pygame import Rect
from Hexes.hex_field import Hex_Field
from Entities.armies import Armies
from scrollbar_master.scrollbar import ScrollBar
from utilities.button import Button
from utilities.input_box import InputBox

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

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__)) # Get the path to the program
file_text_height = 32   # Define the height of the input text box (it will hold the map file name)
file_text_width = 200   # Define the width of the input text box (it will hold the map file name)
bg_color = (0, 0, 0)    # Define the background color of the screen to black


class Map_Editor_Window():
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.file_name = 'default'
        self.hex_field = Hex_Field(self.surface,mode="editor",offset=file_text_height,THIS_FOLDER=THIS_FOLDER)
        self.armies = Armies(self.surface, offset=file_text_height, THIS_FOLDER=THIS_FOLDER)
        self.screen = pygame.display.set_mode((self.surface.get_width(), self.surface.get_height()), pygame.RESIZABLE)  # Define the initial screen size and allow the screen to be resized
        self.selectionBar = Rect(0, 0, self.screen.get_width(), file_text_height)
        self.vertical_scrollbar = ScrollBar(self.hex_field.get_field_dimensions()['height'], pygame.display.get_surface(),"vertical")        # Define the initial location and orientation of the scrollbar
        self.horizontal_scrollbar = ScrollBar(self.hex_field.get_field_dimensions()['width'], pygame.display.get_surface(),"horizontal")     # Define the initial location and orientation of the scrollbar
        self.user_input_file = InputBox(0, 0, file_text_width, file_text_height, self.file_name)    # Input text box (holds the name of the map file stored as CSV)
        self.save_button = Button((self.user_input_file.rect.x + self.user_input_file.rect.width, 0, file_text_width/2, file_text_height), DARK_GRAY, self.save_map, text="Save Map", **BUTTON_STYLE)
        self.load_button = Button((self.save_button.rect.x + self.save_button.rect.width, 0, file_text_width/2, file_text_height), DARK_GRAY, self.load_map, text="Load Map", **BUTTON_STYLE)
        self.select_terrain_button = Button((self.load_button.rect.x + self.load_button.rect.width, 0, file_text_width/2, file_text_height), self.hex_field.current_terrain.color, self.select_terrain_button_callback, text=self.hex_field.current_terrain.name, **TERRAIN_BUTTON_STYLE)
        self.control_loop()     # Start the loop for the window

    def select_terrain_button_callback(self):
        self.hex_field.next_terrain()
        self.select_terrain_button.color = self.hex_field.current_terrain.color
        self.select_terrain_button.set_text(self.hex_field.current_terrain.name)

    def load_map(self):
        file_path = THIS_FOLDER + "\maps\\"
        # If the maps folder does not exist, make it
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # Try to load the file. If it fails, don't crash
        try:
            with open(file_path + self.user_input_file.getText() + ".csv", newline='') as f:
                reader = csv.reader(f,delimiter=',')
                self.hex_field.clear_field()
                for row in reader:
                    self.hex_field.new_hex(row)
            self.screen = pygame.display.set_mode((self.surface.get_width(), self.surface.get_height()), pygame.RESIZABLE)  # Update the screen size and allow the screen to be resized
        except:
            pass

    def save_map(self):
        file_path = THIS_FOLDER + "\maps\\"
        # If the maps folder does not exist, make it
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        
        # Do I need to add a way to sort the hexes by coordinates before writing them to a file?
        with open(file_path + self.user_input_file.getText() + ".csv", mode='w') as map_file:
            map_writer = csv.writer(map_file, delimiter=',', lineterminator='\r')
            for hexagon in self.hex_field.field:
                map_writer.writerow([hexagon.x,hexagon.y,hexagon.terrain.name])

    def control_loop(self):
        while True:     # Main update loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # Handle program exit event
                    quit()
                    exit()

                elif event.type == pygame.MOUSEBUTTONUP:
                        self.hex_field.mouse_click_event(event, self.horizontal_scrollbar.axis, self.vertical_scrollbar.axis)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:      
                        self.hex_field.add_row()        # Add a row of hexes to the field

                    elif event.key == pygame.K_UP:
                        self.hex_field.remove_row()     # Remove a row of hexes from the field

                    elif event.key == pygame.K_LEFT:
                        self.hex_field.remove_column()  # Remove a column of hexes from the field

                    elif event.key == pygame.K_RIGHT:
                        self.hex_field.add_column()     # Add a row of hexes to the field
                
                    self.vertical_scrollbar.image_dimension = self.hex_field.get_field_dimensions()['height']     # Update the scrollbar with a new image height
                    self.horizontal_scrollbar.image_dimension = self.hex_field.get_field_dimensions()['width']    # Update the scrollbar with a new image width

                self.user_input_file.handle_event(event)
                self.save_button.handle_event(event)
                self.load_button.handle_event(event)
                self.select_terrain_button.handle_event(event)
                self.vertical_scrollbar.handle_event(event)
                self.horizontal_scrollbar.handle_event(event)

            self.screen.fill(bg_color)                 # Draw the background of the screen
            self.hex_field.draw_hex_field(self.screen, self.horizontal_scrollbar.axis, self.vertical_scrollbar.axis)    # Draw the hex field on the screen
            pygame.draw.rect(self.screen,BLACK,self.selectionBar)
            self.user_input_file.update(self.screen)        # Draw the User Input File text box on the screen
            self.save_button.update(self.screen)            # Draw the save button on the screen
            self.load_button.update(self.screen)            # Draw the load button on the screen
            self.select_terrain_button.update(self.screen)  # Draw the select terrain button on the screen
            self.horizontal_scrollbar.update(self.screen)   # Update and draw the horizontal scrollbar
            self.vertical_scrollbar.update(self.screen)     # Update and draw the vertical scrollbar
            
            pygame.display.flip()

