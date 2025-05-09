from other_functions import get_pix


# Move enemies that are alive and haven't finished
class Enemy:
    def __init__(self, title, health, speed, attack, sequence):
        self.title = title
        self.health = health
        self.speed = speed
        self.attack = attack

        # Example: [Location(x, y), Location(x, y), ...]
        self.sequence = sequence

        self.x = self.sequence[0].x
        self.y = self.sequence[0].y

        self.x_pix, self.y_pix = get_pix(self.x, self.y)
        self.direction = self.get_direction(self.x, self.y, self.sequence[1].x, self.sequence[1].y)

        # Every 5 steps turn to direction, every 10 steps reset to 0 (Moving through tiles)
        self.step_in_tile = 24

        self.finished = False
        self.alive = True
        
    def move(self):
        # print(self.direction)
        if self.step_in_tile == 24:
            if not (self.sequence[-1].x == self.x and self.sequence[-1].y == self.y):
                self.direction = self.get_direction(self.x, self.y, self.sequence[1].x, self.sequence[1].y)
        elif self.step_in_tile == 40:
            self.step_in_tile = 0
            self.sequence.remove(self.sequence[0])
            self.x = self.sequence[0].x
            self.y = self.sequence[0].y
            # print(f'x={self.x}, y={self.y}')

        # step
        if self.direction == "UP":
            self.y_pix -= 2.125
        elif self.direction == "DOWN":
            self.y_pix += 2.125
        elif self.direction == "LEFT":
            self.x_pix -= 2.125
        elif self.direction == "RIGHT":
            self.x_pix += 2.125
        
        self.step_in_tile += 1

        if self.sequence[-1].x == self.x and self.sequence[-1].y == self.y and self.step_in_tile == 10:
                self.finished = True

    def get_direction(self, current_x, current_y, next_x, next_y):
        if current_x > next_x:
            return "LEFT"
        elif current_x < next_x:
            return "RIGHT"
        elif current_y > next_y:
            return "UP"
        else:
            return "DOWN"
        
    def get_x_pix(self):
        return self.x_pix

    def get_y_pix(self):
        return self.y_pix
    
    def is_finished(self):
        return self.finished