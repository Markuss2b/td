import pygame
import os
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame_functions import draw_text
from pyopengl_functions import load_texture, draw_quad, unload_texture

class TDGame:
    def __init__(self, clock, screen):
        self.clock = clock

        self.display_size = (1600, 900)
        # TODO: If i change main menu to opengl swap this to previous screen
        self.screen = pygame.display.set_mode(self.display_size, pygame.OPENGL|pygame.DOUBLEBUF)

        self.click = False

        self.tile_textures = {}
        self.obstacle_textures = {}
        self.tower_textures = {}
        self.enemy_textures = {}

        # Other textures

        self.td_game_loop()

    def td_game_loop(self):

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.display_size[0], self.display_size[1], 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
 
        #textID = load_texture("")
        self.load_tile_textures()
        self.load_obstacle_textures()
        print(self.tile_textures)
        print(self.obstacle_textures)

        running = True
        while running:
            self.mx, self.my = pygame.mouse.get_pos()
            
            top_border = pygame.Rect(0, 0, 1600, 40)
            tile_map = pygame.Rect(0, 40, 1360, 900)
            tower_selector = pygame.Rect(1360, 40, 240, 900)

            self.click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                    # Unload textures when code stops running
                    for texture_id in self.tile_textures.values():
                        unload_texture(texture_id)

                    for texture_id in self.obstacle_textures.values():
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
            #draw_quad(0, 0, 500, 500, textID)
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
        pass

    def load_tower_textures(self):
        pass

