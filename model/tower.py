import copy
import pygame
import math
from other_functions import get_pix
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
        self.direction = "DOWN"
        self.img_end = "D"

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
    
    def get_direction(self):
        return self.direction
    
    def get_ending(self):
        return self.img_end
    
    def reset_last_attack(self):
        self.last_attack = pygame.time.get_ticks() + 1000
    
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
            for target in available_targets:
                if self.is_in_range(target) == True:

                    self.turn_to_target(target)

                    # Spawn bullet with target to enemy
                    return Bullet(self.bullet_img, target, 1, 1, self.x, self.y)


    def turn_to_target(self, target):
        target_x = target.get_x_pix()
        target_y = target.get_y_pix()

        tower_x_pix, tower_y_pix = get_pix(self.x, self.y)

        # Pygame reversed Y
        radians = math.atan2(-(target_y - tower_y_pix), target_x - tower_x_pix)
        degrees = (radians * (180 / math.pi) + 360) % 360

        if degrees <= 22.5 and degrees > 0 or degrees > 337.5:
            self.img_end = "R"
            self.direction = "RIGHT"
        elif degrees > 22.5 and degrees <= 67.5:
            self.img_end = "UR"
            self.direction = "UPRIGHT"
        elif degrees > 67.5 and degrees <= 112.5:
            self.img_end = "U"            
            self.direction = "UP"
        elif degrees > 112.5 and degrees <= 157.5:
            self.img_end = "UL"
            self.direction = "UPLEFT"
        elif degrees > 157.5 and degrees <= 202.5:
            self.img_end = "L"
            self.direction = "LEFT"
        elif degrees > 202.5 and degrees <= 247.5:
            self.img_end = "DL"
            self.direction = "DOWNLEFT"
        elif degrees > 247.5 and degrees <= 292.5:
            self.img_end = "D"
            self.direction = "DOWN"
        elif degrees > 292.5 and degrees <= 337.5:
            self.img_end = "DR"
            self.direction = "DOWNRIGHT"


    def is_in_range(self, target):
        target_x = target.get_x()
        target_y = target.get_y()

        if abs(self.x - target_x) > self.range:
            return False
        if abs(self.y - target_y) > self.range:
            return False

        return True