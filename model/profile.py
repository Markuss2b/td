class Profile:
    def __init__(self, id, name, wins, losses):
        self.id = id
        self.name = name
        self.wins = wins
        self.losses = losses

    def get_name(self):
        return self.name