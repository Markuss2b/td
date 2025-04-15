class Tower_availability:
    def __init__(self, max_x, max_y):
        self.tower_avail = []
        self.max_x = max_x
        self.max_y = max_y
        
        
    def get_tower_availability(self):
        return self.tower_avail    
    
    
    def create_empty_tower_avail_map(self):
        for i in range(self.max_y):
            self.tower_avail.append([])
            for j in range(self.max_x):
                self.tower_avail[i].append("O")
    
    
    # Automatically crosses out the possibility to place towers on all path tiles 
    def tower_auto_x_path_tiles(self, path_sequence): 
        for step in path_sequence:
            self.tower_avail[step.y][step.x] = "X"        
    
    
    def remove_tile_tower_avail(self, x, y):
        if x <= self.max_x and x >= 0 and y <= self.max_y and y >= 0: 
            self.tower_avail[y][x] = "X"
            
            
    def get_tile_tower_avail(self, x, y):
        if x <= self.max_x and x >= 0 and y <= self.max_y and y >= 0:
            return self.tower_avail[y][x]
    
        
    def add_tower_avail(self, x, y):
        if x <= self.max_x and x >= 0 and y <= self.max_y and y >= 0: 
            self.tower_avail[y][x] = "O"
            
            
    def save_tower_avail_map(self, map_name):
        f = open(f'./all_maps/{map_name}/tower_availability.txt', "w")
        for i in range(len(self.tower_avail)):
            for j in range(len(self.tower_avail[i])):
                f.write(f'{self.tower_avail[i][j]} ')
            f.write("\n")
        f.close()
    
    
    def recreate_tower_avail_map_from_file(self, map_name):
        with open(f'./all_maps/{map_name}/tower_availability.txt', "r") as path_file:
            self.tower_avail = [line.split() for line in path_file]
            self.max_x = len(self.tower_avail[0])
            self.max_y = len(self.tower_avail)
    