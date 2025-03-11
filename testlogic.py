from model.map import Map
from model.tile_type_enum import TileType

# new_map = Map("main_map", 10, 10)
# new_map.create_map()
# new_map.draw_map_locations()

# print(new_map.get_tile(8, 8).type)

# new_map.get_tile(8, 8).change_type(TileType.tower.value)
# print(new_map.get_tile(8, 8).type)

# new_map.draw_map_types()

# new_map.save_map()

new_map = Map("main_map", 5, 5)
new_map.create_map()
status = new_map.recreate_map_from_file("main_map")
new_map.draw_map_types()
new_map.save_map()

start = new_map.get_map_start()
end = new_map.get_map_end()
print(start.type, start.x, start.y)
print(end.type, end.x, end.y)

path_tiles = new_map.get_path_tiles()
print(path_tiles)

valid = new_map.validate_boring_path()
print(valid)
