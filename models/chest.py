from models.entity import Entity
from models.inventory import Inventory


class Chest(Entity):
    def __init__(self, x, y, name, hp, actions):
        super().__init__(x, y, name, hp, actions)
        self.inventory = Inventory()

    def open(self):
        self.hp = 0
        return self.inventory