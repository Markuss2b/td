# TODO pre-existing tiles for creating maps?
"""
Example: 
Path1 = North/South wall
Path2 = South/East wall
etc... 
Inheritance ?
"""
# TODO walls are needed for Start/End/Path tiles

class Tile:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        #             NORTH  EAST   SOUTH  WEST
        self.walls = [False, False, False, False]
        
    def change_type(self, type):
        self.type = type
        
    def add_wall_north(self):
        self.walls[0] = True
        
    def add_wall_east(self):
        self.walls[1] = True
    
    def add_wall_south(self):
        self.walls[2] = True
        
    def add_wall_south(self):
        self.walls[3] = True
        
    def remove_wall_north(self):
        self.walls[0] = False
        
    def remove_wall_east(self):
        self.walls[1] = False
    
    def remove_wall_south(self):
        self.walls[2] = False
        
    def remove_wall_south(self):
        self.walls[3] = False
         
