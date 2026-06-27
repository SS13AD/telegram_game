from models.player import Player

class Game:
    def __init__(self):
        self.player = Player(50, 50)
        self.state= 'game'

    def go_to_inventory(self):
        self.state = 'inventory'

    def go_to_game(self):
        self.state = 'game'