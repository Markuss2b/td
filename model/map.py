

# TODO there can be multiple paths

class Map:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.paths = []
        self.tiles = []
        self.tower_tiles = []
        
    def create_map_files(self):
        pass    
        
    def tower_auto_x_path_tiles(self, path):
        # TODO automatically cross out the possibility to place towers on all path tiles 
        pass    
        
    def save_map(self):
        pass   
        
    def recreate_map_from_folder(self):
        # From path folder, get paths
        # From tile_names.txt get tile names
        # From tower_tiles.txt get tower tiles (where can you place towers) 
        pass