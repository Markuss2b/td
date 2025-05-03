import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame_functions import draw_text
from pyopengl_functions import load_texture, draw_quad

class TDGame:
    def __init__(self, clock, screen, click):
        self.clock = clock

        self.display_size = (1600, 900)
        # TODO: If i change main menu to opengl swap this to previous screen
        self.screen = pygame.display.set_mode(self.display_size, pygame.OPENGL|pygame.DOUBLEBUF)

        self.click = click

        self.td_game_loop()

    def td_game_loop(self):

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.display_size[0], self.display_size[1], 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
 
        textID = load_texture("")

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
            draw_quad(0, 0, 500, 500, textID)
            pygame.display.flip()

            # Frame rate
            self.clock.tick(60)
        


