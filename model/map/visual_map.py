from model.map.tile_type_enum import TileType

# TODO Change type needs to be remade

class Visual_map:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.visual_tiles = []


    def create_empty_visual_map(self):
        for i in range(self.max_x):
            self.visual_tiles.append([])
            for j in range(self.max_y):
                self.visual_tiles[i].append(TileType.none.value)
                
                
    def save_visual_map(self):
        pass
    
    
    def recreate_visual_map_from_file(self):
        pass            
    

class Visual_tile:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        
    def change_type(self, type):
        self.type = type
        
    def remove_type(self):
        self.type = TileType.none.value