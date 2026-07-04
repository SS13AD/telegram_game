import json
import os
import random

class RoomManager:
    def __init__(self, filename='rooms.json', rooms_count=10):
        self.filename = filename
        self.rooms = []
        self.rooms_count = rooms_count
        self.used_ids = {room['id'] for room in self.rooms}
        self.current_room_id = 0

        self.types_rooms = ['space_station_room', 'open_space_room']
        self.entities = ['monster_small', 'monster_medium', 'chest']

        self.load_rooms()

    def load_rooms(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.rooms = json.load(f)
                return

        self.generate_random_rooms(self.rooms_count)

    def save_rooms(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.rooms, f, ensure_ascii=False, indent=2)

    def is_id_unique(self, new_id):
        return new_id not in self.used_ids

    def generate_valid_id(self, current_id):
        first_id = 1
        while not self.is_id_unique(first_id):
            first_id += 1

        return first_id

    def get_room(self, room_id):
        return next((room for room in self.rooms if room['id'] == room_id), None)

    def get_current_room(self):
        return self.get_room(self.current_room_id)

    def move_to_direction(self, direction):
        current_room = self.get_current_room()
        if not current_room:
            return False

        if direction in current_room['directions']:
            self.current_room_id = current_room['directions'][direction]
            return True

    def create_room(self, current_room_id, direction, room_type=None, objects=None):
        current_room = self.get_room(current_room_id)
        if not current_room:
            print(f"Ошибка: комната с ID {current_room_id} не найдена!")
            return None

        if 'directions' in current_room and direction in current_room['directions']:
            print('В комнате уже есть выход в этом направлении')
            return None

        new_id = self.generate_valid_id(current_room_id)

        new_room = {
            'id': new_id,
            'name': f'Комната {new_id}',
            'type': room_type or random.choice(self.types_rooms),
            'objects': objects or random.sample(
                self.entities,
                random.randint(0, 3)
            ),
            'directions': {},
        }

        current_room['directions'][direction] = new_id
        opposite_direction = {'up':'back', 'back':'up', 'right': 'left', 'left':'right'}[direction]
        new_room['directions'][opposite_direction] = current_room_id

        self.rooms.append(new_room)
        self.used_ids.add(new_id)

        print(f"Создана комната ID {new_id}, {direction}")
        return new_id

    def generate_random_rooms(self, num_rooms):
        print(f"Генерируем {num_rooms} комнат...")

        if not self.rooms:
            start_room = {
                'id': 0,
                'name': 'Стартовая комната',
                'type': 'space_station_room',
                'objects': [],
                'directions': {}
            }

            self.rooms.append(start_room)
            self.used_ids.add(0)

        avaliable_rooms = [0]

        for i in range(num_rooms):
            current_room_id = random.choice(avaliable_rooms)
            direction = random.choice(['up', 'right', 'left', 'back'])

            new_id = None
            iterations = 100
            while new_id == None and iterations > 0:
                new_id = self.create_room(current_room_id, direction,
                                          random.choice(self.types_rooms),
                                          random.sample(self.entities, random.randint(0, 3)))
                iterations -= 1

            if new_id is not None:
                avaliable_rooms.append(new_id)
                if len(avaliable_rooms) > 1:
                    avaliable_rooms.remove(current_room_id)

        self.save_rooms()

roomman = RoomManager(rooms_count = 20)
