import pygame
from models.inventory import Inventory

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.surface.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = ''
        self.hp = 100
        self.add_hp = 0
        self.protect = 0
        self.mana = 0
        self.max_mana = 100
        self.max_hp = 100
        self.equipped = {
            'weapon': None,
            'armor': None,
            'ring': None,
            'amulet': None
        }
        self.money = 0
        self.inventory = Inventory()

    def decrease_hp(self, damage):
        if self.hp > 0:
            self.hp -= damage
            if self.hp <= 0:
                return #проигрышь

    def receving_hp(self, heal):
        if self.hp > 0:
            self.hp += heal
            if self.hp > self.max_hp:
                self.hp = self.max_hp

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

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