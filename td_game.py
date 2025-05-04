import pygame
import os
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame_functions import draw_text
from pyopengl_functions import load_texture, draw_quad, unload_texture
from model.map.map import Map
from model.map.premade_map import PremadeMap

class TDGame:
    def __init__(self, clock, screen, selected_profile, map_selected):
        self.clock = clock

        self.display_size = (1600, 900)
        # TODO: If i change main menu to opengl swap this to previous screen
        self.screen = pygame.display.set_mode(self.display_size, pygame.OPENGL|pygame.DOUBLEBUF)


        self.selected_profile = selected_profile
        self.map_selected = map_selected

        self.click = False
        self.tile_size = 85

        self.tile_textures = {}
        self.obstacle_textures = {}
        self.tower_textures = {}
        self.enemy_textures = {}
        self.assets_textures = {}
        self.UI_textures = {}
        self.premade_map_texture = None

        # Other textures

        self.td_game_loop()

    def td_game_loop(self):

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.display_size[0], self.display_size[1], 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
 
        # Load all textures

        if self.map_selected.get_map_type() == "Map":
            self.load_tile_textures()
            self.load_obstacle_textures()
        elif self.map_selected.get_map_type() == "PremadeMap":
            self.load_premade_map_textures()

        # Always load
        self.load_UI_textures()


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
            self.draw_UI()

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

    
    def draw_UI(self):
        draw_quad(1360, 30, 240, 870, self.UI_textures.get("UI_SidePanel.png"))


    def draw_map(self):
        visual_tile = self.map_selected.get_visual_map()
        visual_tile_map = visual_tile.get_visual_tile_map()

        for y in range(len(visual_tile_map)):
            for x in range(len(visual_tile_map[y])):

                tile_x, tile_y = self.get_rect_param(x, y)
                tile = visual_tile.get_tile_type(x, y)

                if tile != None:
                    draw_quad(tile_x, tile_y, self.tile_size, self.tile_size, self.tile_textures.get(tile))


    def draw_obstacles(self):
        obstacles = self.sort_obstacles_from_top_descending()
        for obstacle in obstacles:
            draw_quad(obstacle.get_left(), obstacle.get_top(), obstacle.get_width(), obstacle.get_height(), self.obstacle_textures.get(obstacle.get_name()))


    def draw_premade_map(self):
        draw_quad(0, 80, 1360, 765, self.premade_map_texture)




    # Might want to move this to a different file
    def sort_obstacles_from_top_descending(self):
        obstacles = self.map_selected.get_obstacles()
        sorted_obstacles = sorted(obstacles , key=lambda obstacle: obstacle.get_top())
        return sorted_obstacles

    def get_rect_param(self, x, y):
        # LEFT, TOP
        return x * 85, y * 85 + 80