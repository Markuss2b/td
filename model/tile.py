class Tile:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        
    def change_type(self, type):
        self.type = type
