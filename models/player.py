import pygame
from models.inventory import Inventory

class Player:
    def __init__(self):
        super().__init__()

        self.name = ''

        self.health = 100
        self.mana = 0
        self.money = 0
        self.protect = 0
        self.damage = 10

        self.max_mana = 100
        self.max_health = 100

        self.add_hp = 0
        self.equipped = {
            'weapon': None,
            'armor': None,
            'ring': None,
            'amulet': None
        }
        self.inventory = Inventory()

    def decrease_hp(self, damage):
        if self.hp > 0:
            self.hp -= damage
            if self.hp <= 0:
                return #проигрышь

    def receiving_hp(self, heal):
        if self.hp > 0:
            self.hp += heal
            if self.hp > self.max_hp:
                self.hp = self.max_hp

    # def move(self, x, y):
    #     self.rect.x = x
    #     self.rect.y = y

    def decrease_mana(self, down_mana):
        if self.mana >= 0:
            self.mana -= down_mana
            if self.mana < 0:
                self.mana = 0

    def receving_mana(self, up_mana):
        if self.mana > 0:
            self.mana += up_mana
            if self.mana > self.max_mana:
                self.mana = self.max_mana