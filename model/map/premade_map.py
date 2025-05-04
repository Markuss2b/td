import os
from model.map.tower_availability_map import Tower_availability
from model.map.path import Path

class PremadeMap:
    def __init__(self, name, x, y):
        self.type = "PremadeMap"
        self.name = name
        self.x = x
        self.y = y
        self.paths = []
        self.tower_availability_map = Tower_availability(x, y)

    def get_map_name(self):
        return self.name
    
    def get_map_type(self):
        return self.type

    def get_tower_availability_map(self):
        return self.tower_availability_map        
           
    def get_path(self, path_name):
        return next((path for path in self.paths if path.name == path_name), None)
    
    def get_all_paths(self):
        return self.paths
    
    def recreate_map_from_folder(self):

        # Path
        all_path_dir = os.listdir(f'./predrawn_maps/{self.name}/paths')
        for path_i in range(len(all_path_dir)):
            path_name = all_path_dir[path_i].replace(".txt", "")

            self.paths.append(Path(path_name, self.x, self.y))
            self.paths[path_i].recreate_path_from_file(self.name, path_name, self.type)
        
        self.tower_availability_map.recreate_tower_avail_map_from_file(self.name, self.type)
