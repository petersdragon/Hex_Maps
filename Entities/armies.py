'''
    Comment for the file here
'''
import json
import pygame
from Entities.unit import Unit
from utilities import definitions

class Armies():
    '''
        Comment for the class here
    '''
    def __init__(self, scrollbars, offset=0):
        self.scrollbar = scrollbars
        self.unit_info = {}
        self.file_path = definitions.UTILITIES + "//unit_info.json"
        self.load_unit_info()
        #self.armies = []
        self.menu_visible = False
        print(self.unit_info['Gondor'])
        print(self.unit_info['Gondor']['Hero'])
        print(self.unit_info['Gondor']['Hero']['Archer'])
        print(self.unit_info['Gondor']['Hero']['Archer'])

    def load_unit_info(self):
        '''
            Read all unit info and organize it into dictionaries.
            Structure: {sides{armors{melee, archer}}}
        '''
        with open(self.file_path, newline='') as file:
            obj = json.loads(file.read())
            sides = list(set([x['side'] for x in obj])) # Get the unique sides in the list of units
            for side in sides:
                armors = list(set([x['armor'] for x in obj if x['side'] == side]))    # Get the unique armors for each side in the list of unit_info
                armor_dict = {}
                for armor in armors:
                    attack_type = [x for x in obj if x['side'] == side and x['armor'] == armor][0]
                    # Allow Archer option if Archer_Attack > 0, Allow Melee option if Melee_Attack > 0
                    attack_type_dict = {}
                    if attack_type['melee_attack'] > 0:
                        attack_type_dict['Melee'] = 'Melee'
                    if attack_type['archer_attack'] > 0:
                        attack_type_dict['Archer'] = 'Archer'
                    armor_dict[armor] = attack_type_dict
                self.unit_info[side] = armor_dict

    def recruit_unit(self,x,y,unit_info):
        '''
            Comment for the function here
        '''
        self.armies.append(Unit(x,y,unit_info))

    def update(self, surface):
        '''
            Comment for the function here
        '''
        for unit in self.armies:
            unit.draw_unit(surface, self.scrollbar[0].axis, self.scrollbar[1].axis, self.font)
        self.unit_menu.draw()

    def toggle_menu(self):
        '''
            Comment for the function here
        '''
        if not self.menu_visible:
            self.unit_menu.show()
            self.menu_visible = True
        elif self.menu_visible:
            self.unit_menu.hide()
            self.menu_visible = False

    def handle_event(self, event):
        '''
            Comment for the function here
        '''
