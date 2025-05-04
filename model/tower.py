class Tower:
    def __init__(self, name, attack, range, x, y, tower_image):
        self.name = name
        self.attack = attack
        self.range = range
        self.x = x
        self.y = y
        self.tower_image = tower_image

    def get_name(self):
        return self.name
    
    def get_attack(self):
        return self.attack
    
    def get_range(self):
        return self.range
    
    def get_location(self):
        return (self.x, self.y)
    
    def get_image(self):
        return self.tower_image
    