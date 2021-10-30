class Terrain():
    '''
        The information describing a single Terrain type. It's name, movement cost, and color.
    '''
    def __init__(self, name, movement_cost, color):
        self.name = name
        self.movement_cost = movement_cost
        self.color = color
