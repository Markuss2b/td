import os
from model.map.path import Path, Location
from model.map.visual_map import Visual_map
from model.map.tower_availability_map import Tower_availability

# TODO there can be multiple paths

class Map:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.paths = []
        self.visual_map = Visual_map(x, y)
        self.tower_availability_map = Tower_availability(x, y)

    
    def get_map_name(self):
        return self.name
        
        
    def create_map_folder(self):
        dir_path = f'./all_maps/{self.name}'
        
        # If map directory doesn't exist, then create one
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        
        
    def initialize_all_maps(self):
        self.create_map_folder()
        self.visual_map.create_empty_visual_map()
        self.tower_availability_map.create_empty_tower_avail_map()
        
        first_path = Path("first_path", self.x, self.y)
        first_path.make_empty_path()
        
        self.paths.append(first_path)
        
        
    def get_visual_map(self):
        return self.visual_map
    
    def get_tower_availability_map(self):
        return self.tower_availability_map        
        
        
    def add_path(self, path_name):
        self.paths.append(Path(path_name, self.x, self.y))
        
        
    def get_path(self, path_name):
        return next((path for path in self.paths if path.name == path_name), None)
    
    
    def delete_path(self, path_name):
        try:
            potential_path = next((path for path in self.paths if path.name == path_name), None)
            self.paths.remove(potential_path)
        except:
            print("No path found")    
        
        
    def save_map(self):
        self.visual_map.save_visual_map(self.name)
        
        for path in self.paths:
            path.save_path(self.name)
        
        self.tower_availability_map.save_tower_avail_map(self.name)
        
        
    def recreate_map_from_folder(self):
        self.visual_map.recreate_visual_map_from_file(self.name)
        
        # Path
        all_path_dir = os.listdir(f'./all_maps/{self.name}/paths')
        for path_i in range(len(all_path_dir)):
            path_name = all_path_dir[path_i].replace(".txt", "")

            self.paths.append(Path(path_name, self.x, self.y))
            self.paths[path_i].recreate_path_from_file(self.name, path_name)
        
        self.tower_availability_map.recreate_tower_avail_map_from_file(self.name)