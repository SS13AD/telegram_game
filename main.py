import aiogram
import pygame
import asyncio
import random

from aiogram import Dispatcher, Bot, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove, FSInputFile
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from pygame.examples.moveit import WIDTH

from models.keyboard import *
from config import *
from models.map_generator import RoomManager
from models.display_room import *
from models.game import *
roommanager = RoomManager()
gamemanager = Game()

dp = Dispatcher()
bot = Bot(Token)
user_states = {}
main_message = None

screen = pygame.display.set_mode((WIDTH, HEIGHT))

async def main():
    print('Bot started')
    await dp.start_polling(bot)

@dp.message(lambda message:message.text == '/start')
async def start(message):
    global main_message
    global gamemanager
    global roommanager
    user_id = message.from_user.id
    user_states[user_id] = {'current_room': user_id}

    screen.fill(pygame.Color('Black'))
    pygame.display.flip()
    pygame.image.save(screen, 'start.png')

    roommanager = RoomManager()
    gamemanager = Game()

    rects = get_entities(0)

    for rect in rects:
        pygame.draw.rect(screen, pygame.Color('White'), rect)
    main_message = await message.answer_photo(photo=FSInputFile('start.png'), reply_markup=keyboard)

@dp.callback_query(F.data=='Направо')
async def sides(callback):
    screen.fill(pygame.Color('White'))
    pygame.display.flip()
    pygame.image.save(screen, 'start.png')
    file = types.InputMediaPhoto(media=FSInputFile('start.png'))
    await main_message.edit_media(media=file, reply_markup=keyboard)

@dp.callback_query(F.data=='Налево')
async def sides(callback):
    screen.fill(pygame.Color('Red'))
    pygame.display.flip()
    pygame.image.save(screen, 'start.png')
    file = types.InputMediaPhoto(media=FSInputFile('start.png'))
    await main_message.edit_media(media=file, reply_markup=keyboard)

@dp.callback_query(F.data=='Прямо')
async def sides(callback):
    screen.fill(pygame.Color('Purple'))
    pygame.display.flip()
    pygame.image.save(screen, 'start.png')
    file = types.InputMediaPhoto(media=FSInputFile('start.png'))
    await main_message.edit_media(media=file, reply_markup=keyboard)

@dp.callback_query(F.data=='Назад')
async def sides(callback):
    screen.fill(pygame.Color('Blue'))
    pygame.display.flip()
    pygame.image.save(screen, 'start.png')
    file = types.InputMediaPhoto(media=FSInputFile('start.png'))
    await main_message.edit_media(media=file, reply_markup=keyboard)

@dp.callback_query(F.data=='Инвентарь')
async def show_inventory(callback):
    screen.fill(pygame.Color('Black'))
    x = 10
    y = 10
    current_item = 0
    row_count = WIDTH // 110
    keys = [[]]
    current_row = 0
    for item in gamemanager.player.inventory.items:
        screen.blit(item.image, (x, y))
        current_item += 1
        if current_item >= row_count:
            x = 10
            y += 100+10
            current_item = 0
            current_row += 1
            keys.append([])
            keys[current_row].append(InlineKeyboardButton(text=item.name, callback_data='123'))
        else:
            x += 100 + 10
            keys[current_row].append(InlineKeyboardButton(text=item.name, callback_data='123'))
    pygame.display.flip()
    pygame.image.save(screen, 'start.png')
    file = types.InputMediaPhoto(media=FSInputFile('start.png'))
    keys.append([InlineKeyboardButton(text='Назад', callback_data='Выйти из инвенторя')])
    keyboard_inventory = aiogram.types.InlineKeyboardMarkup(inline_keyboard=keys, resize_keyboard=True)
    await main_message.edit_media(media=file, reply_markup=keyboard_inventory)

if __name__ == '__main__':
    asyncio.run(main())