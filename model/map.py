from model.tile import Tile
from model.tile_type_enum import TileType
import numpy as np

# TODO for creating map


class Map:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.tiles = []
        self.valid_path = self.validate_boring_path()
        
    
    def is_map_valid(self):
        return self.valid_path
        
        
    # TODO TEMPORARY FUNCTIONS
    # Note its not 1-10 but 0-9    
    def draw_map_locations(self):
        for i in self.tiles:
            for j in i:
                print(f'({j.x} {j.y})', end=" ")
            print()


    def draw_map_types(self):
        for i in self.tiles:
            for j in i:
                print(j.type, end=" ")
            print()
    # TODO
            
            
    def create_map(self):
        self.tiles = []
        for i in range(self.y):
            self.tiles.append([])
            for j in range(self.x):
                self.tiles[i].append(Tile(TileType.none.value, j, i))
        self.tiles.reverse()
        
        
    def get_tile(self, x, y):
        return self.tiles[y][x]
    
    
    """
    Section takes care of returning where in the map is the Start tile and the End tile
    There can only be 1 Start tile and 1 End tile / Else returns None
    """
    def get_map_start(self):
        start_tiles = [el for lst in self.tiles for el in lst if el.type == "Start"]
        count_of_start = len(start_tiles)
        tile = self.start_end_error(start_tiles, "Start", count_of_start)
        return tile
    
    def get_map_end(self):
        end_tiles = [el for lst in self.tiles for el in lst if el.type == "End"]
        count_of_end = len(end_tiles)
        tile = self.start_end_error(end_tiles, "End", count_of_end)
        return tile
    
    def start_end_error(self, lst, type, count_of_type):
        try:
            if count_of_type != 1:
                raise Exception
            
            return lst[0]
        except:
            print(f'There are {count_of_type} "{type}" tiles \n Invalid {type} usage')
    # Section ends
     
    def get_path_tiles(self):
        path_tiles = [el for lst in self.tiles for el in lst if el.type == "Path"]
        return path_tiles
     
     
    # Function validates that From Start tile to End tile, there is a valid path
    def validate_boring_path(self):
        start_tile = self.get_map_start()
        end_tile = self.get_map_end()
        path_tiles = self.get_path_tiles()
        
        
        
        
    
    
    # TODO Create multiple possible paths
    def validate_chaos_path(self):
        pass
    
    
    def save_map(self):
        f = open(f'./maps/{self.name}.txt', "w")
        for i in self.tiles:
            for j in i:
                f.write(f'{j.type} ')
            f.write("\n")
            
        f.close()
        
        
    def recreate_map_from_file(self, name):
        corrupt_file = False
        all_types = TileType.get_types()
        self.tiles = []
        
        # Copies a Map object values from a map file
        with open(f'./maps/{name}.txt', "r") as map_file:
            type_list = [line.split() for line in map_file if line.split() != []]
            self.x = len(type_list[0])
            self.y = len(type_list)
            
            for i in range(len(type_list)):
                
                # If file has been edited, then create an empty map
                if corrupt_file == True:
                    # self.y = i
                    self.create_map()
                    break
                
                self.tiles.append([])
                try:
                    if len(type_list[i]) < self.x:
                        raise Exception

                    for j in range(len(type_list[i])):
                        if not type_list[i][j] in all_types:
                            raise Exception
                        
                        self.tiles[i].append(Tile(type_list[i][j], j, i))
                except:
                    corrupt_file = True
                    print("File has been edited")
        
        return corrupt_file

            
        