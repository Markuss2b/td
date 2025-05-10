import copy
import pygame
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

        self.last_attack = pygame.time.get_ticks()

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
    
    def attack_enemy(self, all_enemies, last_attack, bullets_on_map):
        self.last_attack = last_attack
        available_targets = []
        
        # Calculate if enemy will die, by checking how many bullets are currently targetting it
        for enemy in all_enemies:
            enemy_health = copy.copy(enemy.get_health())
            for bullet in bullets_on_map:
                if enemy == bullet.get_target():
                    enemy_health -= bullet.get_damage()

            if enemy_health > 0:
                available_targets.append(enemy)

        # Get enemy closest to finish
        available_targets = sorted(available_targets, key=lambda x: len(x.get_sequence()))

        if len(available_targets) > 0:
            # Spawn bullet with target to enemy
            return Bullet(self.bullet_img, available_targets[0], 1, 1, self.x, self.y)
