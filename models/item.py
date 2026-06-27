import pygame

class Item:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.image = pygame.image.load('test.jpg')
        self.image = pygame.transform.scale(self.image, (100, 100))