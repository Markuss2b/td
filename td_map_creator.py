import pygame
import os
import sys
import shutil
from pygame_functions import draw_text, draw_checkmark_on_menu, draw_img_on_rect, draw_transparent_img, check_button_state
from model.map.map import Map, Location, Obstacle
from model.map.tile_type_enum import get_tile_types

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

        self.load_map_error_msg = False
        
        # Function in tile_type_enum. Returns Dict  Example={"Grass": ["Grass1", "Grass2"]}
        self.all_tile_types = get_tile_types()
        self.selected_visual_tile_type = "None"

        self.all_obstacles = self.get_obstacles_from_image_folder()
        self.selected_obstacle = "None"
        self.obstacle_placement_method = "Free"

        # Boolean for on click actions
        self.click = False

        # Boolean for holding key actions
        self.hold_m1 = False

        self.last_selected_tile = None

        # Which editing view has been selected, Path, Tower availability, Visual tiles, Obstacles
        self.selected_view_mode = "Tiles"

        # Top of Screen, can select path
        self.selected_sequence = "first_path"

        self.selected_tile = None

        # Color for numbers
        self.selected_style = "Red"

        self.grid = False

        self.page = 1

        self.font = pygame.font.SysFont(None, 20)

        # List containing of all maps from all_maps folder
        self.all_maps = []

        self.path_names = ["second_path", "third_path", "fourth_path"]

        # Tiles are 85x85
        self.tile_size = 85

        self.last_hold_action = pygame.time.get_ticks()

        self.counter = 0
        self.td_map_creator_loop()


    def td_map_creator_loop(self):
        action_delay = 100

        while self.running:
            if self.selected_view_mode == "Obstacles":
                action_delay = 100
            else:
                action_delay = 10

            now = pygame.time.get_ticks()

            self.counter += 1

            self.screen.fill((0,0,0))

            self.all_maps = os.listdir("all_maps")

            self.mx, self.my = pygame.mouse.get_pos()

            main_map_rect = pygame.Rect(0, 80, 1360, 765)
            pygame.draw.rect(self.screen, (25, 25, 25), main_map_rect)

            # Stops Map Creator crashing when map is not selected
            if self.map_selected != None:

                # Tell user that a map cannot be played without proper paths
                playable_map = True
                for single_path in self.map_selected.get_all_paths():
                    if len(single_path.get_sequence()) <= 1:
                        playable_map = False
                        self.load_map_error_msg = True
                        break

                if playable_map == True:
                    self.load_map_error_msg = False
               
                self.draw_tile_img()

                if self.load_obstacle_menu == False:
                    self.draw_selected_obstacle_on_mouse()

            top_border = pygame.Rect(0, 0, 1600, 30)
            pygame.draw.rect(self.screen, (0, 75, 125), top_border)

            # Draws first so the obstacles do not get drawn outside the map
            seq_rec = []
            if self.map_selected != None:
                # Draws sequence blocks(=Amount of Paths) at the top
                for i in range(len(self.map_selected.get_all_paths())):
                    seq = pygame.Rect(40 + i * 70, 0, 60, 30)
                    if i == 0 and self.selected_sequence == "first_path" or self.selected_sequence == self.path_names[i-1] and i != 0:
                        pygame.draw.rect(self.screen, (255, 15, 0), seq)
                    else:
                        pygame.draw.rect(self.screen, (180, 0, 0), seq)

                    draw_text(f'PATH {i}', pygame.font.SysFont(None, 20), (0, 0, 0), self.screen, seq.left + 3, seq.top + 9)
                    seq_rec.append(seq)

                # Buttons for adding and removing paths    
                add_path_button = pygame.Rect(40 + len(self.map_selected.get_all_paths()) * 70, 0, 30, 30)
                remove_path_button = pygame.Rect(40 + len(self.map_selected.get_all_paths()) * 70 + 30 + 5, 0, 30, 30)
                remove_tow_avail_with_sequence_button = pygame.Rect(40 + len(self.map_selected.get_all_paths()) * 70 + 30 + 5 + 30 + 10, 0, 50, 30)
                clear_path_button = pygame.Rect(40 + len(self.map_selected.get_all_paths()) * 70 + 30 + 5 + 30 + 10 + 50 + 10, 0, 50, 30)
                undo_clear_button = pygame.Rect(40 + len(self.map_selected.get_all_paths()) * 70 + 30 + 5 + 30 + 10 + 50 + 10 + 50 + 10, 0, 30, 30)

                draw_img_on_rect(self.screen, "images/Assets/Plus.png", add_path_button.left, add_path_button.top, add_path_button.width, add_path_button.height)
                draw_img_on_rect(self.screen, "images/Assets/Minus.png", remove_path_button.left, remove_path_button.top, remove_path_button.width, remove_path_button.height)
                pygame.draw.rect(self.screen, (255, 255, 255), remove_tow_avail_with_sequence_button)
                pygame.draw.rect(self.screen, (255, 255, 255), clear_path_button)
                draw_img_on_rect(self.screen, "images/Assets/Undo.png", undo_clear_button.left, undo_clear_button.top, undo_clear_button.width, undo_clear_button.height)

                draw_text("PATH X", pygame.font.SysFont(None, 20), (0, 0, 0), self.screen, remove_tow_avail_with_sequence_button.left + 1, remove_tow_avail_with_sequence_button.top + 9)
                draw_text("CLEAR", pygame.font.SysFont(None, 20), (0, 0, 0), self.screen, clear_path_button.left + 1, clear_path_button.top + 9)

                self.handle_path_buttons(add_path_button, remove_path_button, seq_rec, clear_path_button, remove_tow_avail_with_sequence_button, undo_clear_button)


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

            if self.load_map_error_msg == True:
                draw_text("ALL PATHS MUST BE ATLEAST 2 SQUARES BIG", pygame.font.SysFont(None, 30), (255, 0, 0), self.screen, 30, map_top_border.top + map_top_border.height / 2 - 8)

            map_creator_ui = pygame.Rect(1360, 30, 240, 870)
            draw_img_on_rect(self.screen, "images/UI/MapCreator/UI_SidePanel.png", map_creator_ui.left, map_creator_ui.top, map_creator_ui.width, map_creator_ui.height)

            grid_button = pygame.Rect(1330, 30, 30, 30)
            pygame.draw.rect(self.screen, (75, 75, 75), grid_button)
            draw_text("#", pygame.font.SysFont(None, 30), (255, 255, 255), self.screen, grid_button.left + 9, grid_button.top + 5)

            save_button = pygame.Rect(1360, 850, 120, 50)
            type = check_button_state(save_button, self.mx, self.my, False, False)  
            draw_img_on_rect(self.screen, f'images/UI/MapCreator/Buttons/BTN_Save_{type}.png', save_button.left, save_button.top, save_button.width, save_button.height)

            exit_button = pygame.Rect(1480, 850, 120, 50)
            type = check_button_state(exit_button, self.mx, self.my, False, False)  
            draw_img_on_rect(self.screen, f'images/UI/MapCreator/Buttons/BTN_Exit_{type}.png', exit_button.left, exit_button.top, exit_button.width, exit_button.height)

            select_map = pygame.Rect(1400, 90, 160, 50)
            type = check_button_state(select_map, self.mx, self.my, self.load_map_menu, False)
            draw_img_on_rect(self.screen, f'images/UI/MapCreator/Buttons/Plate/BTN_SelectMap_{type}.png', select_map.left, select_map.top, select_map.width, select_map.height)

            see_tiles = pygame.Rect(1400, 190, 160, 50)
            selected = True if self.selected_view_mode == "Tiles" else False
            type = check_button_state(see_tiles, self.mx, self.my, selected, False)
            draw_img_on_rect(self.screen, f'images/UI/MapCreator/Buttons/Plate/BTN_EditTiles_{type}.png', see_tiles.left, see_tiles.top, see_tiles.width, see_tiles.height)

            open_tile_menu_button = pygame.Rect(1400, 260, 160, 50)
            disabled = True if self.selected_view_mode == "Obstacles" or self.selected_view_mode == "Tower" or self.selected_view_mode == "Sequence" else False
            type = check_button_state(open_tile_menu_button, self.mx, self.my, self.load_tile_menu, disabled)
            draw_img_on_rect(self.screen, f'images/UI/MapCreator/Buttons/Plate/BTN_SelectTile_{type}.png', open_tile_menu_button.left, open_tile_menu_button.top, open_tile_menu_button.width, open_tile_menu_button.height)

            see_obstacles = pygame.Rect(1400, 360, 160, 50)
            selected = True if self.selected_view_mode == "Obstacles" else False
            type = check_button_state(see_obstacles, self.mx, self.my, selected, False)
            draw_img_on_rect(self.screen, f'images/UI/MapCreator/Buttons/Plate/BTN_EditObstacles_{type}.png', see_obstacles.left, see_obstacles.top, see_obstacles.width, see_obstacles.height)
            
            open_obstacle_menu = pygame.Rect(1400, 430, 160, 50)
            disabled = True if self.selected_view_mode == "Tiles" or self.selected_view_mode == "Tower" or self.selected_view_mode == "Sequence" else False
            type = check_button_state(open_obstacle_menu, self.mx, self.my, self.load_obstacle_menu, disabled)
            draw_img_on_rect(self.screen, f'images/UI/MapCreator/Buttons/Plate/BTN_SelectObstacle_{type}.png', open_obstacle_menu.left, open_obstacle_menu.top, open_obstacle_menu.width, open_obstacle_menu.height)

            see_tower_avail = pygame.Rect(1400, 530, 160, 50)
            selected = True if self.selected_view_mode == "Tower" else False
            type = check_button_state(see_tower_avail, self.mx, self.my, selected, False)
            draw_img_on_rect(self.screen, f'images/UI/MapCreator/Buttons/Plate/BTN_EditTower_{type}.png', see_tower_avail.left, see_tower_avail.top, see_tower_avail.width, see_tower_avail.height)
            
            see_sequence = pygame.Rect(1400, 600, 160, 50)
            selected = True if self.selected_view_mode == "Sequence" else False
            type = check_button_state(see_sequence, self.mx, self.my, selected, False)
            draw_img_on_rect(self.screen, f'images/UI/MapCreator/Buttons/Plate/BTN_EditPath_{type}.png', see_sequence.left, see_sequence.top, see_sequence.width, see_sequence.height)

            red_style_button = pygame.Rect(1400, 660, 70, 70)
            blue_style_button = pygame.Rect(1490, 660, 70, 70)
            white_style_button = pygame.Rect(1445, 740, 70, 70)
            pygame.draw.rect(self.screen, (0, 0, 0), red_style_button)
            pygame.draw.rect(self.screen, (0, 0, 0), blue_style_button)
            pygame.draw.rect(self.screen, (0, 0, 0), white_style_button)
            draw_img_on_rect(self.screen, "images/Numbers/Red/1.png", red_style_button.left, red_style_button.top, red_style_button.width-1, red_style_button.height-1)
            draw_img_on_rect(self.screen, "images/Numbers/Blue/1.png", blue_style_button.left, blue_style_button.top, blue_style_button.width-1, blue_style_button.height-1)
            draw_img_on_rect(self.screen, "images/Numbers/White/1.png", white_style_button.left, white_style_button.top, white_style_button.width-1, white_style_button.height-1)

            # For now, have to manually add if i add any buttons
            self.handle_style(red_style_button, blue_style_button, white_style_button)
            self.handle_buttons(select_map, save_button, exit_button, see_tiles, see_tower_avail, see_sequence, tile_map, open_tile_menu_button, open_obstacle_menu, see_obstacles, grid_button)


            draw_text("CREATOR", self.font, (255, 255, 255), self.screen, 900, 16)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.screen.fill((0, 0, 0))
                    sys.exit()
                
                # Inputs 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        
                        # For unselecting obstacle
                        if self.selected_view_mode == "Obstacles" and self.selected_obstacle != "None" and self.load_obstacle_menu == False:
                            self.selected_obstacle = "None"

                        self.load_map_menu = False
                        self.load_tile_menu = False
                        self.load_obstacle_menu = False
                        self.page = 1

                        # Without this click would stay TRUE (if clicked on anything) and would click on anything hovered after closing the POP-UP
                        self.click = False

                    if self.naming_new_map == True:
                        if event.key == pygame.K_BACKSPACE:
                            self.new_map_name = self.new_map_name[:-1]
                        else:
                            if len(self.new_map_name) < 10:
                                self.new_map_name += event.unicode
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True


            # For Removing or Returning Obstacles while holding a button
            if self.map_selected != None:
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    if len(self.map_selected.get_obstacles()) > 0:
                        if now - self.last_hold_action > action_delay:
                            self.map_selected.remove_obstacle()
                            self.last_hold_action = now

                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    if len(self.map_selected.get_removed_obstacles()) > 0:
                        if now - self.last_hold_action > action_delay:
                            self.map_selected.return_removed_obstacle()
                            self.last_hold_action = now


            # For on hold mouse1 events, like interacting with tiles
            if pygame.mouse.get_pressed()[0]:
                if now - self.last_hold_action > action_delay:
                    self.hold_m1 = True
                    self.last_hold_action = now
                else:
                    self.hold_m1 = False
            elif not pygame.mouse.get_pressed()[0]:
                self.hold_m1 = False

            pygame.display.flip()

            # Frame rate
            self.clock.tick(60)


    def handle_buttons(self, select_map, save_button, exit_button, see_tiles, see_tower_avail, see_sequence, tile_map, open_tile_menu_button, open_obstacle_menu, see_obstacles, grid_button):

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

            if grid_button.collidepoint(self.mx, self.my):
                if self.click:
                    if self.grid == True:
                        self.grid = False
                    else:
                        self.grid = True

            # For selecting tiles in the map
            if self.map_selected != None:
                for y in range(len(tile_map)):
                    for x in range(len(tile_map[y])):
                        if tile_map[y][x].collidepoint(self.mx, self.my):

                            # Click has to be before hold, because every hold is a click, but not every click is a hold
                            if self.click:
                                # If tile type or obstacle have not been selected, will crash if tile has been clicked on
                                if (self.selected_view_mode == "Tower" or self.selected_view_mode == "Sequence" or
                                        self.selected_view_mode == "Tiles" and self.selected_visual_tile_type != "None" or
                                        self.selected_view_mode == "Obstacles" and self.selected_obstacle != "None"):
                                    
                                    self.selected_tile = Location(x, y)
                                    print(f'Selected: X = {self.selected_tile.x}, Y = {self.selected_tile.y}')
                                    self.interacting_with_tiles()
                                    self.last_selected_tile = self.selected_tile


                            elif self.hold_m1:
                                self.selected_tile = Location(x, y)
                                print(f'Selected: X = {self.selected_tile.x}, Y = {self.selected_tile.y}')

                                if self.last_selected_tile != None:
                                    if not (self.last_selected_tile.x == self.selected_tile.x and self.last_selected_tile.y == self.selected_tile.y) and (self.selected_view_mode == "Tower" or self.selected_view_mode == "Sequence"):
                                        self.interacting_with_tiles()
                                elif self.selected_view_mode == "Tower" or self.selected_view_mode == "Sequence":
                                    self.interacting_with_tiles()

                                if self.selected_view_mode == "Tiles" and self.selected_visual_tile_type != "None" or self.selected_view_mode == "Obstacles" and self.selected_obstacle != "None":
                                    self.interacting_with_tiles()

                                self.last_selected_tile = self.selected_tile

        self.click = False


    def handle_path_buttons(self, add_path_button, remove_path_button, seq_rec, clear_path_button, remove_tow_avail_with_sequence_button, undo_clear_button):
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

        # Clears path or tower_availability
        if clear_path_button.collidepoint(self.mx, self.my):
            if self.click:
                if self.selected_view_mode == "Sequence":
                    all_paths = self.map_selected.get_all_paths()
                    if self.selected_sequence == "first_path":
                        all_paths[0].make_empty_path()
                    else:
                        all_paths[self.path_names.index(self.selected_sequence)+1].make_empty_path()
                elif self.selected_view_mode == "Tower":
                    self.map_selected.get_tower_availability_map().create_empty_tower_avail_map()

        # Undo clear action
        if undo_clear_button.collidepoint(self.mx, self.my):
            if self.click:
                if self.selected_view_mode == "Sequence":
                    all_paths = self.map_selected.get_all_paths()
                    if self.selected_sequence == "first_path":
                        all_paths[0].undo_path_clear()
                    else:
                        all_paths[self.path_names.index(self.selected_sequence)+1].undo_path_clear()
                elif self.selected_view_mode == "Tower":
                    self.map_selected.get_tower_availability_map().undo_tower_availability_clear()


    def handle_style(self, red_style_button, blue_style_button, white_style_button):
        if red_style_button.collidepoint(self.mx, self.my):
            if self.click:
                self.selected_style = "Red"
        
        if blue_style_button.collidepoint(self.mx, self.my):
            if self.click:
                self.selected_style = "Blue"

        if white_style_button.collidepoint(self.mx, self.my):
            if self.click:
                self.selected_style = "White"


    def select_map_menu(self):
        map_menu_left = 530
        map_menu_top = 100
        map_menu_width = 300
        map_menu_length = 720
        map_menu = pygame.Rect(map_menu_left, map_menu_top, map_menu_width, map_menu_length)
        draw_img_on_rect(self.screen, "images/UI/T_Background4.png", map_menu_left, map_menu_top, map_menu_width, map_menu_length)

        base_x = map_menu_left + 20
        base_y = map_menu_top + 10

        # Creates a rect for every map
        all_maps_rect = []
        for i in range(len(self.all_maps)):
            map_rect = pygame.Rect(base_x, base_y + 40 * (i + 1), 230, 30)
            
            # Adds a selected button effect
            if self.map_selected != None:
                if self.map_selected.get_map_name() == self.all_maps[i]:
                    pygame.draw.rect(self.screen, (211, 211, 211), map_rect)
                    draw_img_on_rect(self.screen, "images/Assets/Grid1.png", map_rect.left, map_rect.top, map_rect.width, map_rect.height)
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), map_rect)
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), map_rect)

            draw_text(self.all_maps[i], pygame.font.SysFont(None, 30), (0, 0, 0), self.screen, map_rect.left + 5, map_rect.top + 5)

            delete_map_rect = pygame.Rect(base_x + 230, base_y + 40 * (i + 1), 30, 30)
            draw_img_on_rect(self.screen, f'images/Assets/X_{self.selected_style}.png', delete_map_rect.left, delete_map_rect.top, delete_map_rect.width, delete_map_rect.height)
            
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

                    if self.map_selected != None:
                        if self.map_selected.get_map_name() == self.all_maps[i]:
                            self.map_selected = None


        checkmark_rect = draw_checkmark_on_menu(self.screen, map_menu)
        self.click_outside_menu(map_menu, checkmark_rect)

        return map_menu_left, map_menu_top, map_menu_width, map_menu_length


    def create_new_map(self, map_menu_left, map_menu_top, map_menu_width, map_menu_length):

        # Create buttons
        add_new_map_rect = pygame.Rect(map_menu_left + 30, map_menu_top + map_menu_length - 220, map_menu_width - 60, 50)

        if add_new_map_rect.collidepoint(self.mx, self.my):
            pygame.draw.rect(self.screen, (200, 200, 200), add_new_map_rect)
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), add_new_map_rect)

        draw_text("CREATE MAP", pygame.font.SysFont(None, 50), (0, 0, 0), self.screen, add_new_map_rect.left + 3, add_new_map_rect.top + 10)

        new_map_inputfield = pygame.Rect(map_menu_left + 30, map_menu_top + map_menu_length - 150, map_menu_width - 60, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), new_map_inputfield)

        if self.naming_new_map == False:
            draw_text("Enter map name", pygame.font.SysFont(None, 40), (100, 100, 100), self.screen, new_map_inputfield.left + 5, new_map_inputfield.top + 13)
        else:
            draw_text(self.new_map_name, pygame.font.SysFont(None, 50), (0, 0, 0), self.screen, new_map_inputfield.left, new_map_inputfield.top + 10)

        # Max 10 custom maps
        if len(self.all_maps) < 10:
            # Activating input field
            if new_map_inputfield.collidepoint(self.mx, self.my):
                if self.click:
                    self.naming_new_map = True
                    self.new_map_name = ""

            # Creating a new map
            elif add_new_map_rect.collidepoint(self.mx, self.my):
                if self.click:
                    if self.new_map_name != "" and not self.new_map_name in self.all_maps:
                        self.map_selected = Map(self.new_map_name, 16, 9)
                        self.map_selected.create_map_folder()
                        self.map_selected.initialize_all_maps()
                        self.map_selected.save_map()

                        self.selected_view_mode = "Tiles"
                        self.new_map_name = ""

            elif self.click:
                self.naming_new_map = False
                self.new_map_name = "" 


    def open_tile_menu(self):
        tile_menu_left = 370
        tile_menu_top = 100
        tile_menu_width = 545
        tile_menu_length = 700
        tile_menu = pygame.Rect(tile_menu_left, tile_menu_top, tile_menu_width, tile_menu_length)
        draw_img_on_rect(self.screen, "images/UI/T_Background4.png", tile_menu_left, tile_menu_top, tile_menu_width, tile_menu_length)

        all_tile_type_rect = []

        base_x = tile_menu_left + 20
        base_y = tile_menu_top + 20

        loop = 0

        for key in self.all_tile_types.keys():

            if loop+1 > self.page * 5:
                break
            elif loop+1 > (self.page - 1) * 5:
                for tile_type in self.all_tile_types.get(key):
                    tile_type_rect = pygame.Rect(base_x, base_y, self.tile_size, self.tile_size)

                    # Draws the tile type images
                    draw_img_on_rect(self.screen, f'images/Tiles/{key}/{tile_type}', base_x, base_y, self.tile_size, self.tile_size)

                    # Example = [[Rect, Type], [Rect, Type]]
                    all_tile_type_rect.append([tile_type_rect, tile_type])

                    base_x += self.tile_size + 20
                base_y += self.tile_size + 20
                base_x = tile_menu_left + 20
            loop += 1

        checkmark_rect = draw_checkmark_on_menu(self.screen, tile_menu)

        self.change_page(checkmark_rect, len(self.all_tile_types) * 5)

        self.select_menu_functionality(self.selected_view_mode, all_tile_type_rect, tile_menu,checkmark_rect)

        
    def open_obstacle_menu(self):
        obstacle_menu_left = 370
        obstacle_menu_top = 100
        obstacle_menu_width = 545
        obstacle_menu_length = 700
        obstacle_menu = pygame.Rect(obstacle_menu_left, obstacle_menu_top, obstacle_menu_width, obstacle_menu_length)
        draw_img_on_rect(self.screen, "images/UI/T_Background4.png", obstacle_menu_left, obstacle_menu_top, obstacle_menu_width, obstacle_menu_length)

        all_obstacle_rect = []
        base_x = obstacle_menu_left + 20
        base_y = obstacle_menu_top + 20

        for i in range(len(self.all_obstacles)):
            
            if i+1 > self.page * 25:
                break
            elif i+1 > (self.page - 1) * 25:
                obstacle_name = self.all_obstacles[i]

                obstacle_rect = pygame.Rect(base_x, base_y, self.tile_size, self.tile_size)
                # Draws the obstacle images
                draw_img_on_rect(self.screen, f'images/Obstacles/{obstacle_name}', base_x, base_y, self.tile_size, self.tile_size)

                all_obstacle_rect.append([obstacle_rect, obstacle_name])

                base_x += self.tile_size + 20

                # 5 in a row
                if (i+1) % 5 == 0:
                    base_x = obstacle_menu_left + 20
                    base_y += self.tile_size + 20

        checkmark_rect = draw_checkmark_on_menu(self.screen, obstacle_menu)

        self.change_obstacle_placement_method(checkmark_rect)
        self.change_page(checkmark_rect, len(self.all_obstacles))

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
                draw_img_on_rect(self.screen, f'images/Assets/select.png', something_rect[0].x, something_rect[0].y, self.tile_size, self.tile_size)

            self.click_outside_menu(something_menu, checkmark_rect)

        
    def click_outside_menu(self, something_menu, checkmark_rect):
        # If Click outside of menu, close menu
        if not something_menu.collidepoint(self.mx, self.my) or checkmark_rect.collidepoint(self.mx, self.my):
            if self.click:
                self.hold_m1 = False
                self.last_hold_action = pygame.time.get_ticks()
                self.load_obstacle_menu = False
                self.load_tile_menu = False
                self.load_map_menu = False
                self.page = 1


    # Gets accurate UI Location for Tile
    def get_rect_param(self, x, y):
        # LEFT, TOP
        return x * 85, y * 85 + 80
    

    def get_xy_from_cords(self, x, y):
        return int(x / 85), int(y / 85) - 1


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
                        draw_img_on_rect(self.screen, f'images/Assets/X_{self.selected_style}.png', left, top, self.tile_size, self.tile_size)
            else:
                sel_path.add_next_step(x, y)

        elif self.selected_view_mode == "Obstacles":
            new_image_width, new_image_height, path = self.get_obstacle_sizes()

            if self.obstacle_placement_method == "Free":
                left, top = self.get_free_obstacle_left_top(new_image_width, new_image_height)
                self.map_selected.add_obstacle(self.selected_obstacle, left, top, new_image_width, new_image_height)
            if self.obstacle_placement_method == "Tile":
                left, top = self.get_rect_param(x, y)
                left = left - 20

                # TODO: Scuffed
                if new_image_height >= 200:
                    top = top - self.tile_size - new_image_height/5
                elif new_image_height >= 120:
                    top = top - 20

                obstacle_already_exists = False
                for obstacle in self.map_selected.get_obstacles():
                    if obstacle.get_left() == left and obstacle.get_top() == top:
                        obstacle_already_exists = True
                        
                if obstacle_already_exists == False:
                    self.map_selected.add_obstacle(self.selected_obstacle, left, top, new_image_width, new_image_height)


    def draw_tile_img(self):

        visual_tile = self.map_selected.get_visual_map()
        visual_tile_map = visual_tile.get_visual_tile_map()

        for y in range(len(visual_tile_map)):
            for x in range(len(visual_tile_map[y])):

                tile_x, tile_y = self.get_rect_param(x, y)
                tile = visual_tile.get_tile_type(x, y)

                if tile != None:
                    folder_name = tile.split("_")[1]

                    draw_img_on_rect(self.screen, f'images/Tiles/{folder_name}/{tile}', tile_x, tile_y, self.tile_size, self.tile_size)
                    
                    # Draws border around each tile
                    if self.grid == True:
                        draw_img_on_rect(self.screen, f'images/Assets/Grid2.png', tile_x, tile_y, self.tile_size, self.tile_size)

        
        obstacles = self.sort_obstacles_from_top_descending()
        for obstacle in obstacles:
            draw_img_on_rect(self.screen, f'images/Obstacles/{obstacle.get_name()}', obstacle.get_left(), obstacle.get_top(), obstacle.get_width(), obstacle.get_height())


        if self.selected_view_mode == "Tower":
            tow_avail = self.map_selected.get_tower_availability_map()
            tow_avail_map = tow_avail.get_tower_availability()
            
            for y in range(len(tow_avail_map)):
                for x in range(len(tow_avail_map[y])):

                    tile_x, tile_y = self.get_rect_param(x, y)
                    tile_avail = tow_avail.get_tile_tower_avail(x, y)

                    # ADD X
                    if tile_avail == "X":
                        draw_img_on_rect(self.screen, f'images/Assets/X_{self.selected_style}.png', tile_x, tile_y, self.tile_size, self.tile_size)


        elif self.selected_view_mode == "Sequence":
            sel_path = self.map_selected.get_path(self.selected_sequence)
            path_2d = sel_path.get_2d_path()

            for y in range(len(path_2d)):
                for x in range(len(path_2d[y])):
                    tile_x, tile_y = self.get_rect_param(x, y)
                    tile_num = path_2d[y][x]

                    if tile_num > 0:
                        draw_img_on_rect(self.screen, f'images/Numbers/{self.selected_style}/{tile_num}.png', tile_x, tile_y, self.tile_size-1, self.tile_size-1)


    def draw_selected_obstacle_on_mouse(self):
        if self.selected_obstacle != "None" and self.selected_view_mode == "Obstacles":
            new_image_width, new_image_height, path = self.get_obstacle_sizes()

            if self.obstacle_placement_method == "Free":
                left, top = self.get_free_obstacle_left_top(new_image_width, new_image_height)
            elif self.obstacle_placement_method == "Tile":
                x, y = self.get_xy_from_cords(self.mx, self.my)
                left, top = self.get_rect_param(x, y)
                left = left - 20

                # TODO: Scuffed
                if new_image_height >= 200:
                    top = top - self.tile_size - new_image_height/5
                elif new_image_height >= 120:
                    top = top - 20
            draw_transparent_img(self.screen, path, left, top, new_image_width, new_image_height)


    def get_obstacle_sizes(self):
            path = f'images/Obstacles/{self.selected_obstacle}'
            obstacle_image = pygame.image.load(path)
            original_image_width, original_image_height = obstacle_image.get_size()
            new_image_width = original_image_width * 2
            new_image_height = original_image_height * 2

            return new_image_width, new_image_height, path
    

    def get_free_obstacle_left_top(self, new_image_width, new_image_height):
        left = self.mx - self.tile_size/2 - 10
        top = self.my - new_image_height + self.tile_size/2
        return left, top
    
                     
    def get_obstacles_from_image_folder(self):
        return os.listdir("images/Obstacles")
    
    
    def change_obstacle_placement_method(self, example_rect):
        # Checkbox, 
        change_obstacle_placement_method_rect = pygame.Rect(example_rect.left, example_rect.top - 60, example_rect.width, example_rect.height)
        pygame.draw.rect(self.screen, (80, 80, 80), change_obstacle_placement_method_rect)
        draw_text("LOCK:", pygame.font.SysFont(None, 40), (255, 255, 255), self.screen, change_obstacle_placement_method_rect.left - 95, change_obstacle_placement_method_rect.top + 12)
        if self.obstacle_placement_method == "Tile":
            draw_img_on_rect(self.screen, f'images/Assets/X_{self.selected_style}.png', change_obstacle_placement_method_rect.left, change_obstacle_placement_method_rect.top, change_obstacle_placement_method_rect.width, change_obstacle_placement_method_rect.height)

        if change_obstacle_placement_method_rect.collidepoint(self.mx, self.my):
            if self.click:
                if self.obstacle_placement_method == "Free":
                    self.obstacle_placement_method = "Tile"
                elif self.obstacle_placement_method == "Tile":
                    self.obstacle_placement_method = "Free"

    
    def change_page(self, example_rect, len_of_all):
        page_back = pygame.Rect(example_rect.left, example_rect.top - 90, 20, 20)
        page_forwards = pygame.Rect(example_rect.left + 30, example_rect.top - 90, 20, 20)

        disabled = False if self.page != 1 and self.page > len_of_all / 25 else True
        type = check_button_state(page_back, -1, -1, False, disabled)
        draw_img_on_rect(self.screen, f'images/UI/Page/BTN_Back_{type}.png', page_back.left, page_back.top, page_back.width, page_back.height)

        disabled = False if self.page < len_of_all / 25 else True
        type = check_button_state(page_forwards, -1, -1, False, disabled)
        draw_img_on_rect(self.screen, f'images/UI/Page/BTN_Forward_{type}.png', page_forwards.left, page_forwards.top, page_forwards.width, page_forwards.height)

        if page_back.collidepoint(self.mx, self.my):
            if self.click:
                if self.page != 1 and self.page > len_of_all / 25:
                    self.page -= 1
        
        if page_forwards.collidepoint(self.mx, self.my):
            if self.click:
                if self.page < len_of_all / 25:
                    self.page += 1


    def sort_obstacles_from_top_descending(self):
        obstacles = self.map_selected.get_obstacles()
        sorted_obstacles = sorted(obstacles , key=lambda obstacle: obstacle.get_top())
        return sorted_obstacles
    