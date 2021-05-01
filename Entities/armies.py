from Entities.unit import Unit, UnitInfo
import pygame, json
from utilities.popup_menu.gamelib.popup_menu import NonBlockingPopupMenu

class Armies():
    def __init__(self, scrollbars, offset=0, THIS_FOLDER=''):
        self.scrollbar = scrollbars
        self.unit_info = []
        self.file_path = THIS_FOLDER + "//utilities//unit_info.json"
        self.unit_entry = []
        self.load_unit_info()
        self.armies = []
        sysfont = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(sysfont, 24)
        self.unit_menu = NonBlockingPopupMenu(self.unit_entry)
        self.menu_visible = False

    def load_unit_info(self):
        with open(self.file_path, newline='') as f:
            obj = json.loads(f.read())
            for unit in obj:
                self.unit_info.append(UnitInfo(**unit))
            # Build menu
            sides = list(set([x['side'] for x in obj])) # Get the unique sides in the list of unit_info
            for side in sides:
                armors = list(set([x['armor'] for x in obj if x['side'] == side]))    # Get the unique armors for each side in the list of unit_info
                self.unit_entry.append(side)
                armor_entry = []
                for armor in armors:
                    type_entry = []
                    item = [x for x in obj if x['side'] == side and x['armor'] == armor][0]
                    # Allow Archer option if Archer_Attack > 0, Allow Melee option if Melee_Attack > 0 
                    if item['archer_attack'] > 0:
                        type_entry.append("Archer")
                    if item['melee_attack'] > 0:
                        type_entry.append("Melee")
                    if len(type_entry) > 0:
                        armor_entry.append(armor)
                        armor_entry.append(type_entry)
                self.unit_entry.append(armor_entry)

    def add_unit(self,x,y,team,data):
        self.armies.append(Unit(x,y,team,data))

    def update(self, surface):
        for unit in self.armies:
            unit.draw_unit(surface, self.scrollbar[0].axis, self.scrollbar[1].axis, self.font)
        self.unit_menu.draw()

    def toggle_menu(self):
        if self.menu_visible == False:
            self.unit_menu.show()
            self.menu_visible = True
        elif self.menu_visible == True:
            self.unit_menu.hide()
            self.menu_visible = False

    def handle_event(self, event):
        pass
