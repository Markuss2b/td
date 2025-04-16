import pygame
import os
from func import draw_text
from model.map.map import Map, Location, Obstacle
from model.map.tile_type_enum import get_tile_types

# FIXME: Clicking on X returns to menu (Should quit the program)
# FIXME: Do i want map_menu to be centered around the screen or the map
# FIXME: Overlapping path
# TODO: Obstacles
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

        # Boolean for on click actions
        self.click = False

        # Which editing view has been selected, Path, Tower availability, Visual tiles, Obstacles
        self.selected_view_mode = "Tiles"

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
            pygame.draw.rect(self.screen, (0, 0, 0), main_map_rect)


            # Creating the tile map 16x9 (144 buttons)
            tile_map = []
            for y in range(9):
                tile_map.append([])
                for x in range(16):
                    tile_x, tile_y = self.get_rect_param(x, y)
                    tile_rect = pygame.Rect(tile_x, tile_y, self.tile_size, self.tile_size)
                    tile_map[y].append(tile_rect)


            top_border = pygame.Rect(0, 0, 1600, 30)
            pygame.draw.rect(self.screen, (0, 0, 255), top_border)

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
                pygame.draw.rect(self.screen, (255, 255, 255), add_path_button)
                pygame.draw.rect(self.screen, (255, 255, 255), remove_path_button)

            map_creator_ui = pygame.Rect(1360, 30, 240, 870)
            pygame.draw.rect(self.screen, (0, 122, 122), map_creator_ui)

            save_button = pygame.Rect(1360, 850, 120, 50)
            exit_button = pygame.Rect(1480, 850, 120, 50)
            pygame.draw.rect(self.screen, (0, 255, 0), save_button)
            pygame.draw.rect(self.screen, (255, 0, 0), exit_button)

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

            # Stops Map Creator crashing when map is no selected
            if self.map_selected != None:
                self.draw_tile_img()

                self.handle_path_buttons(add_path_button, remove_path_button, seq_rec)

            # For now, have to manually add if i add any buttons
            self.handle_buttons(select_map, save_button, exit_button, see_tiles, see_tower_avail, see_sequence, tile_map, open_tile_menu_button, open_obstacle_menu, see_obstacles)


            draw_text("CREATOR", self.font, (255, 255, 255), self.screen, 900, 20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.screen.fill((0, 0, 0))
                
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

                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
            

            pygame.display.flip()

            # Frame rate
            self.clock.tick(60)


    def handle_buttons(self, select_map, save_button, exit_button, see_tiles, see_tower_avail, see_sequence, tile_map, open_tile_menu_button, open_obstacle_menu, see_obstacles):

        # Map menu pop up and its functionality
        # FIXME: MAX 10 MAPS
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

            if save_button.collidepoint(self.mx, self.my):
                if self.click:

                    # FIXME: If Map not selected will crash
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
            for y in range(len(tile_map)):
                for x in range(len(tile_map[y])):
                    if tile_map[y][x].collidepoint(self.mx, self.my):
                        if self.click:
                            self.selected_tile = Location(x, y)
                            print(f'Selected: X = {self.selected_tile.x}, Y = {self.selected_tile.y}')

                            self.interacting_with_tiles()

        self.click = False


    def handle_path_buttons(self, add_path_button, remove_path_button, seq_rec):
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


    def select_map_menu(self):
        map_menu_left = 650
        map_menu_top = 100
        map_menu_width = 300
        map_menu_length = 700
        map_menu = pygame.Rect(map_menu_left, map_menu_top, map_menu_width, map_menu_length)
        pygame.draw.rect(self.screen, (0, 0, 0), map_menu)

        base_x = map_menu_left + 20
        base_y = map_menu_top + 60

        # Creates a rect for every map
        all_maps_rect = []
        for i in range(len(self.all_maps)):
            map_rect = pygame.Rect(base_x, base_y + 40 * (i + 1), 260, 30)
            all_maps_rect.append(map_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), map_rect)

        # Selects any previously made maps
        for i in range(len(all_maps_rect)):
            map_rect = all_maps_rect[i]

            if map_rect.collidepoint(self.mx, self.my):
                if self.click:
                    self.map_selected = Map(self.all_maps[i], 0, 0)

                    self.map_selected.recreate_map_from_folder()

        self.click_outside_menu(map_menu)

        return map_menu_left, map_menu_top, map_menu_width, map_menu_length


    def create_new_map(self, map_menu_left, map_menu_top, map_menu_width, map_menu_length):

        # Create buttons
        add_new_map_rect = pygame.Rect(map_menu_left + 30, map_menu_top + map_menu_length - 150, map_menu_width - 60, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), add_new_map_rect)

        new_map_inputfield = pygame.Rect(map_menu_left + 30, map_menu_top + map_menu_length - 80, map_menu_width - 60, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), new_map_inputfield)

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
                # Draws the tile type images
                tile_img = pygame.image.load(f'images/Tiles/{key}/{tile_type}')
                tile_img = pygame.transform.scale(tile_img, (self.tile_size, self.tile_size))
                self.screen.blit(tile_img, (base_x, base_y))

                tile_type_rect = pygame.Rect(base_x, base_y, self.tile_size, self.tile_size)

                # Example = [[Rect, Type], [Rect, Type]]
                all_tile_type_rect.append([tile_type_rect, tile_type])

                base_x += self.tile_size + 20
            base_y += self.tile_size + 20
            base_x = tile_menu_left + 20

        self.select_menu_functionality(self.selected_view_mode, all_tile_type_rect, tile_menu)

        
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
            # Draws the obstacle images
            obstacle_img = pygame.image.load(f'images/Obstacles/{obstacle_name}')
            obstacle_img = pygame.transform.scale(obstacle_img, (self.tile_size, self.tile_size))
            self.screen.blit(obstacle_img, (base_x, base_y))

            obstacle_rect = pygame.Rect(base_x, base_y, self.tile_size, self.tile_size)

            all_obstacle_rect.append([obstacle_rect, obstacle_name])

            base_x += self.tile_size + 20

        self.select_menu_functionality(self.selected_view_mode, all_obstacle_rect, obstacle_menu)

        
    def select_menu_functionality(self, menu_type, all_something_rect, something_menu):

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
                selected_img = pygame.image.load(f'images/Assets/select.png')
                selected_img = pygame.transform.scale(selected_img, (self.tile_size, self.tile_size))
                self.screen.blit(selected_img, (something_rect[0].x, something_rect[0].y))

            self.click_outside_menu(something_menu)

        
    def click_outside_menu(self, something_menu):
        # If Click outside of menu, close menu
        if not something_menu.collidepoint(self.mx, self.my):
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

        # FIXME: BUGGY MESS
        elif self.selected_view_mode == "Sequence":
            sel_path = self.map_selected.get_path(self.selected_sequence)
            seq = sel_path.get_sequence()

            if sel_path.get_start() == None:
                sel_path.set_start(x, y)
            elif seq[-1].x == x and seq[-1].y == y:
                sel_path.remove_step()
            else:
                sel_path.add_next_step(x, y)

        # TODO:
        elif self.selected_view_mode == "Obstacles":
            print(self.map_selected.get_obstacles())
            if self.click:
                if self.selected_obstacle != "None":
                    # FIXME: Bit hard to control placement
                    # FIXME: Taller than tile size
                    self.map_selected.add_obstacle(self.selected_obstacle, self.mx, self.my, 170, 284)


    def draw_tile_img(self):

        visual_tile = self.map_selected.get_visual_map()
        visual_tile_map = visual_tile.get_visual_tile_map()

        for y in range(len(visual_tile_map)):
            for x in range(len(visual_tile_map[y])):

                tile_x, tile_y = self.get_rect_param(x, y)
                tile = visual_tile.get_tile_type(x, y)

                if tile != None:
                    folder_name = tile.split("_")[1]

                    tile_img = pygame.image.load(f'images/Tiles/{folder_name}/{tile}')
                    tile_img = pygame.transform.scale(tile_img, (85, 85))
                    self.screen.blit(tile_img, (tile_x, tile_y))

        
        obstacles = self.map_selected.get_obstacles()
        for obstacle in obstacles:
            obstacle_img = pygame.image.load(f'images/Obstacles/{obstacle.get_name()}')
            obstacle_img = pygame.transform.scale(obstacle_img, (obstacle.get_width(), obstacle.get_height()) )
            self.screen.blit(obstacle_img, (obstacle.get_left(), obstacle.get_top()))


        if self.selected_view_mode == "Tower":
            tow_avail = self.map_selected.get_tower_availability_map()
            tow_avail_map = tow_avail.get_tower_availability()
            
            for y in range(len(tow_avail_map)):
                for x in range(len(tow_avail_map[y])):

                    tile_x, tile_y = self.get_rect_param(x, y)
                    tile_avail = tow_avail.get_tile_tower_avail(x, y)

                    # ADD X
                    if tile_avail == "X":
                        x_img = pygame.image.load("images/Assets/X.png")
                        x_img = pygame.transform.scale(x_img, (85, 85))
                        self.screen.blit(x_img, (tile_x, tile_y))


        elif self.selected_view_mode == "Sequence":
            sel_path = self.map_selected.get_path(self.selected_sequence)
            path_2d = sel_path.get_2d_path()

            for y in range(len(path_2d)):
                for x in range(len(path_2d[y])):
                    tile_x, tile_y = self.get_rect_param(x, y)
                    tile_num = path_2d[y][x]

                    num_img = pygame.image.load(f'images/Numbers/{tile_num}.png')
                    num_img = pygame.transform.scale(num_img, (85, 85))
                    self.screen.blit(num_img, (tile_x, tile_y))
                     
    def get_obstacles_from_image_folder(self):
        return os.listdir("images/Obstacles")