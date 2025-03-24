from model.map.path import Path, Location
from model.map.visual_map import Visual_map, Visual_tile
from model.map.tower_availability_map import Tower_availability

# TODO there can be multiple paths

class Map:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.paths = []
        self.visual_map = None
        self.tower_availability = None
        
    def create_map_files(self):
       # From path move creating paths directory
       # Create base txt files like visual_tiles.txt, tower_tiles.txt 
        pass    
        
        
    def save_map(self):
        
        #TODO might want to create all directories and base txt files here
        
        # Save tiles
        # Save paths
        # Save tower_tiles
        pass   
        
        
    def recreate_map_from_folder(self):
        # From path folder, get paths
        # From visual_tiles.txt get visual_tiles
        # From tower_tiles.txt get tower tiles (where can you place towers) 
        pass