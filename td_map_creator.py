import pygame
from func import draw_text

# Check img

# Tile size 9 x 16

def td_map_creator_loop(clock, screen):
    click = False
    font = pygame.font.SysFont(None, 20)
    
    running = True
    while running:
        screen.fill((0,0,0))

        mapimg = pygame.image.load("images/Scenery2.png")
        mapimg = pygame.transform.scale(mapimg, (1360, 870))
        screen.blit(mapimg, (0, 30))

        top_border = pygame.Rect(0, 0, 1600, 30)
        pygame.draw.rect(screen, (0, 0, 255), top_border)

        seq1 = pygame.Rect(40, 0, 60, 30)
        seq2 = pygame.Rect(105, 0, 60, 30)
        seq3 = pygame.Rect(170, 0, 60, 30)
        seq4 = pygame.Rect(235, 0, 60, 30)
        pygame.draw.rect(screen, (122, 0, 0), seq1)
        pygame.draw.rect(screen, (122, 0, 0), seq2)
        pygame.draw.rect(screen, (122, 0, 0), seq3)
        pygame.draw.rect(screen, (122, 0, 0), seq4)

        # minimize_top = pygame.Rect(0, 0, 30, 30)
        # pygame.draw.rect(screen, (0, 0, 0), minimize_top)

        # tile_map = pygame.Rect(0, 30, 1360, 870)
        # pygame.draw.rect(screen, (255, 255, 255), tile_map)

        map_creator_ui = pygame.Rect(1360, 30, 240, 900)
        pygame.draw.rect(screen, (0, 122, 122), map_creator_ui)

        # minimize_mc_ui = pygame.Rect(1570, 30, 30, 30)
        # pygame.draw.rect(screen, (0, 0, 0), minimize_mc_ui)

        save_button = pygame.Rect(1360, 850, 120, 50)
        exit_button = pygame.Rect(1480, 850, 120, 50)
        pygame.draw.rect(screen, (0, 255, 0), save_button)
        pygame.draw.rect(screen, (255, 0, 0), exit_button)

        select_map = pygame.Rect(1400, 90, 160, 50)
        pygame.draw.rect(screen, (255, 255, 255), select_map)

        see_tiles = pygame.Rect(1400, 190, 160, 50)
        see_tower_avail = pygame.Rect(1400, 260, 160, 50)
        see_sequence = pygame.Rect(1400, 330, 160, 50)
        pygame.draw.rect(screen, (255, 255, 255), see_tiles)
        pygame.draw.rect(screen, (255, 255, 255), see_tower_avail)
        pygame.draw.rect(screen, (255, 255, 255), see_sequence)


        draw_text("CREATOR", font, (255, 255, 255), screen, 900, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
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