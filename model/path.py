class Path:
    def __init__(self, name):
        self.name = name
        self.start_location = None
        self.end_location = None
        self.path_tiles = []
        self.valid_path = False
        
    def clear_path(self):
        pass
    
    def add_next_step(self, x, y):
        pass
    
    def remove_step(self, x, y):
        pass
    
    def get_start(self):
        pass
    
    def get_end(self):
        pass
    
    def save_path(self):
        pass
    
    def recreate_path_from_file(self):
        pass
    
    def validate_path(self):
        pass
    