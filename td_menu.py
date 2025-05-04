import pygame
from OpenGL.GL import *
from td_game import TDGame
from td_map_creator import MapCreator
from pygame_functions import draw_checkmark_on_menu, draw_img_on_rect, draw_text
from db_functions import *
from model.profile import Profile


# FIXME: If too many profiles made it will look ugly
class MainMenu:
    def __init__(self):
        self.menu_state = "main_menu"
        self.click = False
        self.load_game = False
        self.load_select_profile = False
        self.load_create_new_profile = False
        self.can_delete_profile = False
        self.mx = 0
        self.my = 0
        self.selected_profile = None
        self.naming_new_profile = False
        self.new_profile_name = ""

        pygame.init()
        self.font = pygame.font.SysFont(None, 30)
        self.screen = pygame.display.set_mode((1600, 900), 0, 32)
        self.clock = pygame.time.Clock()

        self.main_loop()

    def main_loop(self):
        running = True
        while(running):
            
            self.mx, self.my = pygame.mouse.get_pos()
            if self.menu_state == "main_menu":

                if self.load_select_profile == True:
                    # FIXME: Transparent later ?
                    self.screen.fill((0,0,0))
                    self.profile_screen()
                elif self.load_create_new_profile == True:
                    self.screen.fill((0,0,0))
                    self.create_new_profile()
                else:
                    self.screen.fill((0,0,0))

                    if self.selected_profile != None:
                        draw_text(f'Hello {self.selected_profile.get_name()}', self.font, (255,255,255), self.screen, 55, 70)

                    select_profile_button = pygame.Rect(50, 100, 150, 50)
                    play_button = pygame.Rect(50, 200, 150, 50)
                    map_creator_button = pygame.Rect(50, 300, 150, 50)
                    exit_button = pygame.Rect(50, 400, 150, 50)

                    pygame.draw.rect(self.screen, (255, 255, 255), select_profile_button)
                    draw_text(f'Select Profile', self.font, (0,0,0), self.screen, select_profile_button.left + 2, select_profile_button.top + 2)

                    pygame.draw.rect(self.screen, (255, 255, 255), play_button)
                    draw_text(f'Play', self.font, (0,0,0), self.screen, play_button.left + 2, play_button.top + 2)

                    pygame.draw.rect(self.screen, (255, 255, 255), map_creator_button)
                    draw_text(f'Map creator', self.font, (0,0,0), self.screen, map_creator_button.left + 2, map_creator_button.top + 2)

                    pygame.draw.rect(self.screen, (255, 255, 255), exit_button)
                    draw_text(f'Exit', self.font, (0,0,0), self.screen, exit_button.left + 2, exit_button.top + 2)

                    if select_profile_button.collidepoint(self.mx, self.my):
                        if self.click:
                            self.load_select_profile = True
                    if self.selected_profile != None:
                        if play_button.collidepoint(self.mx, self.my):
                            if self.click:
                                self.play_game()
                    if map_creator_button.collidepoint(self.mx, self.my):
                        if self.click:
                            self.map_creator()
                    if exit_button.collidepoint(self.mx, self.my):
                        if self.click:
                            self.quit()


            self.click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Inputs 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.load_create_new_profile == True:
                            self.load_create_new_profile = False
                            self.load_select_profile = True
                        else:
                            self.load_select_profile = False

                    if self.naming_new_profile == True:
                        if event.key == pygame.K_BACKSPACE:
                            self.new_profile_name = self.new_profile_name[:-1]
                        else:
                            if len(self.new_profile_name) < 16:
                                self.new_profile_name += event.unicode
                
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
        TDGame(self.clock, self.screen)

    def map_creator(self):
        MapCreator(self.clock, self.screen)
        
    def profile_screen(self):
        profile_left = 140
        profile_top = 50
        profile_width = 1320
        profile_height = 800
        profile_menu = pygame.Rect(profile_left, profile_top, profile_width, profile_height)
        pygame.draw.rect(self.screen, (40, 40, 40), profile_menu)
        
        checkmark_rect = draw_checkmark_on_menu(self.screen, profile_menu)

        if not profile_menu.collidepoint(self.mx, self.my) or checkmark_rect.collidepoint(self.mx, self.my):
            if self.click:
                self.load_select_profile = False

        create_new_profile_button = pygame.Rect(profile_left + 30, profile_top + profile_height - 60, 150, 40)
        pygame.draw.rect(self.screen, (0, 100, 0), create_new_profile_button)

        enable_disable_delete_profile_button = pygame.Rect(profile_left + profile_width - 150 - 30, profile_top + profile_height - 60, 150, 40)
        pygame.draw.rect(self.screen, (100, 0, 0), enable_disable_delete_profile_button)

        self.handle_profile_buttons(create_new_profile_button, enable_disable_delete_profile_button)

        profile_rects = self.create_profile_rects(profile_left, profile_top)

        self.interact_with_profile_rects(profile_rects)


    def handle_profile_buttons(self, create_new_profile_button, enable_disable_delete_profile_button):
        if create_new_profile_button.collidepoint(self.mx, self.my):
            if self.click:
                self.load_create_new_profile = True
                self.load_select_profile = False

        if enable_disable_delete_profile_button.collidepoint(self.mx, self.my):
            if self.click:
                if self.can_delete_profile == False:
                    self.can_delete_profile = True
                else:
                    self.can_delete_profile = False


    def create_profile_rects(self, profile_left, profile_top):
        all_profiles = get_all_profiles()

        # Creating a rect for each profile created
        base_x = profile_left + 30
        base_y = profile_top + 20

        profile_rects = []

        for i in range(len(all_profiles)):

            id = all_profiles[i][0]
            name = all_profiles[i][1]
            wins = all_profiles[i][2]
            losses = all_profiles[i][3]

            # 4 in a row
            if (i+1) % 5 == 0:
                base_x = profile_left + 30
                base_y += 170

            profile_rect = pygame.Rect(base_x, base_y, 300, 150)
            # Adds a selected button effect
            if self.selected_profile != None:
                if self.selected_profile.get_name() == name:
                    pygame.draw.rect(self.screen, (211, 211, 211), profile_rect)
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), profile_rect)
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), profile_rect)

            x_rect  = pygame.Rect(profile_rect.left + profile_rect.width - 30, profile_rect.top, 30, 30)
            if self.can_delete_profile == True:
                draw_img_on_rect(self.screen, f'images/Assets/X_RED.png', x_rect.left, x_rect.top, x_rect.width, x_rect.height)

            draw_text(name, self.font, (0,0,0), self.screen, base_x + 2, base_y + 2)
            draw_text(f'Wins: {str(wins)}', self.font, (0,0,0), self.screen, base_x + 2, base_y + 20)
            draw_text(f'Losses: {str(losses)}', self.font, (0,0,0), self.screen, base_x + 2, base_y + 40)

            profile_rects.append([profile_rect, x_rect, id])
            
            base_x += 320

        return profile_rects
    

    def interact_with_profile_rects(self, profile_rects):
        # profile_rects = [ [profile_rect, x_rect, id], [...], .... ]
        for i in range(len(profile_rects)):

            # Selects profile
            if profile_rects[i][0].collidepoint(self.mx, self.my) and self.can_delete_profile == False:
                if self.click:
                    db_profile_result = get_profile_with_id(profile_rects[i][2])
                    id = db_profile_result[0]
                    name = db_profile_result[1]
                    wins = db_profile_result[2]
                    losses = db_profile_result[3]

                    self.selected_profile = Profile(id, name, wins, losses)

            # Deletes profile
            if profile_rects[i][1].collidepoint(self.mx, self.my) and self.can_delete_profile == True:
                if self.click:
                    delete_profile_with_id(profile_rects[i][2])
    

    def create_new_profile(self):
        popup_left = 550
        popup_top = 350
        popup_width = 500
        popup_height = 200
        popup = pygame.Rect(popup_left, popup_top, popup_width, popup_height)
        pygame.draw.rect(self.screen, (40, 40, 40), popup)

        # Inputfield for creating new profile
        new_profile_inputfield = pygame.Rect(popup_left + 30, popup_top + 50, popup_width - 60, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), new_profile_inputfield)

        if self.naming_new_profile == False:
            draw_text("Enter name", pygame.font.SysFont(None, 40), (100, 100, 100), self.screen, new_profile_inputfield.left + 5, new_profile_inputfield.top + 13)
        else:
            draw_text(self.new_profile_name, pygame.font.SysFont(None, 50), (0, 0, 0), self.screen, new_profile_inputfield.left, new_profile_inputfield.top + 10)

        checkmark_rect = draw_checkmark_on_menu(self.screen, popup)

        # Activating input field
        if new_profile_inputfield.collidepoint(self.mx, self.my):
            if self.click:
                self.naming_new_profile = True
                self.new_profile_name = ""

        # Creates new profile
        # TODO: Can create new profile with enter
        elif checkmark_rect.collidepoint(self.mx, self.my):
            if self.click:
                create_profile(self.new_profile_name)

                created_profile = get_profile_with_name(self.new_profile_name)
                id = created_profile[0]
                name = created_profile[1]
                wins = created_profile[2]
                losses = created_profile[3]

                self.selected_profile = Profile(id, name, wins, losses)

                self.load_create_new_profile = False
                self.load_select_profile = True
                self.new_profile_name = "" 

        elif self.click:
            self.naming_new_profile = False
            self.new_profile_name = "" 