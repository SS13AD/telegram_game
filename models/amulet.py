from models.item import Item

class Amulet(Item):
    def __init__(self, name, weight, hp=0, mana=0, protect=0):
        super().__init__(name, weight)
        self.advance = {
            'hp': hp,
            'mana': mana,
            'protect': protect
        }