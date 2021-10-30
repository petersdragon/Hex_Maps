
'''
    Comment for File here
'''
from unit import Unit

class Side():
    '''
        All of the information regarding one Side and its units
    '''
    def __init__(self, side):
        self.side = side
        self.units = []

    def add_unit_type(self, unit_info):
        '''
            Comment for Function here
        '''
        self.units.append(Unit(unit_info))
