import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, name, hp, actions):
        super().__init__()
        self.image = pygame.surface.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.hp = hp
        self.actions = actions

    def decrease_hp(self, damage):
        if self.hp > 0:
            self.hp -= damage
            if self.hp <= 0:
                return  # разрушение энтити

    def receving_hp(self, heal):
        if self.hp > 0:
            self.hp += heal
            if self.hp > self.max_hp:
                self.hp = self.max_hp