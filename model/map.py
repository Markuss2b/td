from model.tile import Tile
from model.tile_type_enum import TileType

# TODO for creating map


class Map:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.tiles = []
        
        
    # TODO TEMPORARY FUNCTIONS    
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
        return self.tiles[y-1][x-1]
    
    
    def save_map(self):
        f = open(f'./maps/{self.name}.txt', "w")
        for i in self.tiles:
            for j in i:
                f.write(f'{j.type} ')
            f.write("\n")
            
        f.close()
        
        
    def recreate_map_from_file(self, name):
        self.name = name
        corrupt_file = False
        all_types = TileType.get_types()
        
        with open(f'./maps/{name}.txt', "r") as map_file:
            type_list = [line.split() for line in map_file if line.split() != []]
            self.x = len(type_list[0])
            self.y = len(type_list)
            
            for i in range(len(type_list)):
                if corrupt_file == True:
                    # self.y = i
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

            
        