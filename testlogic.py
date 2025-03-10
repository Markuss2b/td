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

new_map = Map("temp", 1, 1)
status = new_map.recreate_map_from_file("main_map")

if status == True:
    new_map.create_map()

new_map.draw_map_types()
new_map.draw_map_locations()
print(new_map.get_tile(8, 8).type)
new_map.get_tile(1, 1).change_type(TileType.path.value)

new_map.save_map()

print(new_map.x)
print(new_map.y)
