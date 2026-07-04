import pygame
from models.map_generator import RoomManager
from models.game import Game

class GameManager:
    def __init__(self):
        self.room_manager = RoomManager()
        self.game = Game()
        self.current_room_id = 0

    def get_current_room(self):
        return self.room_manager.get_room(self.current_room_id)

    def move(self, direction):
        if self.room_manager.move_to_direction(direction):
            self.current_room_id = self.room_manager.current_room_id
            return True
        return False

    def get_available_directions(self):
        room = self.get_current_room()
        if room:
            return list(room['directions'].keys())

        return []

    def get_room_objects(self):
        room = self.get_current_room()
        if room:
            return room.get('objects', [])

        return []

    def get_room_type(self):
        room = self.get_current_room()
        if room:
            return room.get('type', 'unknown')

        return 'unknown'

    def render_room(self, screen):
        room = self.get_current_room()
        if not room:
            return

        pygame.init()

        room_type = self.get_room_type()
        objects = self.get_room_objects()

        if room_type == 'space_station_room':
            screen.fill(pygame.Color('Gray'))
        else:
            screen.fill(pygame.Color('Blue'))

        for i in range(len(objects)):
            x = 50 + i * 150
            y = 200
            if objects[i] == 'monster_small':
                pygame.draw.circle(screen, pygame.Color('Red'), (x,y), 30)
            elif objects[i] == 'monster_medium':
                pygame.draw.circle(screen, pygame.Color('Red'), (x, y), 50)
            elif objects[i] == 'chest':
                pygame.draw.rect(screen, pygame.Color('Gold'), (x, y, 60, 60))

        directions = self.get_available_directions()
        if 'up' in directions:
            pygame.draw.rect(screen, pygame.Color('Green'), (250, 50, 100, 30))
        if 'right' in directions:
            pygame.draw.rect(screen, pygame.Color('Green'), (450, 250, 40, 100))
        if 'left' in directions:
            pygame.draw.rect(screen, pygame.Color('Green'), (50, 250, 40, 100))
        if 'back' in directions:
            pygame.draw.rect(screen, pygame.Color('Green'), (250, 450, 100, 30))

        font = pygame.font.Font(None, 36)
        text = font.render(f'Room: {self.current_room_id}', True, pygame.Color('White'))

        screen.blit(text, (10, 10))

        pygame.display.flip()

