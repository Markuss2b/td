from enum import Enum

class TileType(Enum):
    none = "None"
    grass = "Grass"
    sand = "Sand"
    hay = "Hay"
    
    def get_types():
        return ["None", "Grass", "Sand", "Hay"]