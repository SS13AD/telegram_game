import pygame
import json
import random

from models.map_generator import RoomManager
from models.game import Game
from models.player import Player
from models.enemy import Monster
from models.item import Item

class GameManager:
    def __init__(self):
        self.player = Player()
        self.in_combat = False
        self.current_monster = None
        self.combat_log = []

        self.room_manager = RoomManager()
        self.game = Game()

        self.current_room_id = 0

    def get_current_room(self):
        return self.room_manager.get_room(self.current_room_id)

    def move(self, direction):
        if self.in_combat:
            return False

        if self.room_manager.move_to_direction(direction):
            self.current_room_id = self.room_manager.current_room_id
            return True
        return False

    def get_available_directions(self):
        room = self.get_current_room()
        if room:
            return list(room['directions'].keys())

        return []

    def check_room_objects(self):
        room = self.get_current_room()
        if not room:
            return

        objects = room.get('objects', [])

        for obj in objects:
            if 'monster' in obj and not self.in_combat:
                monster_type = obj.split('_')[1] if '_' in obj else 'small'

                self.current_monster = Monster(monster_type)
                self.in_combat = True
                self.combat_log = [f'На вас напал {self.current_monster.name}']

        self.room_manager.save_rooms()

    def open_chest(self):
        items = ['Зелье здоровья', 'Зелье маны',
                 '100 Монет', '300 Монет',
                 'Железный клинок', 'Железный шлем']

        item_name = random.choice(items)
        item = Item(item_name, 5)

        self.player.inventory.add_item(item)
        self.combat_log.append(f'Вы нашли: {item_name}')

        self.save_inventory()

    def attack_monster(self):
        if not self.in_combat or not self.current_monster:
            return 'Нет противника для атаки'

        damage_step = 2
        player_damage = random.randint(self.player.damage - damage_step,
                                       self.player.damage + damage_step)

        self.current_monster.health -= player_damage
        log = f'Вы нанесли {player_damage} урона {self.current_monster.name}'

        if self.current_monster.health <= 0:
            self.combat_log.append(log)
            self.combat_log.append(f'Вы победили {self.current_monster.name}')

            self.in_combat = False

            room = self.get_current_room()

            if room and 'objects' in room:
                monster_obj = next((obj for obj in room['objects'] if 'monster' in obj), None)

                if monster_obj:
                    room['objects'].remove(monster_obj)

            reward = self.current_monster.reward_money

            self.player.money += reward
            self.combat_log.append(f'Вы получили: {reward} монет!')

            self.current_monster = None

            self.room_manager.save_rooms()
            return '\n'.join(self.combat_log)

        monster_damage = random.randint(self.current_monster.damage - damage_step,
                                        self.current_monster.damage + damage_step)
        self.player.health -= monster_damage

        log += f'\n{self.current_monster.name} нанес вам {monster_damage} урона'

        if self.player.health <= 0:
            self.combat_log.append(log)
            self.combat_log.append('Вас убили, игра начинается заново')

            self.player.health = self.player.max_health
            self.current_room_id = 0
            self.room_manager.current_room_id = 0
            self.in_combat = False
            self.current_monster = None
            return '\n'.join(self.combat_log)

    def get_available_actions(self):
        room = self.get_current_room()
        if not room:
            return []

        actions = []

        if self.in_combat:
            actions.append('attack')
            actions.append('defend')
            return actions

        objects = room.get('objects', [])

        if 'chest' in objects:
            actions.append('open_chest')

        return actions

    def defend(self):
        if not self.in_combat or not self.current_monster:
            return 'Нет монстра для защиты'

        damage_step = 2

        monster_base_damage = self.current_monster.damage
        monster_damage_protected = monster_base_damage * (1 - (self.player.protect/100))

        self.player.health -= monster_damage_protected
        log = f'Вы защитилисть и получили {monster_damage_protected} урона! (Минус {self.player.protect}% урона)'

        if self.player.health <= 0:
            self.combat_log.append(log)
            self.combat_log.append('Вас убили, игра начинается заново')

            self.player.health = self.player.max_health
            self.current_room_id = 0
            self.room_manager.current_room_id = 0
            self.in_combat = False
            self.current_monster = None
            return '\n'.join(self.combat_log)

        self.combat_log.append(log)
        return log

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

        hp_str = f'HP: {self.player.health}'
        hp_color = pygame.Color('Red')
        text_hp = font.render(hp_str, True, hp_color)

        money_str = f'M: {self.player.money}'
        money_color = pygame.Color('Gold')
        text_money = font.render(money_str, True, money_color)

        screen.blit(text, (10, 10))
        screen.blit(text_hp, (400, 10))
        screen.blit(text_money, (10, 400))

        if self.in_combat and self.current_monster:
            font_small = pygame.font.Font(None, 16)
            monster_info = f'{self.current_monster.name} HP: {self.current_monster.health}'
            text = font_small.render(monster_info, True, pygame.Color('Orange'))

            screen.blit(text, (300, 50))

        if self.combat_log:
            font_small = pygame.font.Font(None, 18)
            for i, log in enumerate(self.combat_log):
                text = font_small.render(log, True, pygame.Color('Yellow'))
                screen.blit(text, (10, 50 + i * 25))

        pygame.display.flip()

    def save_inventory(self):
        with open('inventory.json', 'w', encoding='utf-8') as f:
            json_inv = {
                'inventory': [item.name for item in self.player.inventory.items]
            }
            json.dump(json_inv, f, ensure_ascii=False, indent=2)

