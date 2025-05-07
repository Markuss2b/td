import pygame
import os
import time
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame_functions import draw_text
from db_functions import get_tower_with_name
from pyopengl_functions import load_texture, draw_quad, unload_texture, draw_quads, create_shader, draw_quad_2, draw_quads_2, destroy
from model.map.map import Map
from model.map.premade_map import PremadeMap
from model.tower import Tower

class TDGame:
    def __init__(self, clock, screen, selected_profile, map_selected):
        self.clock = clock

        self.display_size = (1600, 900)
        # TODO: If i change main menu to opengl swap this to previous screen
        self.screen = pygame.display.set_mode(self.display_size, pygame.OPENGL|pygame.DOUBLEBUF)


        self.selected_profile = selected_profile
        self.map_selected = map_selected
        self.tower_avail = self.map_selected.get_tower_availability_map()

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
        # Other textures

        self.static_tile = False
        self.static_obstacles = False
        self.static_UI = False


        self.texture_ids_with_quads = {}

        self.premade_map_texture = None

        self.tower_selected = None

        #TODO:
        self.only_tower = get_tower_with_name("Magma Ball")

        self.towers_on_map = []

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(2 * 4))

        self.shader = create_shader()
        glUseProgram(self.shader)

        self.td_game_loop()

    def td_game_loop(self):
 
        # Load all textures

        if self.map_selected.get_map_type() == "Map":
            self.load_tile_textures()
            self.load_obstacle_textures()
        elif self.map_selected.get_map_type() == "PremadeMap":
            self.load_premade_map_textures()

        # Always load
        self.load_tower_textures()
        self.load_enemy_textures()
        self.load_UI_textures()

        self.group_textures_2()
        print(self.texture_ids_with_quads)


        running = True
        while running:
            self.mx, self.my = pygame.mouse.get_pos()
            self.click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

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
                
                # Inputs 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True


            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            if self.map_selected.get_map_type() == "Map":
                self.draw_map()
                self.draw_obstacles()
            elif self.map_selected.get_map_type() == "PremadeMap":
                self.draw_premade_map()

            # Always draw
            select_magma_rect = self.draw_UI()
            self.handle_UI_buttons(select_magma_rect)
            self.draw_towers()

            start = time.time()
            draw_quads_2(self.texture_ids_with_quads, self.shader, self.vbo)
            end = time.time()
            print(f'Time: {start-end}')

            if self.tower_selected != None:
                if self.click:
                    x, y = self.get_xy_from_cords(self.mx, self.my)

                    if x >= 0 and x <= 15 and y >= 0 and y <= 8:
                        self.place_tower(x, y)

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

    def load_UI_textures(self):
        self.UI_textures["UI_SidePanel.png"] = load_texture(f'images/UI/MapCreator/UI_SidePanel.png') 

    def load_premade_map_textures(self):
        self.premade_map_texture = load_texture(f'predrawn_maps/{self.map_selected.get_map_name()}/map_image.png')


    def group_textures(self):
        all_textures = self.tile_textures | self.enemy_textures | self.UI_textures | self.tower_textures | self.assets_textures | self.obstacle_textures 
        self.texture_ids_with_quads = { all_textures.get(k):[] for k in all_textures }

    
    def group_textures_2(self):
        self.texture_ids_with_quads["UI"] = { self.UI_textures.get(k):[] for k in self.UI_textures }
        self.texture_ids_with_quads["TILE"] = { self.tile_textures.get(k):[] for k in self.tile_textures }
        self.texture_ids_with_quads["OBSTACLES"] = { self.obstacle_textures.get(k):[] for k in self.obstacle_textures }
        self.texture_ids_with_quads["TOWER"] = { self.tower_textures.get(k):[] for k in self.tower_textures }
        self.texture_ids_with_quads["ENEMY"] = { self.enemy_textures.get(k):[] for k in self.enemy_textures }
        self.texture_ids_with_quads["ASSETS"] = { self.assets_textures.get(k):[] for k in self.assets_textures }

    
    def draw_UI(self):
        draw_quad_2(1360, 30, 240, 870, self.UI_textures.get("UI_SidePanel.png"), self.shader, self.vbo)

        select_magma_rect = pygame.Rect(1435, 60, 85, 85)
        draw_quad_2(select_magma_rect.left, select_magma_rect.top, select_magma_rect.width, select_magma_rect.height, self.enemy_textures.get("MagmaBall.png"), self.shader, self.vbo)

        return select_magma_rect
    

    def handle_UI_buttons(self, select_magma_rect):
        if select_magma_rect.collidepoint(self.mx, self.my):
            if self.click:

                # TODO: towers
                self.tower_selected = self.only_tower


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


    def draw_premade_map(self):
        draw_quad_2(0, 80, 1360, 765, self.premade_map_texture, self.shader, self.vbo)


    def place_tower(self, x, y):
        
        tile_tower_avail = self.tower_avail.get_tile_tower_avail(x, y)

        tower_already_there = False

        if tile_tower_avail != "X":
            
            if self.towers_on_map != []:
                for tower in self.towers_on_map:
                    tower_location = tower.get_location()
                    if tower_location == (x, y):
                        tower_already_there = True

                if tower_already_there == False:
                    # Name, attack, range, x, y
                    self.towers_on_map.append(Tower(self.tower_selected[1], self.tower_selected[2], self.tower_selected[3], x, y, self.tower_selected[4]))
            else:
                self.towers_on_map.append(Tower(self.tower_selected[1], self.tower_selected[2], self.tower_selected[3], x, y, self.tower_selected[4]))
        


    def draw_towers(self):
        clear_list = False
        for tower in self.towers_on_map:
            if clear_list == False:
                self.texture_ids_with_quads.get("TOWER").get(self.tower_textures.get(tower.get_image())).clear()
                clear_list = True

            tower_location = tower.get_location()
            left, top = self.get_rect_param(tower_location[0], tower_location[1])

            self.texture_ids_with_quads.get("TOWER").get(self.tower_textures.get(tower.get_image())).append((left, top, self.tile_size, self.tile_size))
            # draw_quad(left, top, self.tile_size, self.tile_size, self.tower_textures.get(tower.get_image()))

    def remove_tower():
        pass



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