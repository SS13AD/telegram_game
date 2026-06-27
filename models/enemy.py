from models.entity import Entity
from models.inventory import Inventory

class Enemy(Entity):
    def __init__(self, x, y, name, hp, actions, protect, mana, damage):
        super().__init__(x, y, name, hp, actions)
        self.mana = mana
        self.protect = protect
        self.inventory = Inventory()
        self.damage = damage

    def use_item(self):
        return #

    def atack(self, player):
        player.decrease_hp(self.damage)