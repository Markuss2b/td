from model.map.map import Map

# TODO profile
# TODO spawner
class Game:
    def __init__(self, game_name):
        self.game_name = game_name
        self.map = Map(game_name, 0, 0)
        
    def recreate_map(self):
        self.map.recreate_map_from_folder()