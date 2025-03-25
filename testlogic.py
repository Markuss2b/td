from model.map.map import Map
from model.map.tile_type_enum import TileType

# first_map = Map("test_map", 10, 10)
# first_map.initialize_all_maps()
# first_map.get_visual_map().change_tile_type(0, 0, TileType.grass.value)
# first_map.get_path("first_path").set_start(0, 0)
# first_map.get_tower_availability_map().tower_auto_x_path_tiles(first_map.get_path("first_path").get_sequence())
# first_map.save_map()

second_map = Map("test_map", 0, 0)
second_map.recreate_map_from_folder()
# second_map.get_path("first_path").draw_path()
second_map.get_path("first_path").draw_path()
print(second_map.get_tower_availability_map().get_tile_tower_avail(0, 0))

print(second_map.get_visual_map().get_tile_type(0, 0))
print(second_map.get_visual_map().get_tile_type(0, 1))

print("======================================")
print(second_map.get_path("first_path").get_end().y)
print("======================================")
second_map.get_path("first_path").add_next_step(0, 1)
second_map.get_path("first_path").draw_path()