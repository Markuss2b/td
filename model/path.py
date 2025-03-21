# TODO might need to change indexes

class Path:
    def __init__(self, name, max_x, max_y):
        self.name = name
        self.max_x = max_x
        self.max_y = max_y
        self.start_location = None
        self.end_location = None
        self.sequence = [None]
        self.path_tiles = []
        self.valid_path = False
        
        
    def make_empty_path(self):
        for i in range(self.max_x):
            self.path_tiles.append([])
            for j in range(self.max_y):
                self.path_tiles[i].append(0)
                
                
    def draw_path(self):
        for i in self.sequence:
            for j in i:
                print(j, end=" ")
            print()                
    
    
    def add_next_step(self, x, y):
        last_move = self.sequence[-1]
        try:
            if abs(last_move.x - x) == 0 and abs(last_move.y - y) == 1 or abs(last_move.x - x) == 1 and abs(last_move.y - y) == 0 and x < self.max_x and x >= 0 and y < self.max_y and y >= 0:
                self.sequence.append(Location(x, y))
                self.path_tiles[y][x] = len(self.sequence)
        except Exception:
            # TODO     
            print("Cant connect moves")
            
            
    def remove_step(self):
        self.path_tiles[self.sequence.y][self.sequence.x] = 0
        self.sequence.remove(self.sequence[-1])
    
    
    def set_start(self, x, y):
        self.start_location = Location(x, y)
        self.sequence[0] = self.start_location
        self.path_tiles[y][x] = 1
    def get_start(self):
        return self.start_location
    
    def set_end(self, x, y):
        self.end_location = Location(x, y)
        self.sequence.append(Location(x, y))
        self.path_tiles[y][x] = len(self.sequence)
    def get_end(self):
        return self.end_location
    
    
    def save_path(self, map_name):
        f = open(f'./all_maps/{map_name}/{self.name}.txt', "w")
        for i in len(self.path_tiles):
            for j in len(self.path_tiles[i]):
                f.write(f'{self.path_tiles[i][j]} ')
            f.write("\n")
        f.close()

    
    def recreate_path_from_file(self):
        pass
    
    
    def validate_path(self):
        pass
    

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
