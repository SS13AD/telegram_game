import pygame

class Item:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.image = pygame.surface.Surface((50, 50))