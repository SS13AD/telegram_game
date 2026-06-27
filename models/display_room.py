import json
import pygame

def get_entities(index):
    with open('map.json', 'r') as f:
        map = json.load(f)['map']['rooms']
        current_room = map[index]
        current_entities = current_room['entities']
        start_x = 50
        start_y = 50
        entities = []
        for entity in current_entities:
            current_rect = pygame.Rect(start_x, start_y, 50, 50)
            entities.append(current_rect)
            start_x += 50
        return entities