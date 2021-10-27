'''
    Comment for the file here
'''
class CubeHex():
    '''
        A single hex tile of the grid in Cubic coordinates
    '''
    def __init__(self, x, y, z, radius):
        assert (round(x + y + z) == 0), "Sum of cubic coordinates must be 0 (x + y + z = 0)"    # Check to see if the coordinates are valid cubic coordinates
        self.x = x                      # The x coordinate of the hex in the cubic space
        self.y = y                      # The y coordinate of the hex in the cubic space
        self.z = z                      # The z coordinate of the hex in the cubic space
        self.radius = radius            # Radius of the hex from its center to one of its vertices
