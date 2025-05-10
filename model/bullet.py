import math
from other_functions import get_pix

class Bullet:
    def __init__(self, bullet_img, target, speed, damage, x, y):
        self.bullet_img = bullet_img
        self.target = target
        self.speed = speed
        self.damage = damage
        self.x = x
        self.y = y
        self.size = 20

        self.x_pix, self.y_pix = get_pix(self.x, self.y)
        self.x_pix += 32.5
        self.y_pix += 32.5
        self.hit = False

    def get_target(self):
        return self.target
    
    def get_damage(self):
        return self.damage

    def get_rect(self):
        return self.x_pix, self.y_pix, self.size, self.size
    
    def get_img(self):
        return self.bullet_img
    
    def has_hit(self):
        return self.hit

    def move(self):
        if self.hit == False:
            target_x = self.target.get_x_pix()
            target_y = self.target.get_y_pix()

            # Aim for center
            center_x = target_x + 32.5
            center_y = target_y + 32.5

            distance_x = abs(self.x_pix - center_x)
            distance_y = abs(self.y_pix - center_y)

            # distance = math.sqrt(pow(self.x_pix, 2) + pow(self.y_pix, 2))
            distance = math.sqrt(pow(distance_x, 2) + pow(distance_y, 2))
            
            if distance >= 12.5:
                vector = ((self.x_pix - center_x) / distance, (self.y_pix - center_y) / distance)

                self.x_pix = self.x_pix - vector[0] * 12.5 * self.speed
                self.y_pix = self.y_pix - vector[1] * 12.5 * self.speed
            else:
                self.x_pix = center_x
                self.y_pix = center_y
                self.hit = True
        else:
            self.target.set_health(self.damage)

        # Collide with shape