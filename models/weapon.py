from models.item import Item

class Weapon(Item):
    def __init__(self, name, weight, damage):
        super().__init__(name, weight)
        self.damage = damage