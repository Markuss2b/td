class Obstacle:
    
    def __init__(self, name, left, top, width, height):
        self.name = name
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def get_name(self):
        return self.name
    def get_left(self):
        return self.left
    def get_top(self):
        return self.top
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height