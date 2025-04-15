from enum import Enum
import os

class TileType(Enum):
    none = "None"
    grass = "Grass"
    sand = "Sand"
    hay = "Hay"
    
    def get_types():
        return ["None", "Grass", "Sand", "Hay"]
    

def get_tile_types():
    tile_types = os.listdir("images/Tiles")
    
    tile_types_dict = { k:os.listdir(f'images/Tiles/{k}') for k in tile_types }

    return tile_types_dict