from td_menu import MainMenu
from td_game import TDGame

class ViewState:
    def __init__(self):
        self.state = "menu"
        self.selected_profile = None
        self.quit = False
        self.map_selected = None
        self.saved_game = []

    def set_state(self, new_state):
        self.state = new_state
    
    def get_state(self):
        return self.state
    
    def get_selected_profile(self):
        return self.selected_profile
    
    def set_selected_profile(self, profile):
        self.selected_profile = profile

    def get_quit(self):
        return self.quit
    
    def set_quit(self, quit):
        self.quit = quit

    def get_map_selected(self):
        return self.map_selected
    
    def set_map_selected(self, map_selected):
        self.map_selected = map_selected

    def get_saved_game(self):
        return self.saved_game
    
    def set_saved_game(self, saved_game):
        self.saved_game = saved_game


def main():
    view_state = ViewState()
    while True:
        if view_state.get_state() == "menu":
            MainMenu(view_state)
        if view_state.get_state() == "game":
            TDGame(view_state)
        if view_state.get_quit() == True:
            break

if __name__ == "__main__":
    main()