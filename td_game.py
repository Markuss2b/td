import pygame
from func import draw_text

def td_game_loop(clock, screen):
    click = False
    font = pygame.font.SysFont(None, 20)
    
    running = True
    while running:
        screen.fill((0,0,0))
        
        top_border = pygame.Rect(0, 0, 1600, 40)
        pygame.draw.rect(screen, (122, 0, 0), top_border)

        tile_map = pygame.Rect(0, 40, 1360, 900)
        pygame.draw.rect(screen, (255, 255, 255), tile_map)

        tower_selector = pygame.Rect(1360, 40, 240, 900)
        pygame.draw.rect(screen, (0, 122, 122), tower_selector)

        draw_text("GAME", font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                screen.fill((0,0,0))
            
            # Inputs 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    screen.fill((0,0,0))
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.flip()

        # Frame rate
        clock.tick(60)

