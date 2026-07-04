from models.entity import Entity
from models.inventory import Inventory
import random

class Monster:
    def __init__(self, monster_type='small'):
        self.type = monster_type
        if monster_type == 'small':
            self.name = 'Маленький монстр'
            self.health = 30
            self.max_health = 30
            self.damage = 5
            self.reward_money = 10
        elif monster_type == 'medium':
            self.name = 'Средний монстр'
            self.health = 50
            self.max_health = 50
            self.damage = 10
            self.reward_money = 20
        else:
            self.name = 'Большой монстр'
            self.health = 100
            self.max_health = 100
            self.damage = 20
            self.reward_money = 100

    def attack(self):
        step_damage = 2

        return random.randint(self.damage - step_damage, self.damage + step_damage)

