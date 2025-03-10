from enum import Enum

class TileType(Enum):
    none = "None"
    path = "Path"
    tower = "Tower"
    
    def get_types():
        return ["None", "Path", "Tower"]