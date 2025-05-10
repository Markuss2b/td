from model.bullet import Bullet

class Tower:
    def __init__(self, name, attack, range, attack_delay, bullet_img, x, y, tower_image):
        self.name = name
        self.attack = attack
        self.range = range
        self.attack_delay = attack_delay
        self.bullet_img = bullet_img
        self.x = x
        self.y = y
        self.tower_image = tower_image

        self.last_attack = 0

    def get_name(self):
        return self.name
    
    def get_attack(self):
        return self.attack
    
    def get_range(self):
        return self.range
    
    def get_attack_delay(self):
        return self.attack_delay
    
    def get_location(self):
        return (self.x, self.y)
    
    def get_image(self):
        return self.tower_image
    
    def get_last_attack(self):
        return self.last_attack
    
    def attack_enemy(self, all_enemies, last_attack):
        self.last_attack = last_attack

        # Get enemy closest to finish
        all_enemies = sorted(all_enemies, key=lambda x: len(x.get_sequence()))

        # Spawn bullet with target to enemy
        return Bullet(self.bullet_img, all_enemies[-1], 1, self.x, self.y)
