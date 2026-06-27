import json
import os
import random

class RoomManager:
    def __init__(self, filename='rooms.json'):
        self.filename = filename
        self.rooms = self.load_rooms()
        self.used_ids = {room['id'] for room in self.rooms}
        self.coordinates = {0: (0, 0)}

    def load_rooms(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return [{
            'id': 0,
            'name': 'Стартовая комната',
            'type': 'space_station_room',
            'objects': [],
            'directions': ['up', 'back', 'right', 'left'],
            'position': 'vertical'
        }]

    def save_rooms(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.rooms, f, ensure_ascii=False, indent=2)

    def is_id_unique(self, new_id):
        return new_id not in self.used_ids


    def check_parity_rule(self, new_id, direction):
        if direction == 'up':
            return new_id % 2 == 0
        else:  # left, right, back
            return new_id % 2 == 1

    def generate_valid_id(self, current_id, direction):
        if direction in ['left', 'right', 'back']:
            candidate_id = current_id + 1
        elif direction == 'up':
            candidate_id = current_id + 2
        else:
            raise ValueError("Неизвестное направление")

        while True:
            if (self.is_id_unique(candidate_id) and
                self.check_parity_rule(candidate_id, direction)):
                return candidate_id
            candidate_id += 1

    def get_coordinates(self, current_id, direction):
        x, y = self.coordinates[current_id]
        if direction == 'up':
            return (x, y + 1)
        elif direction == 'right':
            return (x + 1, y)
        elif direction == 'left':
            return (x - 1, y)
        elif direction == 'back':
            return (x, y - 1)

    def room_exists_at_coords(self, coords):
        """Проверяет, существует ли комната с такими координатами (чтобы избежать пересечений)."""
        return coords in self.coordinates.values()

    def create_room(self, current_room_id, direction, room_type=None, objects=None):
        current_room = next((r for r in self.rooms if r['id'] == current_room_id), None)
        if not current_room:
            print(f"Ошибка: комната с ID {current_room_id} не найдена!")
            return None

        new_id = self.generate_valid_id(current_room_id, direction)
        position = 'vertical' if direction == 'up' else 'horizontal'
        new_coords = self.get_coordinates(current_room_id, direction)

        # Проверка на пересечение комнат
        if self.room_exists_at_coords(new_coords):
            print(f"Комната с координатами {new_coords} уже существует, пропускаем создание комнаты ID {new_id}")
            return None

        self.coordinates[new_id] = new_coords

        new_room = {
            'id': new_id,
            'name': f'Комната {new_id}',
            'type': room_type or random.choice(['space_station_room', 'open_space_room']),
            'objects': objects or random.sample(
                ['monster_small', 'monster_medium', 'chest'],
                random.randint(0, 3)
            ),
            'directions': ['up', 'back', 'right', 'left'],
            'position': position,
            'from_room': current_room_id,
            'direction': direction,
            'coordinates': new_coords
        }

        self.rooms.append(new_room)
        self.used_ids.add(new_id)

        print(f"Создана комната ID {new_id}: {position}, {direction} (координаты: {new_coords})")
        return new_id

    def generate_random_rooms(self, num_rooms):
        print(f"Генерируем {num_rooms} комнат...")

        # Первая комната вверх от стартовой (ID 2)
        id_2 = self.create_room(0, 'up', 'space_station_room', ['monster_small'])
        if id_2 is None:
            return

        available_rooms = [id_2]

        for _ in range(num_rooms - 1):
            # Выбираем случайную комнату из доступных для развития
            current_room_id = random.choice(available_rooms)
            # Случайное направление
            direction = random.choice(['up', 'right', 'left', 'back'])
            # Создаём комнату
            new_id = self.create_room(
                current_room_id,
                direction,
                random.choice(['space_station_room', 'open_space_room']),
                random.sample(['monster_small', 'monster_medium', 'chest'], random.randint(0, 2))
            )

            if new_id:
                available_rooms.append(new_id)
                # С вероятностью 20% убираем родительскую комнату из списка доступных для развития (создаём развилку)
                if random.random() < 0.2:
                    available_rooms.remove(current_room_id)