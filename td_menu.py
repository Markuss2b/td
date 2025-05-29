import pygame
import os
import re
from OpenGL.GL import *
from td_game import TDGame
from td_map_creator import MapCreator
from pygame_functions import draw_checkmark_on_menu, draw_img_on_rect, draw_text
from db_functions import *
from model.profile import Profile
from model.map.map import Map
from model.map.premade_map import PremadeMap


class MainMenu:
    def __init__(self, view_state):
        self.view_state = view_state
        self.menu_state = "main_menu"
        self.click = False
        self.load_game = False
        self.load_select_profile = False
        self.load_create_new_profile = False
        self.load_history = False

        self.load_edit_enemies = False
        self.load_enemy = False
        self.enemy_selected = None
        self.new_enemy_health = ""
        self.editing_enemy_health = False
        self.new_enemy_speed = ""
        self.editing_enemy_speed = False
        self.new_enemy_attack = ""
        self.editing_enemy_attack = False

        self.can_delete_profile = False
        self.load_select_map = False
        self.load_custom_map = False
        self.load_premade_map = False
        self.mx = 0
        self.my = 0
        self.selected_profile = self.view_state.get_selected_profile()
        self.map_selected = None
        self.selected_premade_map = None
        self.naming_new_profile = False
        self.new_profile_name = ""
        self.error_msg = ""
        self.running = True
        self.history_page = 1

        pygame.init()
        self.font = pygame.font.SysFont(None, 30)
        self.screen = pygame.display.set_mode((1600, 900), 0, 32)
        self.clock = pygame.time.Clock()

        self.main_loop()

    def main_loop(self):
        while self.running:
            self.mx, self.my = pygame.mouse.get_pos()
            if self.menu_state == "main_menu":

                if self.load_select_profile == True:
                    self.screen.fill((0,0,0))
                    self.profile_screen()
                elif self.load_create_new_profile == True:
                    self.screen.fill((0,0,0))
                    self.create_new_profile()
                elif self.load_select_map == True:
                    self.screen.fill((0,0,0))
                    draw_img_on_rect(self.screen, "images/MainMenu.png", 0, 0, 1600, 900)
                    self.select_map_menu()
                elif self.load_custom_map == True:
                    self.screen.fill((0,0,0))
                    draw_img_on_rect(self.screen, "images/MainMenu.png", 0, 0, 1600, 900)
                    self.select_custom_made_maps()
                elif self.load_premade_map == True:
                    self.screen.fill((0,0,0))
                    draw_img_on_rect(self.screen, "images/MainMenu.png", 0, 0, 1600, 900)
                    self.select_premade_maps()
                elif self.load_history == True:
                    self.screen.fill((0,0,0))
                    draw_img_on_rect(self.screen, "images/MainMenu.png", 0, 0, 1600, 900)
                    self.history()
                elif self.load_edit_enemies == True:
                    self.screen.fill((0,0,0))
                    draw_img_on_rect(self.screen, "images/MainMenu.png", 0, 0, 1600, 900)
                    self.edit_enemies()
                elif self.load_enemy == True:
                    self.screen.fill((0,0,0))
                    draw_img_on_rect(self.screen, "images/MainMenu.png", 0, 0, 1600, 900)
                    self.edit_enemy()
                else:
                    self.screen.fill((0,0,0))
                    draw_img_on_rect(self.screen, "images/MainMenu.png", 0, 0, 1600, 900)

                    if self.selected_profile != None:
                        draw_text(f'Hello {self.selected_profile.get_name()}', self.font, (255,255,255), self.screen, 80, 70)

                    select_profile_button = pygame.Rect(75, 100, 160, 55)
                    play_button = pygame.Rect(75, 205, 160, 55)
                    map_creator_button = pygame.Rect(75, 305, 160, 55)
                    history_button = pygame.Rect(75, 405, 160, 55)
                    enemies_button = pygame.Rect(75, 505, 160, 55)
                    exit_button = pygame.Rect(75, 605, 160, 55)

                    draw_img_on_rect(self.screen, "images/UI/MainMenu/BTN_SelectProfile.png", select_profile_button.left, select_profile_button.top, select_profile_button.width, select_profile_button.height)
                    # pygame.draw.rect(self.screen, (255, 255, 255), select_profile_button)
                    # draw_text(f'Select Profile', self.font, (0,0,0), self.screen, select_profile_button.left + 2, select_profile_button.top + 2)

                    draw_img_on_rect(self.screen, "images/UI/MainMenu/BTN_Play.png", play_button.left, play_button.top, play_button.width, play_button.height)
                    # pygame.draw.rect(self.screen, (255, 255, 255), play_button)
                    # draw_text(f'Play', self.font, (0,0,0), self.screen, play_button.left + 2, play_button.top + 2)

                    draw_img_on_rect(self.screen, "images/UI/MainMenu/BTN_MapCreator.png", map_creator_button.left, map_creator_button.top, map_creator_button.width, map_creator_button.height)
                    # pygame.draw.rect(self.screen, (255, 255, 255), map_creator_button)
                    # draw_text(f'Map creator', self.font, (0,0,0), self.screen, map_creator_button.left + 2, map_creator_button.top + 2)

                    draw_img_on_rect(self.screen, "images/UI/MainMenu/BTN_History.png", history_button.left, history_button.top, history_button.width, history_button.height)
                    # pygame.draw.rect(self.screen, (255, 255, 255), history_button)
                    # draw_text(f'History', self.font, (0,0,0), self.screen, history_button.left + 2, history_button.top + 2)

                    draw_img_on_rect(self.screen, "images/UI/MainMenu/BTN_Enemies.png", enemies_button.left, enemies_button.top, enemies_button.width, enemies_button.height)
                    # pygame.draw.rect(self.screen, (255, 255, 255), enemies_button)
                    # draw_text(f'Enemies', self.font, (0,0,0), self.screen, enemies_button.left + 2, enemies_button.top + 2)

                    draw_img_on_rect(self.screen, "images/UI/MainMenu/BTN_Exit.png", exit_button.left, exit_button.top, exit_button.width, exit_button.height)
                    # pygame.draw.rect(self.screen, (255, 255, 255), exit_button)
                    # draw_text(f'Exit', self.font, (0,0,0), self.screen, exit_button.left + 2, exit_button.top + 2)

                    if select_profile_button.collidepoint(self.mx, self.my):
                        if self.click:
                            self.load_select_profile = True
                    if self.selected_profile != None:
                        if play_button.collidepoint(self.mx, self.my):
                            if self.click:
                                self.load_select_map = True
                        if history_button.collidepoint(self.mx, self.my):
                            if self.click:
                                self.load_history = True
                    if map_creator_button.collidepoint(self.mx, self.my):
                        if self.click:
                            self.map_creator()
                    if enemies_button.collidepoint(self.mx, self.my):
                        if self.click:
                            self.load_edit_enemies = True
                    if exit_button.collidepoint(self.mx, self.my):
                        if self.click:
                            self.quit()
                            self.view_state.set_quit(True)


            self.click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.view_state.set_quit(True)
                
                # Inputs 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.load_history = False
                        self.can_delete_profile = False

                        if self.load_create_new_profile == True:
                            self.load_create_new_profile = False
                            self.load_select_profile = True
                        else:
                            self.load_select_profile = False

                        if self.load_select_map == True:
                            self.load_select_map = False
                        elif self.load_custom_map == True or self.load_premade_map == True:
                            self.load_select_map = True
                            self.load_custom_map = False
                            self.load_premade_map = False
                        self.error_msg = ""

                        if self.load_enemy == True:
                            self.load_edit_enemies = True
                            self.load_enemy = False
                        elif self.load_edit_enemies == True:
                            self.load_edit_enemies = False

                    # Spaghetti
                    if self.naming_new_profile == True:
                        if event.key == pygame.K_BACKSPACE:
                            self.new_profile_name = self.new_profile_name[:-1]
                        else:
                            if len(self.new_profile_name) < 16:
                                self.new_profile_name += event.unicode

                    if self.editing_enemy_health == True:
                        if event.key == pygame.K_BACKSPACE:
                            self.new_enemy_health = self.new_enemy_health[:-1]
                        else:
                            if len(self.new_enemy_health) < 16:
                                self.new_enemy_health += event.unicode
                
                    # if self.editing_enemy_speed == True:
                    #     if event.key == pygame.K_BACKSPACE:
                    #         self.new_enemy_speed = self.new_enemy_speed[:-1]
                    #     else:
                    #         if len(self.new_enemy_speed) < 16:
                    #             self.new_enemy_speed += event.unicode

                    if self.editing_enemy_attack == True:
                        if event.key == pygame.K_BACKSPACE:
                            self.new_enemy_attack = self.new_enemy_attack[:-1]
                        else:
                            if len(self.new_enemy_attack) < 16:
                                self.new_enemy_attack += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True

            pygame.display.flip()

            # Frame rate
            self.clock.tick(60)

        self.quit()

    def quit(self):
        pygame.quit()

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

                # Remove this = Big problem
                self.can_delete_profile = False

        if enable_disable_delete_profile_button.collidepoint(self.mx, self.my):
            if self.click:
                if self.can_delete_profile == False:
                    self.can_delete_profile = True
                    self.selected_profile = None
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

            # 4 in a row
            if (i+1) % 4 == 0:
                base_x = profile_left + 30
                base_y += 170

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
                    self.view_state.set_selected_profile(self.selected_profile)

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

        draw_text(self.error_msg, pygame.font.SysFont(None, 40), (255, 50, 50), self.screen, popup_left, popup_top + popup_height + 5)

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

                all_profile_names = [profile[1].upper() for profile in get_all_profiles()]

                if not self.new_profile_name.upper() in all_profile_names and len(all_profile_names) < 16 and re.match(r'^[A-Za-z0-9]+$', self.new_profile_name):

                    # Might stop SQL injection
                    # Or might stop error
                    self.new_profile_name = self.new_profile_name.replace("'", "")
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
                    self.error_msg = ""
                elif self.new_profile_name.upper() in all_profile_names:
                    self.error_msg = "Name taken"
                elif len(all_profile_names) >= 16:
                    self.error_msg = "No free slots"
                elif not re.match(r'^[A-Za-z0-9]+$', self.new_profile_name):
                    self.error_msg = "Invalid symbols"

        elif self.click:
            self.naming_new_profile = False
            self.new_profile_name = "" 


    def select_map_menu(self):
        select_map_left = 420
        select_map_top = 250
        select_map_width = 760
        select_map_height = 400
        select_map_menu = pygame.Rect(select_map_left, select_map_top, select_map_width, select_map_height)
        draw_img_on_rect(self.screen, "images/UI/MainMenu/SelectMap/Border.png", select_map_menu.left, select_map_menu.top, select_map_menu.width, select_map_menu.height)

        premade_map_rect = pygame.Rect(select_map_left + 40, select_map_top + 110, 320, 180)
        custom_map_rect = pygame.Rect(select_map_left + 40 + premade_map_rect.width + 40, select_map_top + 110, 320, 180)

        draw_img_on_rect(self.screen, "images/UI/MainMenu/SelectMap/BTN_PremadeMap.png", premade_map_rect.left, premade_map_rect.top, premade_map_rect.width, premade_map_rect.height)
        draw_img_on_rect(self.screen, "images/UI/MainMenu/SelectMap/BTN_CustomMap.png", custom_map_rect.left, custom_map_rect.top, custom_map_rect.width, custom_map_rect.height)

        if self.check_for_saved_games() == True:
            saved_map_rect = pygame.Rect(select_map_left + select_map_width / 2 - 145, select_map_top + select_map_height - 90, 290, 50)
            draw_img_on_rect(self.screen, "images/UI/MainMenu/SelectMap/BTN_Continue.png", saved_map_rect.left, saved_map_rect.top, saved_map_rect.width, saved_map_rect.height)

            if saved_map_rect.collidepoint(self.mx, self.my):
                if self.click:
                    save_path = f'saved_games/{self.selected_profile.get_name()}.txt'
                    with open(save_path, "r") as f:
                        map_name = f.readline().replace("\n", "")
                        wave = int(f.readline().replace("\n", ""))
                        health = int(f.readline().replace("\n", ""))
                        towers = f.readlines()
                    
                    if map_name == "farmfield" or map_name == "farmfield2" or map_name == "pond":
                        self.map_selected = PremadeMap(map_name, 16, 9)
                        self.map_selected.recreate_map_from_folder()
                    else:
                        self.map_selected = Map(map_name, 0, 0)
                        self.map_selected.recreate_map_from_folder()

                    self.view_state.set_map_selected(self.map_selected)
                    self.view_state.set_saved_game([]) # reset
                    self.view_state.get_saved_game().append(wave)
                    self.view_state.get_saved_game().append(health)
                    self.view_state.get_saved_game().append(towers)
                    self.view_state.set_state("game")
                    os.remove(f'saved_games/{self.selected_profile.get_name()}.txt')
                    self.running = False

        if premade_map_rect.collidepoint(self.mx, self.my):
            if self.click:
                self.load_premade_map = True
                self.load_select_map = False
        elif custom_map_rect.collidepoint(self.mx, self.my):
            if self.click:
                self.load_custom_map = True
                self.load_select_map = False

    def select_premade_maps(self):
        map_menu_left = 420
        map_menu_top = 150
        map_menu_width = 760
        map_menu_height = 600
        map_menu = pygame.Rect(map_menu_left, map_menu_top, map_menu_width, map_menu_height)
        draw_img_on_rect(self.screen, "images/UI/MainMenu/SelectMap/Border.png", map_menu.left, map_menu.top, map_menu.width, map_menu.height)
        # pygame.draw.rect(self.screen, (40, 40, 40), map_menu)

        farmfield = pygame.Rect(map_menu_left + 40, map_menu_top + 80, 320, 180)
        draw_img_on_rect(self.screen, "images/PremadeMaps/Scenery2.png", farmfield.left, farmfield.top, farmfield.width, farmfield.height)

        farmfield2 = pygame.Rect(map_menu_left + 40 + farmfield.width + 40, map_menu_top + 80, 320, 180)
        draw_img_on_rect(self.screen, "images/PremadeMaps/Map_HayField.png", farmfield2.left, farmfield2.top, farmfield2.width, farmfield2.height)

        pond = pygame.Rect(map_menu_left + 40, map_menu_top + 80 + 180 + 40, 320, 180)
        draw_img_on_rect(self.screen, "images/PremadeMaps/Map_Pond.png", pond.left, pond.top, pond.width, pond.height)
                
        temp2 = pygame.Rect(map_menu_left + 40 + farmfield.width + 40, map_menu_top + 80 + 180 + 40, 320, 180)
        pygame.draw.rect(self.screen, (175, 175, 175), temp2)

        premade_map_rects = [[farmfield, "farmfield"], [farmfield2, "farmfield2"], [pond, "pond"], [temp2, "3"]]
                             
        for map_rect in premade_map_rects:
            if map_rect[0].collidepoint(self.mx, self.my):
                if self.click:
                    self.selected_premade_map = map_rect[1]

            if map_rect[1] == self.selected_premade_map:
                draw_img_on_rect(self.screen, "images/Assets/select.png", map_rect[0].left, map_rect[0].top, map_rect[0].width, map_rect[0].height)

        checkmark_rect = draw_checkmark_on_menu(self.screen, map_menu)

        if self.selected_premade_map == "farmfield" or self.selected_premade_map == "farmfield2" or self.selected_premade_map == "pond":
            if checkmark_rect.collidepoint(self.mx, self.my):
                if self.click:
                    self.map_selected = PremadeMap(self.selected_premade_map, 16, 9)
                    self.map_selected.recreate_map_from_folder()
                    self.view_state.set_map_selected(self.map_selected)

                    self.view_state.set_state("game")
                    self.running = False
                    # TDGame(self.clock, self.screen, self.selected_profile, self.map_selected)


    def select_custom_made_maps(self):
        custom_maps = os.listdir("all_maps")

        for temp_map_name in custom_maps:
            temp_map = Map(temp_map_name, 16, 9)
            temp_map.recreate_map_from_folder()

            for temp_path in temp_map.get_all_paths():
                if len(temp_path.get_sequence()) <= 1:
                    custom_maps.remove(temp_map_name)
                    break

        map_menu_left = 650
        map_menu_top = 100
        map_menu_width = 300
        map_menu_height = 720
        map_menu = pygame.Rect(map_menu_left, map_menu_top, map_menu_width, map_menu_height)
        pygame.draw.rect(self.screen, (75, 75, 75), map_menu)

        base_x = map_menu_left + 20
        base_y = map_menu_top + 10

        # Creates a rect for every map
        all_maps_rect = []
        for i in range(len(custom_maps)):
            map_rect = pygame.Rect(base_x, base_y + 40 * (i + 1), 260, 30)
            
            # Adds a selected button effect
            if self.map_selected != None:
                if self.map_selected.get_map_name() == custom_maps[i]:
                    pygame.draw.rect(self.screen, (160, 160, 160), map_rect)
                    draw_img_on_rect(self.screen, "images/Assets/Grid1.png", map_rect.left, map_rect.top, map_rect.width, map_rect.height)
                else:
                    pygame.draw.rect(self.screen, (125, 125, 125), map_rect)
            else:
                pygame.draw.rect(self.screen, (125, 125, 125), map_rect)

            draw_text(custom_maps[i], pygame.font.SysFont(None, 30), (255, 255, 255), self.screen, map_rect.left + 5, map_rect.top + 5)
            
            all_maps_rect.append(map_rect)

        # Selects any previously made maps
        for i in range(len(all_maps_rect)):
            map_rect = all_maps_rect[i]

            # Recreates map
            if map_rect.collidepoint(self.mx, self.my):
                if self.click:
                    self.map_selected = Map(custom_maps[i], 0, 0)
                    self.map_selected.recreate_map_from_folder()

        checkmark_rect = draw_checkmark_on_menu(self.screen, map_menu)
        

        if self.map_selected != None:
            if checkmark_rect.collidepoint(self.mx, self.my):
                if self.click:
                    self.view_state.set_map_selected(self.map_selected)
                    self.view_state.set_state("game")
                    self.running = False


    def check_for_saved_games(self):
        saved_game_files = os.listdir("saved_games")
        for game_file in saved_game_files:
            if game_file == f'{self.selected_profile.get_name()}.txt':
                return True
        return False
    
    
    def history(self):
        history_left = 300
        history_top = 150
        history_width = 1000
        history_height = 550
        history_rect = pygame.Rect(history_left, history_top, history_width, history_height)
        draw_img_on_rect(self.screen, "images/UI/MainMenu/SelectMap/Border.png", history_rect.left, history_rect.top, history_rect.width, history_rect.height)
        # pygame.draw.rect(self.screen, (40, 40, 40), history_rect)

        checkmark_rect = draw_checkmark_on_menu(self.screen, history_rect)

        if not history_rect.collidepoint(self.mx, self.my) or checkmark_rect.collidepoint(self.mx, self.my):
            if self.click:
                self.load_history = False

        profile = get_profile_with_name(self.selected_profile.get_name())
        profile_id = profile[0]

        draw_text(self.selected_profile.get_name(), pygame.font.SysFont(None, 45), (255,255,255), self.screen, history_left + 30, history_top + 15)

        draw_text("Game", pygame.font.SysFont(None, 30), (255,255,255), self.screen, history_left + 60, history_top + 60)
        draw_text("Map", pygame.font.SysFont(None, 30), (255,255,255), self.screen, history_left + 130 + 90, history_top + 60)
        draw_text("Result", pygame.font.SysFont(None, 30), (255,255,255), self.screen, history_left + 260 + 120, history_top + 60)
        draw_text("Wave", pygame.font.SysFont(None, 30), (255,255,255), self.screen, history_left + 390 + 150, history_top + 60)
        draw_text("Towers", pygame.font.SysFont(None, 30), (255,255,255), self.screen, history_left + 520 + 180, history_top + 60)
        draw_text("Time", pygame.font.SysFont(None, 30), (255,255,255), self.screen, history_left + 650 + 210, history_top + 60)

        all_games = get_history_with_id(profile_id)
        if all_games != None:
            base_y = history_top + 50

            for i in range(len(all_games)):
                if i+1 > self.history_page * 7:
                    break
                elif i+1 > (self.history_page - 1) * 7:
                    game = all_games[i]
                    draw_text(str(i+1), pygame.font.SysFont(None, 30), (255,255,255), self.screen, history_left + 60, base_y + 60)
                    draw_text(str(game[2]), pygame.font.SysFont(None, 30), (255,255,255), self.screen, history_left + 130 + 90, base_y + 60)
                    draw_text(str(game[3]), pygame.font.SysFont(None, 30), (255,255,255), self.screen, history_left + 260 + 120, base_y + 60)
                    draw_text(str(game[4]), pygame.font.SysFont(None, 30), (255,255,255), self.screen, history_left + 390 + 150, base_y + 60)
                    draw_text(str(game[5]), pygame.font.SysFont(None, 30), (255,255,255), self.screen, history_left + 520 + 180, base_y + 60)
                    draw_text(str(game[6]), pygame.font.SysFont(None, 30), (255,255,255), self.screen, history_left + 650 + 210, base_y + 60)
                    base_y += 50
        
        self.change_page(checkmark_rect, len(all_games))
        

    def change_page(self, example_rect, len_of_all):
        page_back = pygame.Rect(example_rect.left, example_rect.top - 30, 20, 20)
        page_forwards = pygame.Rect(example_rect.left + 30, example_rect.top - 30, 20, 20)

        pygame.draw.rect(self.screen, (255, 255, 255), page_back)
        pygame.draw.rect(self.screen, (255, 255, 255), page_forwards)

        if page_back.collidepoint(self.mx, self.my):
            if self.click:
                if self.history_page > 1:
                    self.history_page -= 1
        
        if page_forwards.collidepoint(self.mx, self.my):
            if self.click:
                if self.history_page < len_of_all / 7:
                    self.history_page += 1


    def edit_enemies(self):
        edit_enemies_left = 527.5
        edit_enemies_top = 100
        edit_enemies_width = 545
        edit_enemies_length = 700
        edit_enemies_rect = pygame.Rect(edit_enemies_left, edit_enemies_top, edit_enemies_width, edit_enemies_length)
        pygame.draw.rect(self.screen, (50, 50, 50), edit_enemies_rect)
        # draw_img_on_rect(self.screen, "images/UI/T_CharacterSelectionBackground.png", edit_enemies_rect.left, edit_enemies_rect.top, edit_enemies_rect.width, edit_enemies_rect.height)

        checkmark_rect = draw_checkmark_on_menu(self.screen, edit_enemies_rect)

        if not edit_enemies_rect.collidepoint(self.mx, self.my) or checkmark_rect.collidepoint(self.mx, self.my):
            if self.click:
                self.load_edit_enemies = False

        base_x = edit_enemies_left + 20
        base_y = edit_enemies_top + 20

        all_enemies = get_all_enemies()
        for i in range(len(all_enemies)):
            
            enemy_image = all_enemies[i][-1]
            if enemy_image[-1] == "_":
                enemy_image = f'{enemy_image}D'

            enemy_rect = pygame.Rect(base_x, base_y, 85, 85)
            # Draws the obstacle images
            draw_img_on_rect(self.screen, f'images/Enemies/{enemy_image}', base_x, base_y, 85, 85)

            if enemy_rect.collidepoint(self.mx, self.my):
                if self.click:
                    self.load_enemy = True
                    self.load_edit_enemies = False
                    self.enemy_selected = all_enemies[i]
                    self.new_enemy_health = str(self.enemy_selected[2])
                    self.new_enemy_speed = str(self.enemy_selected[3])
                    self.new_enemy_attack = str(self.enemy_selected[4])

            base_x += 85 + 20

            # 5 in a row
            if (i+1) % 5 == 0:
                base_x = edit_enemies_left + 20
                base_y += 85 + 20

    def edit_enemy(self):
        # Name
        name = self.enemy_selected[1]
        # Image
        enemy_img = self.enemy_selected[-1]
    
        popup_left = 550
        popup_top = 100
        popup_width = 500
        popup_height = 700
        popup = pygame.Rect(popup_left, popup_top, popup_width, popup_height)
        pygame.draw.rect(self.screen, (40, 40, 40), popup)

        # Inputfield for creating new profile
        new_health_inputfield = pygame.Rect(popup_left + 30, popup_top + 30 + 85 * 3 + 30 + 30, popup_width - 60, 50)
        draw_text("Health", pygame.font.SysFont(None, 35), (255, 255, 255), self.screen, new_health_inputfield.left + 5, new_health_inputfield.top - 30)
        pygame.draw.rect(self.screen, (255, 255, 255), new_health_inputfield)

        new_attack_inputfield = pygame.Rect(popup_left + 30, popup_top + 30 + 85 * 3 + 30 + 70 + 60, popup_width - 60, 50)
        draw_text("Attack", pygame.font.SysFont(None, 35), (255, 255, 255), self.screen, new_attack_inputfield.left + 5, new_attack_inputfield.top - 30)
        pygame.draw.rect(self.screen, (255, 255, 255), new_attack_inputfield)

        # new_speed_inputfield = pygame.Rect(popup_left + 30, popup_top + 30 + 85 * 3 + 30 + 70 + 60, popup_width - 60, 50)
        # draw_text("Speed", pygame.font.SysFont(None, 35), (255, 255, 255), self.screen, new_speed_inputfield.left + 5, new_speed_inputfield.top - 30)
        # pygame.draw.rect(self.screen, (255, 255, 255), new_speed_inputfield)

        # new_attack_inputfield = pygame.Rect(popup_left + 30, popup_top + 30 + 85 * 3 + 30 + 70 + 70 + 90, popup_width - 60, 50)
        # draw_text("Attack", pygame.font.SysFont(None, 35), (255, 255, 255), self.screen, new_attack_inputfield.left + 5, new_attack_inputfield.top - 30)
        # pygame.draw.rect(self.screen, (255, 255, 255), new_attack_inputfield)

        draw_img_on_rect(self.screen, f'images/Enemies/{enemy_img}', popup_left + 122.5, popup_top + 30, 85 * 3, 85 * 3)
        draw_text(name, pygame.font.SysFont(None, 50), (255, 255, 255), self.screen, popup_left + 5, popup_top + 10)

        draw_text(self.new_enemy_health, pygame.font.SysFont(None, 50), (0, 0, 0), self.screen, new_health_inputfield.left + 5, new_health_inputfield.top + 10)
        # draw_text(self.new_enemy_speed, pygame.font.SysFont(None, 50), (0, 0, 0), self.screen, new_speed_inputfield.left + 5, new_speed_inputfield.top + 10)
        draw_text(self.new_enemy_attack, pygame.font.SysFont(None, 50), (0, 0, 0), self.screen, new_attack_inputfield.left + 5, new_attack_inputfield.top + 10)

        draw_text(self.error_msg, pygame.font.SysFont(None, 40), (255, 50, 50), self.screen, popup_left, popup_top + popup_height + 5)

        checkmark_rect = draw_checkmark_on_menu(self.screen, popup)

        # Activating input field
        if new_health_inputfield.collidepoint(self.mx, self.my):
            if self.click:
                self.editing_enemy_health = True
                self.editing_enemy_speed = False
                self.editing_enemy_attack = False

        # elif new_speed_inputfield.collidepoint(self.mx, self.my):
        #     if self.click:
        #         self.editing_enemy_speed = True
        #         self.editing_enemy_attack = False
        #         self.editing_enemy_health = False

        elif new_attack_inputfield.collidepoint(self.mx, self.my):
            if self.click:
                self.editing_enemy_attack = True
                self.editing_enemy_speed = False
                self.editing_enemy_health = False

        elif self.click:
            self.editing_enemy_health = False
            self.editing_enemy_speed = False
            self.editing_enemy_attack = False

            if checkmark_rect.collidepoint(self.mx, self.my):
                if re.match(r'^[0-9]+$', self.new_enemy_health) and re.match(r'^[0-9]+$', self.new_enemy_speed) and re.match(r'^[0-9]+$', self.new_enemy_attack) and len(self.new_enemy_health) > 0 and len(self.new_enemy_speed) > 0 and len(self.new_enemy_attack) > 0:

                    # update_enemy(name, int(self.new_enemy_health), int(self.new_enemy_speed), int(self.new_enemy_attack))
                    update_enemy(name, int(self.new_enemy_health), 1, int(self.new_enemy_attack))
                    self.new_enemy_attack = ""
                    self.new_enemy_health = ""
                    self.new_enemy_speed = ""
                    self.load_enemy = False
                    self.enemy_selected = None
                    self.error_msg = ""
                else:
                    self.error_msg = "Invalid symbols"