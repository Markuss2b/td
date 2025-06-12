import pygame
import os
import time
import copy
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from db_functions import get_tower_with_name, add_profile_win_by_name, add_profile_loss_by_name, add_game_in_history, get_profile_with_name
from pyopengl_functions import load_texture, unload_texture, create_shader, draw_quad_2, draw_quads_2, destroy
from pygame_functions import check_button_state
from model.map.map import Map
from model.map.premade_map import PremadeMap
from model.tower import Tower
from model.enemy import Enemy
from model.game_wave import Wave

# TODO: Select tower
# TODO: Towers in menu
# FIXME: Transparent finish only looks good in premade maps
class TDGame:
    def __init__(self, view_state):
        self.view_state = view_state
        self.clock = pygame.time.Clock()

        self.display_size = (1600, 900)
        self.screen = pygame.display.set_mode(self.display_size, pygame.OPENGL|pygame.DOUBLEBUF)

        self.selected_profile = view_state.get_selected_profile()
        self.map_selected = view_state.get_map_selected()
        self.tower_avail = self.map_selected.get_tower_availability_map()
        self.sequences = [path.get_sequence() for path in self.map_selected.get_all_paths()]

        self.selected_sequence = 0
        # self.game_waves = [Wave(1000, 0, 10, 0), Wave(1000, 0, 20, 0), Wave(500, 0, 1, 0), Wave(500, 0, 1, 0), Wave(500, 0, 1, 0)]
        # self.game_waves = [Wave(500, 100, 20, 10)]
        self.game_waves = [Wave(200, 10, 0, 0), Wave(350, 20, 5, 0), Wave(500, 10, 5, 3), Wave(500, 15, 5, 5), Wave(150, 200, 0, 0), Wave(100, 1, 0, 0)]
        self.current_wave = 0

        self.click = False
        self.mx = 0
        self.my = 0
        self.tile_size = 85

        self.tile_textures = {}
        self.obstacle_textures = {}
        self.tower_textures = {}
        self.enemy_textures = {}
        self.assets_textures = {}
        self.UI_textures = {}
        self.bullet_textures = {}
        # Other textures

        self.static_tile = False
        self.static_obstacles = False
        self.static_UI = False


        self.texture_ids_with_quads = {}

        self.premade_map_texture = None

        self.tower_selected = None

        self.stickman = get_tower_with_name("Stickman")

        self.towers_on_map = []

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(2 * 4))

        self.shader = create_shader(vertex_path = "shaders/vertex.txt", fragment_path = "shaders/new_fragment.txt")
        glUseProgram(self.shader)
        self.alpha = 1

        self.enemies_on_map = []
        self.last_spawn = pygame.time.get_ticks()

        self.bullets_on_map = []

        self.health = 50
        self.pause = True
        self.game_end = False
        self.result = ""
        self.profile_updated = False
        self.towers_placed_amount = 0
        self.game_start_time = time.time()
        self.game_end_time = None

        self.trash_selected = False

        self.running = True
        self.td_game_loop()

    def td_game_loop(self):

        # Always load
        self.load_tower_textures()
        self.load_enemy_textures()
        self.load_UI_textures()
        self.load_bullet_textures()

        # Load all textures

        if self.map_selected.get_map_type() == "Map":
            self.load_tile_textures()
            self.load_obstacle_textures()
        elif self.map_selected.get_map_type() == "PremadeMap":
            self.load_premade_map_textures()

        self.group_textures_2()


        # If loading save file
        if len(self.view_state.get_saved_game()):
            # TODO: Only tower
            self.tower_selected = self.stickman
            self.current_wave = self.view_state.get_saved_game()[0]
            self.health = self.view_state.get_saved_game()[1]

            towers = self.view_state.get_saved_game()[2]
            for tower in towers:
                tower = tower.replace("\n", "")
                tower = tower.split(",")
                
                name = tower[0]
                x = int(tower[1])
                y = int(tower[2])
                self.place_tower(x, y)
            
            self.view_state.set_saved_game([])

        # MOVEMENT
        delay = 16.67
        last_event = pygame.time.get_ticks()

        # Add delay to waves ?
        last_spawn_delay = self.game_waves[self.current_wave].get_spawn_delay()
        self.game_waves[self.current_wave].create_wave()

        while self.running:
            print(self.texture_ids_with_quads)
            # Swapping waves / Game over
            if len(self.game_waves[self.current_wave].get_enemies()) == 0 and len(self.enemies_on_map) == 0:
                self.pause = True

                if len(self.sequences) > 1:
                    if not self.selected_sequence == len(self.sequences)-1:
                        self.selected_sequence += 1
                    else:
                        self.selected_sequence = 0

                if self.current_wave < len(self.game_waves)-1:
                    self.current_wave += 1
                    self.game_waves[self.current_wave].create_wave()
                    last_spawn_delay = self.game_waves[self.current_wave].get_spawn_delay()

                if self.current_wave == len(self.game_waves)-1 and len(self.enemies_on_map) == 0 and self.pause == True:
                    self.game_end = True
                    self.result = "Won"
                    if self.profile_updated == False:
                        self.profile_updated = True
                        add_profile_win_by_name(self.selected_profile.get_name())

                        # Game history
                        self.game_end_time = time.time()
                        profile = get_profile_with_name(self.selected_profile.get_name())
                        profile_id = profile[0]
                        add_game_in_history(profile_id, self.map_selected.get_map_name(), "Win", self.current_wave+1, self.towers_placed_amount, int(self.game_end_time - self.game_start_time))
                        
                
            if self.health <= 0:
                self.game_end = True
                self.result = "Lost"
                if self.profile_updated == False:
                    self.profile_updated = True
                    add_profile_loss_by_name(self.selected_profile.get_name())

                    # Game history
                    self.game_end_time = time.time()
                    profile = get_profile_with_name(self.selected_profile.get_name())
                    profile_id = profile[0]
                    add_game_in_history(profile_id, self.map_selected.get_map_name(), "Loss", self.current_wave+1, self.towers_placed_amount, int(self.game_end_time - self.game_start_time))


            self.mx, self.my = pygame.mouse.get_pos()
            self.click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                    if self.map_selected.get_map_type() == "Map":
                    # Unload textures when code stops running
                        for texture_id in self.tile_textures.values():
                            unload_texture(texture_id)

                        for texture_id in self.obstacle_textures.values():
                            unload_texture(texture_id)
                    elif self.map_selected.get_map_type() == "PremadeMap":
                        unload_texture(self.premade_map_texture)

                    # Always unload
                    for texture_id in self.UI_textures.values():
                        unload_texture(texture_id)

                    for texture_id in self.enemy_textures.values():
                        unload_texture(texture_id)

                    for texture_id in self.tower_textures.values():
                        unload_texture(texture_id)

                    glDeleteProgram(self.shader)
                    destroy(self.vao, self.vbo)

                    pygame.quit()
                    quit()
                    self.view_state.set_quit(True)
                
                # Inputs 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.tower_selected = None


            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


            if self.game_end == True:
                self.alpha = 0.3

            if self.map_selected.get_map_type() == "Map":
                self.draw_map()

                if self.game_end != True:
                    self.draw_obstacles()
                else:
                    self.remove_obstacles()

            elif self.map_selected.get_map_type() == "PremadeMap":
                self.draw_premade_map()

            # Always draw
            self.draw_towers()

            start = time.time()
            draw_quads_2(self.texture_ids_with_quads, self.shader, self.vbo, self.alpha)
            end = time.time()
            # print(f'Time: {start-end}')

            self.draw_UI()

            # TODO: MOVEMENT
            now = pygame.time.get_ticks()
            if now - last_event > delay:
                last_event += delay

                self.move_enemies()

            
            self.draw_enemies()


            # Spawning enemy
            if self.pause == False:
                if len(self.game_waves[self.current_wave].get_enemies()) > 0:
                    now = pygame.time.get_ticks()
                    if now - self.last_spawn > last_spawn_delay:
                        self.last_spawn += last_spawn_delay
                        self.enemies_on_map.append(self.game_waves[self.current_wave].spawn_enemy(copy.copy(self.sequences[self.selected_sequence])))

            # Placing Tower
            if self.click:
                x, y = self.get_xy_from_cords(self.mx, self.my)

                if x >= 0 and x <= 15 and y >= 0 and y <= 8:

                    if self.trash_selected == False:
                        if self.tower_selected != None:
                            self.place_tower(x, y)
                    else:
                        self.remove_tower(x, y)

            # Shooting
            self.towers_fire()

            # Bullets
            self.move_bullets()

            # print(self.bullet_textures)
            self.draw_bullets()

            if self.game_end == True:
                self.draw_game_end_popup()


            pygame.display.flip()

            # Frame rate
            self.clock.tick(60)
        

    def load_tile_textures(self):
        all_tile_images = []
        folders = os.listdir("images/Tiles")
        for folder in folders:
            path_to_img = f'images/Tiles/{folder}'
            folder_images = os.listdir(path_to_img)
            all_tile_images = all_tile_images + [[image_name, path_to_img] for image_name in folder_images]

        # Example: {T_Grass_1.png : 1, ....}
        self.tile_textures = { k[0]:load_texture(f'{k[1]}/{k[0]}') for k in all_tile_images }
            

    def load_obstacle_textures(self):
        obstacle_path = "images/Obstacles"
        all_obstacle_images = os.listdir(obstacle_path)
        self.obstacle_textures = { k:load_texture(f'{obstacle_path}/{k}') for k in all_obstacle_images }

    def load_enemy_textures(self):
        enemies_path = "images/Enemies"
        all_enemy_images = os.listdir(enemies_path)
        self.enemy_textures = { k:load_texture(f'{enemies_path}/{k}') for k in all_enemy_images }

    def load_tower_textures(self):
        towers_path = "images/Towers"
        all_tower_images = os.listdir(towers_path)
        self.tower_textures = { k:load_texture(f'{towers_path}/{k}') for k in all_tower_images }

    def load_assets_textures(self):
        pass

    # FIXME: UNORGANIZED
    def load_UI_textures(self):
        self.UI_textures["UI_SidePanel.png"] = load_texture(f'images/UI/MapCreator/UI_SidePanel.png') 
        self.UI_textures["T_CharacterSelectionBackground.png"] = load_texture(f'images/UI/Game/T_CharacterSelectionBackground.png')
        self.UI_textures["BTN_PlayButton_Unselected.png"] = load_texture(f'images/UI/Game/BTN_PlayButton_Unselected.png')
        self.UI_textures["BTN_PlayButton_Hovered.png"] = load_texture(f'images/UI/Game/BTN_PlayButton_Hovered.png')
        self.UI_textures["BTN_TrashButton_Hovered.png"] = load_texture(f'images/UI/Game/BTN_TrashButton_Hovered.png')
        self.UI_textures["BTN_TrashButton_Unselected.png"] = load_texture(f'images/UI/Game/BTN_TrashButton_Unselected.png')
        self.UI_textures["BTN_Return_Unselected.png"] = load_texture(f'images/UI/Game/BTN_Return_Unselected.png')
        self.UI_textures["BTN_SaveAndExit_Unselected.png"] = load_texture(f'images/UI/Game/BTN_SaveAndExit_Unselected.png')
        self.UI_textures["BTN_SaveAndExit_Disabled.png"] = load_texture(f'images/UI/Game/BTN_SaveAndExit_Disabled.png')
        self.UI_textures["BTN_Return_Hovered.png"] = load_texture(f'images/UI/Game/BTN_Return_Hovered.png')
        self.UI_textures["BTN_SaveAndExit_Hovered.png"] = load_texture(f'images/UI/Game/BTN_SaveAndExit_Hovered.png')
        self.UI_textures["T_DestroyTowers.png"] = load_texture(f'images/UI/Game/T_DestroyTowers.png')
        self.UI_textures["BTN_Back.png"] = load_texture(f'images/UI/Game/GameEnd/BTN_Back.png')
        self.UI_textures["BTN_Retry.png"] = load_texture(f'images/UI/Game/GameEnd/BTN_Retry.png')
        self.UI_textures["T_YouLost.png"] = load_texture(f'images/UI/Game/GameEnd/T_YouLost.png')
        self.UI_textures["T_YouWon.png"] = load_texture(f'images/UI/Game/GameEnd/T_YouWon.png')
        self.UI_textures["T_GameEndBackground.png"] = load_texture(f'images/UI/Game/GameEnd/T_GameEndBackground.png')
        self.UI_textures["BTN_Next.png"] = load_texture(f'images/UI/Game/GameEnd/BTN_Next.png')
        self.UI_textures["T_TopBorder_Green.png"] = load_texture(f'images/UI/Game/T_TopBorder_Green.png')
        self.UI_textures["T_BottomBorder_Green.png"] = load_texture(f'images/UI/Game/T_BottomBorder_Green.png')
        self.UI_textures["T_TopBorder_Red.png"] = load_texture(f'images/UI/Game/T_TopBorder_Red.png')
        self.UI_textures["T_BottomBorder_Red.png"] = load_texture(f'images/UI/Game/T_BottomBorder_Red.png')
        self.UI_textures["T_Background4.png"] = load_texture(f'images/UI/T_Background4.png')
        self.UI_textures["select.png"] = load_texture(f'images/Assets/select.png')
        self.UI_textures["redpixel.png"] = load_texture(f'images/redpixel.png')
        self.UI_textures["blackpixel.png"] = load_texture(f'images/blackpixel.png')

    # TODO:
    def load_bullet_textures(self):
        bullet_path = "images/Bullets"
        all_bullet_images = os.listdir(bullet_path)
        self.bullet_textures = { k:load_texture(f'{bullet_path}/{k}') for k in all_bullet_images }

    def load_premade_map_textures(self):
        self.premade_map_texture = load_texture(f'predrawn_maps/{self.map_selected.get_map_name()}/map_image.png')


    def group_textures(self):
        all_textures = self.tile_textures | self.enemy_textures | self.UI_textures | self.tower_textures | self.assets_textures | self.obstacle_textures 
        self.texture_ids_with_quads = { all_textures.get(k):[] for k in all_textures }

    
    def group_textures_2(self):
        self.texture_ids_with_quads["UI"] = { self.UI_textures.get(k):[] for k in self.UI_textures }
        self.texture_ids_with_quads["TILE"] = { self.tile_textures.get(k):[] for k in self.tile_textures }
        self.texture_ids_with_quads["TOWER"] = { self.tower_textures.get(k):[] for k in self.tower_textures }
        self.texture_ids_with_quads["ENEMY"] = { self.enemy_textures.get(k):[] for k in self.enemy_textures }
        self.texture_ids_with_quads["ASSETS"] = { self.assets_textures.get(k):[] for k in self.assets_textures }
        self.texture_ids_with_quads["BULLET"] = { self.bullet_textures.get(k):[] for k in self.bullet_textures }
        self.texture_ids_with_quads["OBSTACLES"] = { self.obstacle_textures.get(k):[] for k in self.obstacle_textures }

    
    # Inefficient drawing
    def draw_UI(self):

        if self.health > 0:
            draw_quad_2(0, 0, 800 - 16 * self.health, 30, self.UI_textures.get("blackpixel.png"), self.shader, self.vbo, self.alpha)
            draw_quad_2(800 - 16 * self.health, 0, 32 * self.health, 30, self.UI_textures.get("redpixel.png"), self.shader, self.vbo, self.alpha)
            draw_quad_2(800 + 16 * self.health, 0, 800 - 16 * self.health, 30, self.UI_textures.get("blackpixel.png"), self.shader, self.vbo, self.alpha)

        draw_quad_2(1360, 30, 240, 870, self.UI_textures.get("UI_SidePanel.png"), self.shader, self.vbo, self.alpha)

        draw_quad_2(1370, 40, 220, 460, self.UI_textures.get("T_CharacterSelectionBackground.png"), self.shader, self.vbo, self.alpha)

        if self.pause == True and self.health > 0:
            img = "Green"
        else:
            img = "Red"
        draw_quad_2(0, 30, 1360, 50, self.UI_textures.get(f'T_TopBorder_{img}.png'), self.shader, self.vbo, self.alpha)
        draw_quad_2(0, 845, 1360, 55, self.UI_textures.get(f'T_BottomBorder_{img}.png'), self.shader, self.vbo, self.alpha)

        select_balloon_rect = pygame.Rect(1456, 60, 50, 50)
        draw_quad_2(select_balloon_rect.left, select_balloon_rect.top, select_balloon_rect.width, select_balloon_rect.height, self.bullet_textures.get("Balloon.png"), self.shader, self.vbo, self.alpha)
        
        stickman_border = pygame.Rect(1440, 120, 85, 85)
        draw_quad_2(stickman_border.left, stickman_border.top, stickman_border.width, stickman_border.height, self.UI_textures.get("T_Background4.png"), self.shader, self.vbo, self.alpha)
        stickman_rect = pygame.Rect(1440, 120, 85, 85)
        draw_quad_2(stickman_rect.left, stickman_rect.top, stickman_rect.width, stickman_rect.height, self.tower_textures.get("C_Stickman_D.png"), self.shader, self.vbo, self.alpha)
        if self.tower_selected != None:
            draw_quad_2(stickman_rect.left + 3, stickman_rect.top + 5, stickman_rect.width - 6, stickman_rect.height - 10, self.UI_textures.get("select.png"), self.shader, self.vbo, self.alpha)

        play_button_rect = pygame.Rect(1360, 520, 240, 131)
        active = False if self.pause == True else True
        type = check_button_state(play_button_rect, self.mx, self.my, active, False)
        img = f"BTN_PlayButton_{type}.png"
        draw_quad_2(play_button_rect.left, play_button_rect.top, play_button_rect.width, play_button_rect.height, self.UI_textures.get(img), self.shader, self.vbo, self.alpha)

        trash_button_rect = pygame.Rect(1360 + 120 - 35, 660, 70, 70)
        type = check_button_state(trash_button_rect, self.mx, self.my, self.trash_selected, False)
        img = f"BTN_TrashButton_{type}.png"
        draw_quad_2(trash_button_rect.left, trash_button_rect.top, trash_button_rect.width, trash_button_rect.height, self.UI_textures.get(img), self.shader, self.vbo, self.alpha)

        destroy_towers_rect = pygame.Rect(1360 + 10, 673, 70, 40)
        draw_quad_2(destroy_towers_rect.left, destroy_towers_rect.top, destroy_towers_rect.width, destroy_towers_rect.height, self.UI_textures.get("T_DestroyTowers.png"), self.shader, self.vbo, self.alpha)

        return_to_menu_rect = pygame.Rect(1360, 820, 240, 70)
        type = check_button_state(return_to_menu_rect, self.mx, self.my, False, False)
        img = f"BTN_Return_{type}.png"
        draw_quad_2(return_to_menu_rect.left, return_to_menu_rect.top, return_to_menu_rect.width, return_to_menu_rect.height, self.UI_textures.get(img), self.shader, self.vbo, self.alpha)

        save_and_exit_rect = pygame.Rect(1360, 740, 240, 70)
        disabled = True if self.pause != True else False
        type = check_button_state(save_and_exit_rect, self.mx, self.my, False, disabled)
        img = f"BTN_SaveAndExit_{type}.png"
        draw_quad_2(save_and_exit_rect.left, save_and_exit_rect.top, save_and_exit_rect.width, save_and_exit_rect.height, self.UI_textures.get(img), self.shader, self.vbo, self.alpha)

        self.handle_UI_buttons(stickman_rect, play_button_rect, return_to_menu_rect, save_and_exit_rect, trash_button_rect)
    

    def handle_UI_buttons(self, stickman_rect, play_button_rect, return_to_menu_rect, save_and_exit_rect, trash_button_rect):
        if stickman_rect.collidepoint(self.mx, self.my):
            if self.click:

                # TODO: towers
                self.tower_selected = self.stickman
        
        if play_button_rect.collidepoint(self.mx, self.my):
            if self.click:
                self.pause = False
                self.last_spawn = pygame.time.get_ticks()
                
                for tower in self.towers_on_map:
                    tower.reset_last_attack()

        if return_to_menu_rect.collidepoint(self.mx, self.my):
            if self.click:
                self.running = False
                self.view_state.set_state("menu")

        if self.pause == True:
            if save_and_exit_rect.collidepoint(self.mx, self.my):
                if self.click:
                    save_path = f'saved_games/{self.selected_profile.get_name()}.txt'
                    with open(save_path, "w") as f:
                        f.write(f'{self.map_selected.get_map_name()}\n')
                        f.write(f'{self.current_wave}\n')
                        f.write(f'{self.health}\n')
                        for tower in self.towers_on_map:
                            loc = tower.get_location()
                            f.write(f'{tower.get_name()},{loc[0]},{loc[1]}\n')

                    self.running = False
                    self.view_state.set_state("menu")

        if trash_button_rect.collidepoint(self.mx, self.my):
            if self.click:
                if self.trash_selected == False:
                    self.tower_selected = None
                    self.trash_selected = True
                else:
                    self.trash_selected = False


    def draw_map(self):
        visual_tile = self.map_selected.get_visual_map()
        visual_tile_map = visual_tile.get_visual_tile_map()

        for y in range(len(visual_tile_map)):
            for x in range(len(visual_tile_map[y])):

                tile_x, tile_y = self.get_rect_param(x, y)
                tile = visual_tile.get_tile_type(x, y)

                if tile != None:
                    if self.static_tile == False:
                        self.texture_ids_with_quads.get("TILE").get(self.tile_textures.get(tile)).append((tile_x, tile_y, self.tile_size, self.tile_size))
                    
                    # draw_quad(tile_x, tile_y, self.tile_size, self.tile_size, self.tile_textures.get(tile))

        self.static_tile = True

                    
    def draw_obstacles(self):
        obstacles = self.sort_obstacles_from_top_descending()
        for obstacle in obstacles:
            if self.static_obstacles == False:
                self.texture_ids_with_quads.get("OBSTACLES").get(
                    self.obstacle_textures.get(obstacle.get_name())).append( (obstacle.get_left(), obstacle.get_top(), obstacle.get_width(), obstacle.get_height())
                )
            # draw_quad(obstacle.get_left(), obstacle.get_top(), obstacle.get_width(), obstacle.get_height(), self.obstacle_textures.get(obstacle.get_name()))

        self.static_obstacles = True


    def remove_obstacles(self):
        obstacles = self.sort_obstacles_from_top_descending()
        for obstacle in obstacles:
            self.texture_ids_with_quads.get("OBSTACLES").get(self.obstacle_textures.get(obstacle.get_name())).clear()


    def draw_premade_map(self):
        draw_quad_2(0, 80, 1360, 765, self.premade_map_texture, self.shader, self.vbo, self.alpha)


    def place_tower(self, x, y):
        
        tile_tower_avail = self.tower_avail.get_tile_tower_avail(x, y)

        tower_already_there = False

        if tile_tower_avail != "X":
            
            self.towers_placed_amount += 1

            if self.towers_on_map != []:
                for tower in self.towers_on_map:
                    tower_location = tower.get_location()
                    if tower_location == (x, y):
                        tower_already_there = True

                if tower_already_there == False:
                    # Name, attack, range, x, y
                    self.towers_on_map.append(Tower(self.tower_selected[1], self.tower_selected[2], self.tower_selected[3], 600, "C_Stickman_", x, y, self.tower_selected[4]))
                    # self.towers_on_map.append(Tower(self.tower_selected[1], self.tower_selected[2], 50, 300, "C_Stickman_", x, y, self.tower_selected[4]))
            else:
                self.towers_on_map.append(Tower(self.tower_selected[1], self.tower_selected[2], self.tower_selected[3], 600, "C_Stickman_", x, y, self.tower_selected[4]))
                # self.towers_on_map.append(Tower(self.tower_selected[1], self.tower_selected[2], 50, 300, "C_Stickman_", x, y, self.tower_selected[4]))
        

    def draw_towers(self):
        all_stickman_img = ["C_Stickman_D.png", "C_Stickman_DL.png", "C_Stickman_DR.png", "C_Stickman_L.png", "C_Stickman_R.png", "C_Stickman_U.png", "C_Stickman_UL.png", "C_Stickman_UR.png"]

        if self.texture_ids_with_quads.get("TOWER") != []:
            for img in all_stickman_img:
                self.texture_ids_with_quads.get("TOWER").get(self.tower_textures.get(img)).clear()

        for tower in self.towers_on_map:
            tower_location = tower.get_location()
            img_ending = tower.get_ending()

            left, top = self.get_rect_param(tower_location[0], tower_location[1])

            self.texture_ids_with_quads.get("TOWER").get(self.tower_textures.get(f'{tower.get_image()}{img_ending}.png')).append((left, top, self.tile_size, self.tile_size))
            # draw_quad(left, top, self.tile_size, self.tile_size, self.tower_textures.get(tower.get_image()))

    def remove_tower(self, x, y):
        if self.towers_on_map != []:
            for tower in self.towers_on_map:
                tower_location = tower.get_location()
                if tower_location == (x, y):
                    self.towers_on_map.remove(tower)

    def move_enemies(self):
        for enemy in self.enemies_on_map:
            if enemy.is_finished() == False:
                enemy.move()

                if enemy.is_alive() == False:
                    self.enemies_on_map.remove(enemy)
            else:
                self.health -= enemy.get_attack()
                self.enemies_on_map.remove(enemy)

    # Why did i have to make a list inside of a dict inside of a dict
    def draw_enemies(self):
        # draw_quad_2(enemy.get_x_pix(), enemy.get_y_pix(), 85, 85, self.enemy_textures.get(enemy.get_img()), self.shader, self.vbo)
        self.texture_ids_with_quads.get("ENEMY").get(self.enemy_textures.get("MagmaBall_HD.png")).clear()
        self.texture_ids_with_quads.get("ENEMY").get(self.enemy_textures.get("FireBall.png")).clear()
        self.texture_ids_with_quads.get("ENEMY").get(self.enemy_textures.get("FireOrb.png")).clear()
        for enemy in self.enemies_on_map:
            left, top = enemy.get_x_pix(), enemy.get_y_pix()
            self.texture_ids_with_quads.get("ENEMY").get(self.enemy_textures.get(enemy.get_img())).append((left, top, self.tile_size, self.tile_size))


    def towers_fire(self):
        if len(self.towers_on_map) > 0 and len(self.enemies_on_map) > 0:

            for tower_on_map in self.towers_on_map:
                now = pygame.time.get_ticks()
                if now - tower_on_map.get_last_attack() > tower_on_map.get_attack_delay():
                    new_bullet = tower_on_map.attack_enemy(self.enemies_on_map, tower_on_map.get_attack_delay() + tower_on_map.get_last_attack(), self.bullets_on_map)
                    if new_bullet != None:
                        self.bullets_on_map.append(new_bullet)


    def draw_bullets(self):
        self.texture_ids_with_quads.get("BULLET").get(self.bullet_textures.get("Balloon.png")).clear()
        for bull in self.bullets_on_map:
            bull_left, bull_top, bull_width, bull_height = bull.get_rect()
            #FIXME:
            self.texture_ids_with_quads.get("BULLET").get(self.bullet_textures.get("Balloon.png")).append((bull_left, bull_top, bull_width, bull_height))
            # self.texture_ids_with_quads.get("BULLET").get(self.bullet_textures.get(bull.get_img())).append((bull_left, bull_top, bull_width, bull_height))

    def move_bullets(self):
        if len(self.bullets_on_map) > 0:
            for bull in self.bullets_on_map:
                if bull.has_hit() == False:
                    bull.move()

                    # bull_left, bull_top, bull_width, bull_height = bull.get_rect()
                    # bull_img = bull.get_img()
                    # draw_quad_2(bull_left, bull_top, bull_width, bull_height, self.enemy_textures.get(bull_img), self.shader, self.vbo)
                else:
                    bull.get_target().set_health(bull.get_damage())
                    self.bullets_on_map.remove(bull)


    def draw_game_end_popup(self):
        # Background
        game_end_left = 592
        game_end_top = 130
        game_end_width = 415
        game_end_height = 540
        draw_quad_2(game_end_left, game_end_top, game_end_width, game_end_height, self.UI_textures.get("T_GameEndBackground.png"), self.shader, self.vbo, 1)

        # Result
        result_left = game_end_left + 115
        result_top = game_end_top + 170
        result_width = 194
        result_height = 85
        draw_quad_2(result_left, result_top, result_width, result_height, self.UI_textures.get(f'T_You{self.result}.png'), self.shader, self.vbo, 1)

        # Retry
        exit_left = game_end_left + 130
        exit_top = game_end_top + game_end_height - 135
        exit_width = 60
        exit_height = 60
        draw_quad_2(exit_left, exit_top, exit_width, exit_height, self.UI_textures.get(f'BTN_Back.png'), self.shader, self.vbo, 1)
        exit_rect = pygame.Rect(exit_left, exit_top, exit_width, exit_height)

        # Exit
        retry_left = game_end_left + 130 + 60 + 40
        draw_quad_2(retry_left, exit_top, exit_width, exit_height, self.UI_textures.get(f'BTN_Retry.png'), self.shader, self.vbo, 1)
        retry_rect = pygame.Rect(retry_left, exit_top, exit_width, exit_height)
        
        self.handle_game_end_buttons(exit_rect, retry_rect)

    def handle_game_end_buttons(self, exit_rect, retry_rect):
        if exit_rect.collidepoint(self.mx, self.my):
            if self.click:
                self.running = False
                self.view_state.set_state("menu")
        if retry_rect.collidepoint(self.mx, self.my):
            if self.click:
                self.running = False
                # Redundant
                self.view_state.set_state("game")


    # Might want to move this to a different file
    def sort_obstacles_from_top_descending(self):
        obstacles = self.map_selected.get_obstacles()
        sorted_obstacles = sorted(obstacles , key=lambda obstacle: obstacle.get_top())
        return sorted_obstacles

    def get_rect_param(self, x, y):
        # LEFT, TOP
        return x * 85, y * 85 + 80
    
    def get_xy_from_cords(self, x, y):
        return int(x / 85), int(y / 85) - 1