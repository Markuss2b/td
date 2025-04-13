from model.enemy import Enemy

class Wave:
    def __init__(self):
        self.enemies = []
        
    def add_enemy_1(self):
        self.enemies.append(Enemy(type="basic enemy", health=1, speed=1, attack=1))
    
    def add_enemy_2(self):
        self.enemies.append(Enemy(type="simple enemy", health=3, speed=1, attack=3))
    
    def add_enemy_3(self):
        self.enemies.append(Enemy(type="advanced enemy", health=10, speed=1, attack=10))