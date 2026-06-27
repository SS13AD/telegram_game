from models.item import Item

class Armor(Item):
    def __init__(self, name, weight, protect):
        super().__init__(name, weight)
        self.protect = protect