from Entities.unit import Unit, UnitInfo
import pygame, json

class Armies():
    def __init__(self, surface, offset=0, THIS_FOLDER=''):
        self.unit_info = []
        self.file_path = THIS_FOLDER + "//utilities//unit_info.json"
        self.load_unit_info()
        self.armies = []
        sysfont = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(sysfont, 24)

    def load_unit_info(self):
        with open(self.file_path, newline='') as f:
            obj = json.loads(f.read())
            for unit in obj:
                self.unit_info.append(UnitInfo(**unit))

    def add_unit(self,x,y,team,data):
        self.armies.append(Unit(x,y,team,data))

    def draw_armies(self, surface, x_offset, y_offset):
        for unit in self.armies:
            unit.draw_unit(surface, x_offset, y_offset, self.font)
