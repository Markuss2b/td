import os

# TODO: THIS JUST DOES NOT WORK

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
        self.cleared_path = None

    def get_2d_path(self):
        return self.path_tiles
        
    def get_path_name(self):
        return self.name
    
    def get_sequence(self):
        return self.sequence
        
    
    def make_empty_path(self):
        if self.path_tiles != []:
            self.cleared_path = [self.path_tiles, self.start_location, self.end_location, self.sequence]

        self.path_tiles = []
        self.start_location = None
        self.end_location = None
        self.sequence = [None]
        for i in range(self.max_y):
            self.path_tiles.append([])
            for j in range(self.max_x):
                self.path_tiles[i].append(0)


    def undo_path_clear(self):
        if self.cleared_path != None:
            self.path_tiles = self.cleared_path[0]
            self.start_location = self.cleared_path[1]
            self.end_location = self.cleared_path[2]
            self.sequence = self.cleared_path[3]
            self.cleared_path = None
                
                
    def draw_path(self):
        print("==================================")
        for i in self.path_tiles:
            for j in i:
                print(j, end=" ")
            print()
        print("==================================")                
    
    
    def add_next_step(self, x, y):
        try:
            if self.sequence[0] == None:
                self.sequence[0] = Location(x, y)
                self.path_tiles[y][x] = len(self.sequence)
            else:
                already_in_sequence = False
                for location in self.sequence:
                    if location.x == x and location.y == y:
                        already_in_sequence = True

                last_move = self.sequence[-1]       

                # If statements check if next step is connected with the last move. Also it checks if its out of bounds
                if abs(last_move.x - x) == 0 and abs(last_move.y - y) == 1 or abs(last_move.x - x) == 1 and abs(last_move.y - y) == 0:
                    if x <= self.max_x and x >= 0 and y <= self.max_y and y >= 0:
                        if already_in_sequence == False:
                            self.sequence.append(Location(x, y))
                            self.path_tiles[y][x] = len(self.sequence)
                        else:
                            raise Exception
                    else:
                        raise Exception
                else:
                    raise Exception
             
        except Exception:
            # TODO     
            print("Cant connect moves")
            
            
    def remove_step(self):
        if len(self.sequence) > 1:
            self.path_tiles[self.sequence[-1].y][self.sequence[-1].x] = 0
            self.sequence.remove(self.sequence[-1])
        elif len(self.sequence) == 1:
            self.path_tiles[self.sequence[-1].y][self.sequence[-1].x] = 0
            self.start_location = None
            self.end_location = None
            self.sequence = [None]
            print("No steps to remove")
    
    # TODO: Do i need this ?
    def set_start(self, x, y):
        if x <= self.max_x and x >= 0 and y <= self.max_y and y >= 0:
            # Only remove previous value when start_location has not been set
            if self.start_location != None:
                self.path_tiles[self.start_location.y][self.start_location.x] = 0
            
            # If Sequence has been made, then changing start destroys the whole sequence 
            # TODO Alternative, could lock changing start if the sequence is bigger than 1   
            if len(self.sequence) > 1:
                self.sequence.clear()
                self.sequence.append(None)
                self.path_tiles[self.end_location.y][self.end_location.x] = 0
                self.end_location = None
                
            self.start_location = Location(x, y)
            self.sequence[0] = self.start_location
            self.path_tiles[y][x] = 1
    def get_start(self):
        return self.start_location
    
    # TODO: do i need this?
    def set_end(self, x, y):
        if x <= self.max_x and x >= 0 and y <= self.max_y and y >= 0:
            # Only remove previous value when end_location has not been set
            if self.end_location != None:
                self.path_tiles[self.end_location.y][self.end_location.x] = 0
            
            self.end_location = Location(x, y)
            self.sequence.append(Location(x, y))
            self.path_tiles[y][x] = len(self.sequence)
    def get_end(self):
        return self.end_location
    
    
    def save_path(self, map_name):
        
        # If paths directory doesn't exist, then create one
        paths_dir = f'./all_maps/{map_name}/paths'
        if not os.path.isdir(paths_dir):
            os.mkdir(paths_dir)
            
        f = open(f'./all_maps/{map_name}/paths/{self.name}.txt', "w")
        for i in range(len(self.path_tiles)):
            for j in range(len(self.path_tiles[i])):
                f.write(f'{self.path_tiles[i][j]} ')
            f.write("\n")
        f.close()

    
    # Copy or Load map from file
    def recreate_path_from_file(self, map_name, path_name, map_type):

        if map_type == "PremadeMap":
            start_folder = "predrawn_maps"
        elif map_type == "Map":
            start_folder = "all_maps"

        with open(f'./{start_folder}/{map_name}/paths/{path_name}.txt', "r") as path_file:
            
            txt_file_list = [line.split() for line in path_file]
            self.max_x = len(txt_file_list[0])
            self.max_y = len(txt_file_list)
            
            dict_sequence = {} 
            
            for y in range(self.max_y):
                self.path_tiles.append([])
                
                for x in range(self.max_x):
                    value = int(txt_file_list[y][x])
                    
                    self.path_tiles[y].append(value)

                    if value > 0:
                        dict_sequence[value] = Location(x, y)
                  
            # If there is no sequence then None will be replaced later      
            if len(dict_sequence) != 0:     
                # Predefined first value of sequence that needs to be removed when recreating the path from the file
                self.sequence.remove(None)  

            # Sorting sequence in rising order
            sorted_dict_sequence = dict(sorted(dict_sequence.items()))
            for dict_key in sorted_dict_sequence:
                self.sequence.append(sorted_dict_sequence.get(dict_key))
            
            # Start and end can be in the same location
            if len(self.sequence) > 0:
                self.start_location = self.sequence[0]
                self.end_location = self.sequence[-1]
            
            # Prints sequence coordinates
            # for i in self.sequence:
            #     print(f'x={i.x}, y={i.y}')

    
    def validate_path(self):
        pass
    

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
