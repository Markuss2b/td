import pygame
from OpenGL.GL import *
from td_game import td_game_loop
from td_map_creator import MapCreator


class MainMenu:
    def __init__(self):
        self.menu_state = "main_menu"
        self.click = False

        pygame.init()
        self.screen = pygame.display.set_mode((1600, 900), 0, 32)
        self.clock = pygame.time.Clock()

        self.main_loop()

    def main_loop(self):
        font = pygame.font.SysFont(None, 30)
        running = True
        while(running):
            
            mx, my = pygame.mouse.get_pos()
            if self.menu_state == "main_menu":

                play_button = pygame.Rect(50, 100, 100, 50)
                map_creator_button = pygame.Rect(50, 200, 100, 50)
                exit_button = pygame.Rect(50, 300, 100, 50)

                pygame.draw.rect(self.screen, (255, 255, 255), play_button)
                pygame.draw.rect(self.screen, (255, 255, 255), map_creator_button)
                pygame.draw.rect(self.screen, (255, 255, 255), exit_button)


                if play_button.collidepoint(mx, my):
                    if self.click:
                        self.play_game()
                if map_creator_button.collidepoint(mx, my):
                    if self.click:
                        self.map_creator()
                if exit_button.collidepoint(mx, my):
                    if self.click:    
                        self.quit()


            self.click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Inputs 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True

            pygame.display.flip()

            # Frame rate
            self.clock.tick(60)

        self.quit()

    def quit(self):
        pygame.quit()

    def play_game(self):
        td_game_loop(self.clock, self.screen)

    def map_creator(self):
        MapCreator(self.clock, self.screen)
        
