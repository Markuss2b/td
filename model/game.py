from model.map.map import Map
from model.game_wave import Wave

# TODO profile
# TODO spawner
class Game:
    def __init__(self, game_name):
        self.game_name = game_name
        self.game_map = Map(game_name, 0, 0)
        self.waves = [Wave(10, 2, 1), Wave(20, 10, 5)]

        self.game_map.recreate_map_from_folder()
        
    def spawn_enemy():
        pass
