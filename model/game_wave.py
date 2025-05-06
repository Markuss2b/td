from model.enemy import Enemy

#TODO: Needs some optimization, maybe different wave creation methods
# Headache
class Wave:
    def __init__(self, basic_enemy, simple_enemy, advanced_enemy):
        self.enemies = []
        self.basic_enemy = basic_enemy
        self.simple_enemy = simple_enemy
        self.advanced_enemy = advanced_enemy
        self.types = ["simple", "advanced"]

    def get_enemies(self):
        return self.enemies
        
    def add_enemy_1(self):
        self.enemies.append(Enemy(title="basic", health=1, speed=1, attack=1, x=1, y=1))
    
    def add_enemy_2(self):
        self.enemies.append(Enemy(title="simple", health=3, speed=1, attack=3, x=1, y=1))
    
    def add_enemy_3(self):
        self.enemies.append(Enemy(title="advanced", health=10, speed=1, attack=10, x=1, y=1))

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