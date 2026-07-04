import aiogram
import pygame
import asyncio
import random

from aiogram import Dispatcher, Bot, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove, FSInputFile
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from pygame.examples.moveit import WIDTH

from models.keyboard import keyboard
from config import *
from models.map_generator import RoomManager
from models.display_room import *
from models.game import *
from models.game_manager import GameManager

game_manager = None

dp = Dispatcher()
bot = Bot(Token)
user_states = {}
main_message = None

screen = pygame.display.set_mode((WIDTH, HEIGHT))

def get_game_keyboard():
    global game_manager

    actions_row = []
    actions = game_manager.get_available_actions()

    all_buttons = {
        'Вверх ⬆️': 'up',
        'Вниз ⬇️': 'backward',
        '⬅️ Налево': 'left',
        'Направо ➡️': 'right',
        '🎒 Инвентарь': 'inventory'
    }
    keys = list(all_buttons.keys())

    keyboard_movement = [[InlineKeyboardButton(text=keys[0], callback_data=all_buttons[keys[0]])],
                [InlineKeyboardButton(text=keys[2], callback_data=all_buttons[keys[2]]),
                 InlineKeyboardButton(text=keys[3], callback_data=all_buttons[keys[3]])],
                [InlineKeyboardButton(text=keys[1], callback_data=all_buttons[keys[1]])],
                [InlineKeyboardButton(text=keys[4], callback_data=all_buttons[keys[4]])]]


    if 'attack' in actions:
        actions_row.append(InlineKeyboardButton(text='Атака',
                                                callback_data='attack'))
    if 'defend' in actions:
        actions_row.append(InlineKeyboardButton(text='Защита',
                                                callback_data='defend'))
    if 'open_chest' in actions:
        actions_row.append(InlineKeyboardButton(text='Открыть сундук',
                                                callback_data='open_chest'))
    new_keyboard = keyboard_movement
    if len(actions_row) > 0:
        new_keyboard.append(actions_row)

    return InlineKeyboardMarkup(inline_keyboard=new_keyboard)


async def update_game_display():
    global main_message, screen, game_manager

    game_manager.check_room_objects()
    game_manager.render_room(screen)

    pygame.image.save(screen, 'game.png')

    if main_message:
        file = types.InputMediaPhoto(media=FSInputFile('game.png'))
        await main_message.edit_media(media=file, reply_markup=get_game_keyboard())

@dp.message(lambda message:message.text == '/start')
async def start(message):
    global main_message, game_manager

    game_manager = GameManager()

    game_manager.current_room_id = 0

    game_manager.render_room(screen)
    pygame.image.save(screen, 'game.png')

    main_message = await message.answer_photo(photo=FSInputFile('game.png'), reply_markup=get_game_keyboard())

@dp.callback_query(F.data == 'right')
async def right(callback):
     await handle_movement(callback, 'right')

@dp.callback_query(F.data == 'left')
async def left(callback):
    await handle_movement(callback, 'left')

@dp.callback_query(F.data == 'up')
async def forward(callback):
    await handle_movement(callback, 'up')

@dp.callback_query(F.data == 'backward')
async def back(callback):
    await handle_movement(callback, 'back')

@dp.callback_query(F.data == 'attack')
async def attack(callback):
    global game_manager

    if not game_manager.in_combat:
        room = game_manager.get_current_room()
        if room and any('monster' in obj for obj in room.get('objects', [])):
            game_manager.check_room_objects()
            await update_game_display
            await callback.answer('Монстр атакован')
            return
        else:
            await callback.answer('Здесь нет монстров')
            return

    result = game_manager.attack_monster()
    await update_game_display()

    if not game_manager.in_combat:
        await update_game_display()

    await callback.answer(result)

@dp.callback_query(F.data == 'open_chest')
async def open_chest(callback):
    room = game_manager.get_current_room()
    if not room or 'chest' not in room.get('objects', None):
        await callback.answer("Здесь нет сундука")
        return

    game_manager.open_chest()
    room['objects'].remove('chest')

    game_manager.room_manager.save_rooms()

    await update_game_display()
    await callback.answer('Сундук открыт, предмет в инвентаре')

async def handle_movement(callback, direction):
    global game_manager

    if game_manager.move(direction):
        await update_game_display()

        caption = f'Вы в комнате {game_manager.current_room_id}'
        caption += f'Тип: {game_manager.get_room_type()}'
        caption += f'Объекты: {''.join(game_manager.get_room_objects())}'

        await callback.answer(f'Перешли в комнату {game_manager.current_room_id}')
    else:
        await callback.answer('Там нет прохода')

@dp.callback_query(F.data == 'back_to_game')
async def back_to_game(callback):
    await update_game_display()

@dp.callback_query(F.data == 'inventory')
async def show_inventory(callback):
    global game_manager

    screen.fill(pygame.Color('Black'))

    start_x = 10 #Стартовая позиция x первого предмета
    start_y = 10 #Стартовая позиция y первого предмета

    x = start_x #Позиция конкретного предмета x
    y = start_y #Позиция конкретного предмета y

    margin = 10 #Отступ между предметами
    item_size = 100 #Размер одного предмета (100x100)

    row_count = WIDTH // item_size + margin #Вычисление кол-ва предметов в одном ряду

    keys = [[]] #Все кнопки на клаве

    current_item = 0 #Предмет, который перебираем сейчас
    current_row = 0 #Ряд, в котором сейчас находимся
    for item in game_manager.player.inventory.items:
        screen.blit(item.image, (x, y))

        if current_item >= row_count:
            x = start_x
            y += item_size + margin

            current_item = 0
            current_row += 1

            keys.append([])
            keys[current_row].append(InlineKeyboardButton(text=item.name, callback_data=item.name))
        else:
            x += item_size + margin

            keys[current_row].append(InlineKeyboardButton(text=item.name, callback_data=item.name))

        current_item += 1

    pygame.display.flip()

    pygame.image.save(screen, 'start.png')
    file = types.InputMediaPhoto(media=FSInputFile('start.png'))

    keys.reverse()
    keys.append([InlineKeyboardButton(text='Назад', callback_data='back_to_game')])

    keyboard_inventory = aiogram.types.InlineKeyboardMarkup(inline_keyboard=keys, resize_keyboard=True)

    await main_message.edit_media(media=file, reply_markup=keyboard_inventory)

async def main():
    print('Bot started')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())