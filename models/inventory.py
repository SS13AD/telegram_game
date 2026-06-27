class Inventory:
    def __init__(self):
        self.items = []
        self.max_weight = 100

    def add_item(self, item):
        self.items.append(item)

    def delete_item(self, id):
        self.items.remove(id)