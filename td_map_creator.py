import pygame
import os
from func import draw_text
from model.map.map import Map

# Check img

# Tile size 9 x 16
class MapCreator:

    def __init__(self, clock, screen):
        self.clock = clock
        self.screen = screen

        self.running = True
        self.map_selected = None
        self.naming_new_map = False
        self.new_map_name = ""
        self.tile_map = []
        self.load_map_menu = False
        self.click = False
        self.font = pygame.font.SysFont(None, 20)
        self.all_maps = []

        self.td_map_creator_loop()

    def td_map_creator_loop(self):
        counter = 0
        while self.running:
            counter += 1

            self.screen.fill((0,0,0))
            self.all_maps = os.listdir("all_maps")

            self.mx, self.my = pygame.mouse.get_pos()

            # TODO: NOT STATIC
            # TODO: create Grid of all tiles 16x9 (144 buttons ?)
            mapimg = pygame.image.load("images/Scenery2.png")
            mapimg = pygame.transform.scale(mapimg, (1360, 765))
            self.screen.blit(mapimg, (0, 80))

            # Creating the tile map
            tile_map = []
            for y in range(9):
                tile_y = y * 85 + 80
                tile_size = 85
                tile_map.append([])
                for x in range(16):
                    tile_x = x * 85
                    if counter == 1:
                        print(tile_y, tile_x)
                    tile_rect = pygame.Rect(tile_x, tile_y, tile_size, tile_size)
                    tile_map[y].append(tile_rect)


            top_border = pygame.Rect(0, 0, 1600, 30)
            pygame.draw.rect(self.screen, (0, 0, 255), top_border)

            # TODO: Dynamic like loading maps
            seq1 = pygame.Rect(40, 0, 60, 30)
            seq2 = pygame.Rect(105, 0, 60, 30)
            seq3 = pygame.Rect(170, 0, 60, 30)
            seq4 = pygame.Rect(235, 0, 60, 30)
            pygame.draw.rect(self.screen, (122, 0, 0), seq1)
            pygame.draw.rect(self.screen, (122, 0, 0), seq2)
            pygame.draw.rect(self.screen, (122, 0, 0), seq3)
            pygame.draw.rect(self.screen, (122, 0, 0), seq4)
            
            # minimize_top = pygame.Rect(0, 0, 30, 30)
            # pygame.draw.rect(screen, (0, 0, 0), minimize_top)

            # tile_map = pygame.Rect(0, 30, 1360, 870)
            # pygame.draw.rect(screen, (255, 255, 255), tile_map)

            map_creator_ui = pygame.Rect(1360, 30, 240, 900)
            pygame.draw.rect(self.screen, (0, 122, 122), map_creator_ui)

            # minimize_mc_ui = pygame.Rect(1570, 30, 30, 30)
            # pygame.draw.rect(screen, (0, 0, 0), minimize_mc_ui)

            save_button = pygame.Rect(1360, 850, 120, 50)
            exit_button = pygame.Rect(1480, 850, 120, 50)
            pygame.draw.rect(self.screen, (0, 255, 0), save_button)
            pygame.draw.rect(self.screen, (255, 0, 0), exit_button)

            select_map = pygame.Rect(1400, 90, 160, 50)
            pygame.draw.rect(self.screen, (255, 255, 255), select_map)

            see_tiles = pygame.Rect(1400, 190, 160, 50)
            see_tower_avail = pygame.Rect(1400, 260, 160, 50)
            see_sequence = pygame.Rect(1400, 330, 160, 50)
            pygame.draw.rect(self.screen, (255, 255, 255), see_tiles)
            pygame.draw.rect(self.screen, (255, 255, 255), see_tower_avail)
            pygame.draw.rect(self.screen, (255, 255, 255), see_sequence)


            # For now, have to manually add if i add any buttons
            self.handle_buttons(select_map, save_button, exit_button, see_tiles, see_tower_avail, see_sequence, tile_map)


            draw_text("CREATOR", self.font, (255, 255, 255), self.screen, 900, 20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.screen.fill((0, 0, 0))
                
                # Inputs 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.load_map_menu = False

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


    def handle_buttons(self, select_map, save_button, exit_button, see_tiles, see_tower_avail, see_sequence, tile_map):

        # Map menu pop up and its functionality
        # FIXME: MAX 10 MAPS
        if self.load_map_menu == True:
            map_menu_left, map_menu_top, map_menu_width, map_menu_length = self.select_map_menu() 
            self.create_new_map(map_menu_left, map_menu_top, map_menu_width, map_menu_length)     

        # Main Map Creator UI Buttons
        else:
            if select_map.collidepoint(self.mx, self.my):
                if self.click:
                    self.load_map_menu = True

            if save_button.collidepoint(self.mx, self.my):
                if self.click:
                    self.map_selected.save_map()

            if exit_button.collidepoint(self.mx, self.my):
                if self.click:
                    self.running = False
                    self.screen.fill((0,0,0))

            if see_tiles.collidepoint(self.mx, self.my):
                if self.click:
                    # TODO: Change tile visually:
                    pass

            if see_tower_avail.collidepoint(self.mx, self.my):
                if self.click:
                    # TODO: Add or remove the ability to place towers
                    # Clicking tile either adds or removes this 
                    pass

            if see_sequence.collidepoint(self.mx, self.my):
                if self.click:
                    # TODO: Create sequence view
                    # Clicking tile either adds a number if possible, or removes a number if number already exists
                    pass
            

            # For selecting tiles in the map
            for y in range(len(tile_map)):
                for x in range(len(tile_map[y])):
                    if tile_map[y][x].collidepoint(self.mx, self.my):
                        if self.click:
                            print(f'Selected: X = {x}, Y = {y}')

            self.click = False


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
        # FIXME: The lack of Start tile is making the code crash
        for i in range(len(all_maps_rect)):
            map_rect = all_maps_rect[i]

            if map_rect.collidepoint(self.mx, self.my):
                if self.click:
                    self.map_selected = Map(self.all_maps[i], 0, 0)

                    self.map_selected.recreate_map_from_folder()

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
                    self.map_selected = Map(self.new_map_name, 9, 16)
                    self.map_selected.create_map_folder()
                    self.map_selected.initialize_all_maps()

