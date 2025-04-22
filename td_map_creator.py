import pygame
import os
import sys
import shutil
from func import draw_text
from model.map.map import Map, Location, Obstacle
from model.map.tile_type_enum import get_tile_types

# TODO: Obstacles
# TODO: Naming new map should be visible
# TODO: Buttons should have names
# Tile size 16 x 9
class MapCreator:

    def __init__(self, clock, screen):
        self.clock = clock
        self.screen = screen

        # Map Creator pygame loop
        self.running = True

        # Map selected for editing/creating
        self.map_selected = None

        # Boolean for being able to interact with the input field
        self.naming_new_map = False

        # Input field text
        self.new_map_name = ""

        # Boolean for selecting map menu pop up
        self.load_map_menu = False
        # Boolean for selecting tiles and obstacles in menu
        self.load_tile_menu = False
        self.load_obstacle_menu = False
        
        # Function in tile_type_enum. Returns Dict  Example={"Grass": ["Grass1", "Grass2"]}
        self.all_tile_types = get_tile_types()
        self.selected_visual_tile_type = "None"

        self.all_obstacles = self.get_obstacles_from_image_folder()
        self.selected_obstacle = "None"
        self.obstacle_placement_method = "Free"

        # Boolean for on click actions
        self.click = False

        # Which editing view has been selected, Path, Tower availability, Visual tiles, Obstacles
        self.selected_view_mode = "Tiles"

        # Top of Screen, can select path
        self.selected_sequence = "first_path"

        self.selected_tile = None

        self.font = pygame.font.SysFont(None, 20)

        # List containing of all maps from all_maps folder
        self.all_maps = []

        self.path_names = ["second_path", "third_path", "fourth_path"]

        # Tiles are 85x85
        self.tile_size = 85

        self.counter = 0
        self.td_map_creator_loop()


    def td_map_creator_loop(self):
        while self.running:
            self.counter += 1

            self.screen.fill((0,0,0))

            self.all_maps = os.listdir("all_maps")

            self.mx, self.my = pygame.mouse.get_pos()

            main_map_rect = pygame.Rect(0, 80, 1360, 765)
            pygame.draw.rect(self.screen, (25, 25, 25), main_map_rect)

            # Stops Map Creator crashing when map is no selected
            if self.map_selected != None:
                self.draw_tile_img()

            top_border = pygame.Rect(0, 0, 1600, 30)
            pygame.draw.rect(self.screen, (0, 75, 125), top_border)

            # Draws first so the obstacles do not get drawn outside the map
            seq_rec = []
            if self.map_selected != None:
                # Draws sequence blocks(=Amount of Paths) at the top
                for i in range(len(self.map_selected.get_all_paths())):
                    seq = pygame.Rect(40 + i * 70, 0, 60, 30)
                    pygame.draw.rect(self.screen, (180, 0, 0), seq)
                    seq_rec.append(seq)

                # Buttons for adding and removing paths    
                add_path_button = pygame.Rect(40 + len(self.map_selected.get_all_paths()) * 70, 0, 30, 30)
                remove_path_button = pygame.Rect(40 + len(self.map_selected.get_all_paths()) * 70 + 30 + 5, 0, 30, 30)
                remove_tow_avail_with_sequence_button = pygame.Rect(40 + len(self.map_selected.get_all_paths()) * 70 + 30 + 5 + 30 + 10, 0, 50, 30)
                clear_path_button = pygame.Rect(40 + len(self.map_selected.get_all_paths()) * 70 + 30 + 5 + 30 + 10 + 50 + 10, 0, 50, 30)

                self.draw_img_on_rect("images/Assets/Plus.png", add_path_button.left, add_path_button.top, add_path_button.width, add_path_button.height)
                self.draw_img_on_rect("images/Assets/Minus.png", remove_path_button.left, remove_path_button.top, remove_path_button.width, remove_path_button.height)
                pygame.draw.rect(self.screen, (255, 255, 255), remove_tow_avail_with_sequence_button)
                pygame.draw.rect(self.screen, (255, 255, 255), clear_path_button)

                self.handle_path_buttons(add_path_button, remove_path_button, seq_rec, clear_path_button, remove_tow_avail_with_sequence_button)


            # Creating the tile map 16x9 (144 buttons)
            tile_map = []
            for y in range(9):
                tile_map.append([])
                for x in range(16):
                    tile_x, tile_y = self.get_rect_param(x, y)
                    tile_rect = pygame.Rect(tile_x, tile_y, self.tile_size, self.tile_size)
                    tile_map[y].append(tile_rect)


            # Stops from obstacles being drawn outside of map
            map_top_border = pygame.Rect(0, 30, 1360, 50)
            map_bot_border = pygame.Rect(0, 845, 1360, 55)
            pygame.draw.rect(self.screen, (0, 0, 0), map_top_border)
            pygame.draw.rect(self.screen, (0, 0, 0), map_bot_border)

            map_creator_ui = pygame.Rect(1360, 30, 240, 870)
            pygame.draw.rect(self.screen, (80, 40, 10), map_creator_ui)

            save_button = pygame.Rect(1360, 850, 120, 50)
            exit_button = pygame.Rect(1480, 850, 120, 50)
            pygame.draw.rect(self.screen, (30, 120, 0), save_button)
            pygame.draw.rect(self.screen, (175, 0, 0), exit_button)

            select_map = pygame.Rect(1400, 90, 160, 50)
            pygame.draw.rect(self.screen, (255, 255, 255), select_map)

            see_tiles = pygame.Rect(1400, 190, 160, 50)
            open_tile_menu_button = pygame.Rect(1400, 260, 160, 50)
            pygame.draw.rect(self.screen, (255, 255, 255), see_tiles)
            pygame.draw.rect(self.screen, (150, 150, 50), open_tile_menu_button)

            see_obstacles = pygame.Rect(1400, 360, 160, 50)
            open_obstacle_menu = pygame.Rect(1400, 430, 160, 50)
            pygame.draw.rect(self.screen, (255, 255, 255), see_obstacles)
            pygame.draw.rect(self.screen, (50, 150, 50), open_obstacle_menu)

            see_tower_avail = pygame.Rect(1400, 530, 160, 50)
            see_sequence = pygame.Rect(1400, 600, 160, 50)
            pygame.draw.rect(self.screen, (255, 255, 255), see_tower_avail)
            pygame.draw.rect(self.screen, (255, 255, 255), see_sequence)

            # For now, have to manually add if i add any buttons
            self.handle_buttons(select_map, save_button, exit_button, see_tiles, see_tower_avail, see_sequence, tile_map, open_tile_menu_button, open_obstacle_menu, see_obstacles)


            draw_text("CREATOR", self.font, (255, 255, 255), self.screen, 900, 20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.screen.fill((0, 0, 0))
                    sys.exit()
                
                # Inputs 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.load_map_menu = False
                        self.load_tile_menu = False
                        self.load_obstacle_menu = False

                        # Without this click would stay TRUE (if clicked on anything) and would click on anything hovered after closing the POP-UP
                        self.click = False

                    if self.naming_new_map == True:
                        if event.key == pygame.K_BACKSPACE:
                            self.new_map_name = self.new_map_name[:-1]
                        else:
                            self.new_map_name += event.unicode

                    # For Removing or Returning Obstacles
                    if self.map_selected != None:
                        if len(self.map_selected.get_obstacles()) > 0:
                            if event.key == pygame.K_LEFT:
                                self.map_selected.remove_obstacle()
                        
                        if len(self.map_selected.get_removed_obstacles()) > 0:
                            if event.key == pygame.K_RIGHT:
                                self.map_selected.return_removed_obstacle()

                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
            

            pygame.display.flip()

            # Frame rate
            self.clock.tick(60)


    def handle_buttons(self, select_map, save_button, exit_button, see_tiles, see_tower_avail, see_sequence, tile_map, open_tile_menu_button, open_obstacle_menu, see_obstacles):

        # Map menu pop up and its functionality
        if self.load_map_menu == True:
            map_menu_left, map_menu_top, map_menu_width, map_menu_length = self.select_map_menu() 
            self.create_new_map(map_menu_left, map_menu_top, map_menu_width, map_menu_length)     
        elif self.load_tile_menu == True:
            self.open_tile_menu()
        elif self.load_obstacle_menu == True:
            self.open_obstacle_menu()

        # Main Map Creator UI Buttons
        else:
            if select_map.collidepoint(self.mx, self.my):
                if self.click:
                    self.load_map_menu = True

            # Stops Save button from crashing before loading a map
            if self.map_selected != None:
                if save_button.collidepoint(self.mx, self.my):
                    if self.click:
                        self.map_selected.save_map()

            if exit_button.collidepoint(self.mx, self.my):
                if self.click:
                    self.running = False
                    self.screen.fill((0,0,0))

            if see_tiles.collidepoint(self.mx, self.my):
                if self.click:
                    self.selected_view_mode = "Tiles"
            
            if open_tile_menu_button.collidepoint(self.mx, self.my):
                if self.click:
                    if self.selected_view_mode == "Tiles":
                        self.load_tile_menu = True

            if see_obstacles.collidepoint(self.mx, self.my):
                if self.click:
                    self.selected_view_mode = "Obstacles"

            if open_obstacle_menu.collidepoint(self.mx, self.my):
                if self.click:
                    if self.selected_view_mode == "Obstacles":
                        self.load_obstacle_menu = True

            if see_tower_avail.collidepoint(self.mx, self.my):
                if self.click:
                    self.selected_view_mode = "Tower"

            if see_sequence.collidepoint(self.mx, self.my):
                if self.click:
                    self.selected_view_mode = "Sequence"
            

            # For selecting tiles in the map
            if self.map_selected != None:
                for y in range(len(tile_map)):
                    for x in range(len(tile_map[y])):
                        if tile_map[y][x].collidepoint(self.mx, self.my):
                            if self.click:
                                self.selected_tile = Location(x, y)
                                print(f'Selected: X = {self.selected_tile.x}, Y = {self.selected_tile.y}')

                                self.interacting_with_tiles()

        self.click = False


    def handle_path_buttons(self, add_path_button, remove_path_button, seq_rec, clear_path_button, remove_tow_avail_with_sequence_button):
        # Max 4
        if len(self.map_selected.get_all_paths()) < 4:
            if add_path_button.collidepoint(self.mx, self.my):
                if self.click:
                    self.map_selected.add_path(self.path_names[len(self.map_selected.get_all_paths())-1])
                    self.map_selected.get_all_paths()[-1].make_empty_path()

        # Min 1
        if len(self.map_selected.get_all_paths()) > 1:
            if remove_path_button.collidepoint(self.mx, self.my):
                if self.click:
                    self.selected_sequence = "first_path"
                    self.map_selected.delete_path(self.map_selected.get_all_paths()[-1].get_path_name())

        # Checks if any of the sequence buttons have been selected
        for i in range(len(seq_rec)):
            seq_button = seq_rec[i]

            if seq_button.collidepoint(self.mx, self.my):
                if self.click:
                    if i == 0:
                        self.selected_sequence = "first_path"
                    else:
                        self.selected_sequence = self.path_names[i-1]

        # Clears path
        if clear_path_button.collidepoint(self.mx, self.my):
            if self.click:
                all_paths = self.map_selected.get_all_paths()
                if self.selected_sequence == "first_path":
                    all_paths[0].make_empty_path()
                else:
                    all_paths[self.path_names.index(self.selected_sequence)+1].make_empty_path()

        # Removes tower availability from sequence tiles
        if remove_tow_avail_with_sequence_button.collidepoint(self.mx, self.my):
            if self.click:
                tow_avail = self.map_selected.get_tower_availability_map()
                all_paths = self.map_selected.get_all_paths()
                if self.selected_sequence == "first_path":
                    sequence = all_paths[0].get_sequence()
                    if sequence[0] != None:
                        tow_avail.tower_auto_x_path_tiles(sequence)
                else:
                    sequence = all_paths[self.path_names.index(self.selected_sequence)+1].get_sequence()
                    if sequence[0] != None:
                        tow_avail.tower_auto_x_path_tiles(sequence)


    def select_map_menu(self):
        map_menu_left = 530
        map_menu_top = 100
        map_menu_width = 300
        map_menu_length = 720
        map_menu = pygame.Rect(map_menu_left, map_menu_top, map_menu_width, map_menu_length)
        pygame.draw.rect(self.screen, (0, 0, 0), map_menu)

        base_x = map_menu_left + 20
        base_y = map_menu_top + 10

        # Creates a rect for every map
        all_maps_rect = []
        for i in range(len(self.all_maps)):
            map_rect = pygame.Rect(base_x, base_y + 40 * (i + 1), 230, 30)
            pygame.draw.rect(self.screen, (255, 255, 255), map_rect)

            delete_map_rect = pygame.Rect(base_x + 230, base_y + 40 * (i + 1), 30, 30)
            self.draw_img_on_rect("images/Assets/X.png", delete_map_rect.left, delete_map_rect.top, delete_map_rect.width, delete_map_rect.height)
            
            all_maps_rect.append([map_rect, delete_map_rect])

        # Selects any previously made maps
        for i in range(len(all_maps_rect)):
            map_rect = all_maps_rect[i][0]
            delete_map_rect = all_maps_rect[i][1]

            # Recreates map
            if map_rect.collidepoint(self.mx, self.my):
                if self.click:
                    self.map_selected = Map(self.all_maps[i], 0, 0)

                    self.map_selected.recreate_map_from_folder()

            # Deletes map         
            if delete_map_rect.collidepoint(self.mx, self.my):
                if self.click:
                    shutil.rmtree(f'all_maps/{self.all_maps[i]}')

                    if self.map_selected.get_map_name() == self.all_maps[i]:
                        self.map_selected = None


        checkmark_rect = self.draw_checkmark_on_menu(map_menu)
        self.click_outside_menu(map_menu, checkmark_rect)

        return map_menu_left, map_menu_top, map_menu_width, map_menu_length


    def create_new_map(self, map_menu_left, map_menu_top, map_menu_width, map_menu_length):

        # Create buttons
        add_new_map_rect = pygame.Rect(map_menu_left + 30, map_menu_top + map_menu_length - 220, map_menu_width - 60, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), add_new_map_rect)

        new_map_inputfield = pygame.Rect(map_menu_left + 30, map_menu_top + map_menu_length - 150, map_menu_width - 60, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), new_map_inputfield)

        # Max 10 custom maps
        if len(self.all_maps) < 10:
            # Activating input field
            if new_map_inputfield.collidepoint(self.mx, self.my):
                if self.click:
                    self.naming_new_map = True
                    self.new_map_name = ""
            elif self.click:
                self.naming_new_map = False 

            # Creating a new map
            if add_new_map_rect.collidepoint(self.mx, self.my):
                if self.click:
                    if self.new_map_name != "":
                        self.map_selected = Map(self.new_map_name, 16, 9)
                        self.map_selected.create_map_folder()
                        self.map_selected.initialize_all_maps()
                        self.map_selected.save_map()


    def open_tile_menu(self):
        tile_menu_left = 370
        tile_menu_top = 100
        tile_menu_width = 545
        tile_menu_length = 700
        tile_menu = pygame.Rect(tile_menu_left, tile_menu_top, tile_menu_width, tile_menu_length)
        pygame.draw.rect(self.screen, (0, 0, 0), tile_menu)

        all_tile_type_rect = []

        base_x = tile_menu_left + 20
        base_y = tile_menu_top + 20

        for key in self.all_tile_types.keys():
            for tile_type in self.all_tile_types.get(key):
                tile_type_rect = pygame.Rect(base_x, base_y, self.tile_size, self.tile_size)

                # Draws the tile type images
                self.draw_img_on_rect(f'images/Tiles/{key}/{tile_type}', base_x, base_y, self.tile_size, self.tile_size)

                # Example = [[Rect, Type], [Rect, Type]]
                all_tile_type_rect.append([tile_type_rect, tile_type])

                base_x += self.tile_size + 20
            base_y += self.tile_size + 20
            base_x = tile_menu_left + 20

        checkmark_rect = self.draw_checkmark_on_menu(tile_menu)

        self.select_menu_functionality(self.selected_view_mode, all_tile_type_rect, tile_menu,checkmark_rect)

        
    def open_obstacle_menu(self):
        obstacle_menu_left = 370
        obstacle_menu_top = 100
        obstacle_menu_width = 545
        obstacle_menu_length = 700
        obstacle_menu = pygame.Rect(obstacle_menu_left, obstacle_menu_top, obstacle_menu_width, obstacle_menu_length)
        pygame.draw.rect(self.screen, (0, 0, 0), obstacle_menu)

        all_obstacle_rect = []
        base_x = obstacle_menu_left + 20
        base_y = obstacle_menu_top + 20

        for i in range(len(self.all_obstacles)):
            # 5 in a row
            if (i+1) % 6 == 0:
                base_x = obstacle_menu_left + 20
                base_y += (i+1) / 5 * self.tile_size + 20

            obstacle_name = self.all_obstacles[i]

            obstacle_rect = pygame.Rect(base_x, base_y, self.tile_size, self.tile_size)
            # Draws the obstacle images
            self.draw_img_on_rect(f'images/Obstacles/{obstacle_name}', base_x, base_y, self.tile_size, self.tile_size)

            all_obstacle_rect.append([obstacle_rect, obstacle_name])

            base_x += self.tile_size + 20

        checkmark_rect = self.draw_checkmark_on_menu(obstacle_menu)

        self.change_obstacle_placement_method(checkmark_rect)

        self.select_menu_functionality(self.selected_view_mode, all_obstacle_rect, obstacle_menu, checkmark_rect)

        
    def select_menu_functionality(self, menu_type, all_something_rect, something_menu, checkmark_rect):

        # For selecting which obstacle will be used for placement
        for something_rect in all_something_rect:
            if something_rect[0].collidepoint(self.mx, self.my):
                if self.click:
                    if menu_type == "Obstacles":
                        self.selected_obstacle = something_rect[1]
                    elif menu_type == "Tiles":
                        self.selected_visual_tile_type = something_rect[1]

            # Adds a border on the selected Tile
            if menu_type == "Obstacles" and something_rect[1] == self.selected_obstacle or menu_type == "Tiles" and something_rect[1] == self.selected_visual_tile_type:
                self.draw_img_on_rect(f'images/Assets/select.png', something_rect[0].x, something_rect[0].y, self.tile_size, self.tile_size)

            self.click_outside_menu(something_menu, checkmark_rect)

        
    def click_outside_menu(self, something_menu, checkmark_rect):
        # If Click outside of menu, close menu
        if not something_menu.collidepoint(self.mx, self.my) or checkmark_rect.collidepoint(self.mx, self.my):
            if self.click:
                self.load_obstacle_menu = False
                self.load_tile_menu = False
                self.load_map_menu = False


    # Gets accurate UI Location for Tile
    def get_rect_param(self, x, y):
        # LEFT, TOP
        return x * 85, y * 85 + 80


    # On Tile Click
    def interacting_with_tiles(self):
        x = self.selected_tile.x
        y = self.selected_tile.y

        if self.selected_view_mode == "Tiles":
            visual_map = self.map_selected.get_visual_map()

            visual_map.change_tile_type(x, y, self.selected_visual_tile_type)


        elif self.selected_view_mode == "Tower":
            tow_avail = self.map_selected.get_tower_availability_map()
            tile_avail = tow_avail.get_tile_tower_avail(x, y)

            # REMOVE X
            if tile_avail == "X":
                tow_avail.add_tower_avail(x, y)

            # ADD X
            elif tile_avail == "O":
                tow_avail.remove_tile_tower_avail(x, y)

        elif self.selected_view_mode == "Sequence":
            sel_path = self.map_selected.get_path(self.selected_sequence)
            seq = sel_path.get_sequence()

            # if sel_path.get_start() == None:
            #     sel_path.set_start(x, y)
            if seq[0] != None:
                if seq[-1].x == x and seq[-1].y == y:
                    sel_path.remove_step()
                else:
                    sel_path.add_next_step(x, y)

                    # Draws X for a moment to show that next step cannot be at that xy
                    if sel_path.get_2d_path()[y][x] == 0:
                        left, top = self.get_rect_param(x, y)
                        self.draw_img_on_rect("images/Assets/X.png", left, top, self.tile_size, self.tile_size)
            else:
                sel_path.add_next_step(x, y)


        # TODO:
        elif self.selected_view_mode == "Obstacles":
            print(self.map_selected.get_obstacles())
            if self.click:
                if self.selected_obstacle != "None":
                    # TODO: Size dynamic
                    half = 42
                    if self.obstacle_placement_method == "Free":
                        self.map_selected.add_obstacle(self.selected_obstacle, self.mx - half, self.my - 199, 170, 284)
                    if self.obstacle_placement_method == "Tile":
                        left, top = self.get_rect_param(x, y)
                        left = left - half
                        top = top - 199

                        obstacle_already_exists = False
                        for obstacle in self.map_selected.get_obstacles():
                            if obstacle.get_left() == left and obstacle.get_top() == top:
                                obstacle_already_exists = True
                                
                        if obstacle_already_exists == False:
                            self.map_selected.add_obstacle(self.selected_obstacle, left, top, 170, 284)


    def draw_tile_img(self):

        visual_tile = self.map_selected.get_visual_map()
        visual_tile_map = visual_tile.get_visual_tile_map()

        for y in range(len(visual_tile_map)):
            for x in range(len(visual_tile_map[y])):

                tile_x, tile_y = self.get_rect_param(x, y)
                tile = visual_tile.get_tile_type(x, y)

                if tile != None:
                    folder_name = tile.split("_")[1]

                    self.draw_img_on_rect(f'images/Tiles/{folder_name}/{tile}', tile_x, tile_y, self.tile_size, self.tile_size)

        
        obstacles = self.map_selected.get_obstacles()
        for obstacle in obstacles:
            self.draw_img_on_rect(f'images/Obstacles/{obstacle.get_name()}', obstacle.get_left(), obstacle.get_top(), obstacle.get_width(), obstacle.get_height())


        if self.selected_view_mode == "Tower":
            tow_avail = self.map_selected.get_tower_availability_map()
            tow_avail_map = tow_avail.get_tower_availability()
            
            for y in range(len(tow_avail_map)):
                for x in range(len(tow_avail_map[y])):

                    tile_x, tile_y = self.get_rect_param(x, y)
                    tile_avail = tow_avail.get_tile_tower_avail(x, y)

                    # ADD X
                    if tile_avail == "X":
                        self.draw_img_on_rect("images/Assets/X.png", tile_x, tile_y, self.tile_size, self.tile_size)


        elif self.selected_view_mode == "Sequence":
            sel_path = self.map_selected.get_path(self.selected_sequence)
            path_2d = sel_path.get_2d_path()

            for y in range(len(path_2d)):
                for x in range(len(path_2d[y])):
                    tile_x, tile_y = self.get_rect_param(x, y)
                    tile_num = path_2d[y][x]

                    self.draw_img_on_rect(f'images/Numbers/{tile_num}.png', tile_x, tile_y, self.tile_size, self.tile_size)

                     
    def get_obstacles_from_image_folder(self):
        return os.listdir("images/Obstacles")
    

    def draw_img_on_rect(self, path_to_img, left, top, width, height):
        img = pygame.image.load(path_to_img)
        img = pygame.transform.scale(img, (width, height))
        self.screen.blit(img, (left, top))

    def draw_checkmark_on_menu(self, menu_rect):
        confirm_rect = pygame.Rect(menu_rect.left + menu_rect.width / 2 - 25, menu_rect.top + menu_rect.height - 70, 50, 50)
        self.draw_img_on_rect(f'images/Assets/CheckMark.png', confirm_rect.left, confirm_rect.top, confirm_rect.width, confirm_rect.height)

        return confirm_rect
    
    def change_obstacle_placement_method(self, example_rect):
        # TODO: Future checkbox for swapping obstacle placement method
        change_obstacle_placement_method_rect = pygame.Rect(example_rect.left, example_rect.top - 50, example_rect.width, example_rect.height)
        self.draw_img_on_rect("images/Numbers/0.png", change_obstacle_placement_method_rect.left, change_obstacle_placement_method_rect.top, change_obstacle_placement_method_rect.width, change_obstacle_placement_method_rect.height)

        if change_obstacle_placement_method_rect.collidepoint(self.mx, self.my):
            if self.click:
                if self.obstacle_placement_method == "Free":
                    self.obstacle_placement_method = "Tile"
                elif self.obstacle_placement_method == "Tile":
                    self.obstacle_placement_method = "Free"