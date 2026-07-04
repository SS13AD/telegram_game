from models.item import Item

class Inventory:
    def __init__(self):
        self.items = []
        self.current_weight = 0
        self.max_weight = 100

    def add_item(self, item):
        self.current_weight += item.weight
        self.items.append(item)


    def delete_item(self, id):
        self.current_weight -= self.items[id].weight
        self.items.remove(id)