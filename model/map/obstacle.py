class Obstacle:
    
    def __init__(self, name, left, top, length, width):
        self.name = name
        self.left = left
        self.top = top
        self.length = length
        self.width = width

    def get_name(self):
        return self.name
    def get_left(self):
        return self.left
    def get_top(self):
        return self.top
    def get_length(self):
        return self.length
    def get_width(self):
        return self.width