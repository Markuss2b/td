from model.map.path import Path
from model.game_wave import Wave

class Spawner:
    def __init__(self, sequence):
        self.sequence = sequence
        self.waves = []