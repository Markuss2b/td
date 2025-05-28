from model.enemy import Enemy
from db_functions import get_enemy_with_title

#TODO: Needs some optimization, maybe different wave creation methods
# Headache
class Wave:
    def __init__(self, spawn_delay, basic_enemy, simple_enemy, advanced_enemy):
        self.spawn_delay = spawn_delay
        self.basic_enemy = basic_enemy
        self.simple_enemy = simple_enemy
        self.advanced_enemy = advanced_enemy
        self.types = ["simple", "advanced"]
        self.enemies = []

    def get_spawn_delay(self):
        return self.spawn_delay

    def get_enemies(self):
        return self.enemies
        
    def add_enemy_1(self):
        self.enemies.append("basic")
    
    def add_enemy_2(self):
        self.enemies.append("simple")
    
    def add_enemy_3(self):
        self.enemies.append("advanced")

    # Basic => Fire Orb
    # Simple => Magma Ball
    # Advanced => ?
    def add_enemy(self, type):
        if type == "basic":
            self.add_enemy_1()
        elif type == "simple":
            self.add_enemy_2()
        elif type == "advanced":
            self.add_enemy_3()


    #  If more than 3 enemies, need to make more efficient
    def create_wave(self):
        if self.simple_enemy > 0:
            too_many_simple = False
            step_simple = 0
            can_divide_simple = 0
            return_var_simple = self.get_enemy_step(self.basic_enemy, self.simple_enemy)
            if type(return_var_simple) == bool: 
                too_many_simple = return_var_simple
            else:
                step_simple, can_divide_simple = return_var_simple

        if self.advanced_enemy > 0:
            too_many_advanced = False
            step_advanced = 0
            can_divide_advanced = 0
            return_var_advanced = self.get_enemy_step(self.basic_enemy, self.advanced_enemy)
            if type(return_var_advanced) == bool: 
                too_many_advanced = return_var_advanced
            else:
                step_advanced, can_divide_advanced = return_var_advanced

        for i in range(self.basic_enemy):
            self.add_enemy("basic")
            if self.simple_enemy > 0:
                step_simple = self.add_enemy_in_loop(step_simple, too_many_simple, i, self.basic_enemy, self.simple_enemy, can_divide_simple, "simple")
            if self.advanced_enemy > 0:
                step_advanced = self.add_enemy_in_loop(step_advanced, too_many_advanced,  i, self.basic_enemy, self.advanced_enemy, can_divide_advanced, "advanced")

    def get_enemy_step(self, base_enemies, enemies):
        can_divide = base_enemies
        if base_enemies / enemies >= 2:
            if base_enemies % enemies > 0 or enemies == 1:
                can_divide -= base_enemies % enemies
            step = int(can_divide / enemies)
            return step, can_divide
        else:
            too_many_enemy = True
            return too_many_enemy 

    def add_enemy_in_loop(self, step, too_many_enemy, iteration, base_enemies, enemy_amount, can_divide, enemy_type):
        if too_many_enemy == False:
            if iteration+1 == step and sum(1 for x in self.enemies if isinstance(x, Enemy) and x.title == enemy_type) < enemy_amount:
                step += can_divide / enemy_amount
                self.add_enemy(enemy_type)

        elif too_many_enemy == True:
            left_start = (base_enemies - enemy_amount) / 2
            right_start = enemy_amount + (base_enemies - enemy_amount) / 2

            if iteration > left_start and iteration <= right_start:
                self.add_enemy(enemy_type)
                
        return step
    
    def create_simple_wave(self):
        for i in range(self.simple_enemy):
            self.enemies.append("simple")

    def spawn_enemy(self, sequence):
        if self.enemies[-1] == "basic":
            enemy = get_enemy_with_title("Fire orb")
        elif self.enemies[-1] == "simple":
            enemy = get_enemy_with_title("Magma ball")
        elif self.enemies[-1] == "advanced":
            enemy = get_enemy_with_title("Fire ball")
        
        title, health, speed, attack, img = enemy[1], enemy[2], enemy[3], enemy[4], enemy[5]

        self.enemies.remove(self.enemies[-1])
        return Enemy(title, health, speed, attack, img, sequence)