from model.map.tile_type_enum import TileType

class Visual_map:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.visual_tile_map = []
        
        
    def get_visual_tile_map(self):
        return self.visual_tile_map


    def create_empty_visual_map(self):
        for i in range(self.max_x):
            self.visual_tile_map.append([])
            for j in range(self.max_y):
                self.visual_tile_map[i].append(TileType.none.value)
                
    
    def change_tile_type(self, x, y, tile_type):
        if x <= self.max_x and x >= 0 and y <= self.max_y and y >= 0:
            self.visual_tile_map[y][x] = tile_type
    
    
    def get_tile_type(self, x, y):
        if x <= self.max_x and x >= 0 and y <= self.max_y and y >= 0:
            return self.visual_tile_map[y][x]
    
    
    def remove_tile_type(self, x, y):
        if x <= self.max_x and x >= 0 and y <= self.max_y and y >= 0:
            self.visual_tile_map[y][x] = TileType.none.value
                
                
    def save_visual_map(self, map_name):
        f = open(f'./all_maps/{map_name}/visual_map.txt', "w")
        for i in range(len(self.visual_tile_map)):
            for j in range(len(self.visual_tile_map[i])):
                f.write(f'{self.visual_tile_map[i][j]} ')
            f.write("\n")
        f.close()
    
    
    def recreate_visual_map_from_file(self, map_name):
        with open(f'./all_maps/{map_name}/visual_map.txt', "r") as path_file:
            self.visual_tile_map = [line.split() for line in path_file]
            self.max_x = len(self.visual_tile_map[0])
            self.max_y = len(self.visual_tile_map)           
    