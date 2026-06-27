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
roommanager = RoomManager()

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
    user_id = message.from_user.id
    user_states[user_id] = {'current_room': user_id}

    screen.fill(pygame.Color('Black'))
    pygame.display.flip()
    pygame.image.save(screen, 'start.png')

    roommanager = RoomManager()

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

# def check(side, callback):
#     data = callback.data
#     if data == 'Направо':
#         screen.fill(pygame.Color('White'))
#     elif data == 'Налево':
#         screen.fill(pygame.Color('Red'))
#     elif data == 'Прямо':
#         screen.fill(pygame.Color('Purple'))
#     elif data == 'Назад':
#         screen.fill(pygame.Color('Orange'))

# async def update(message, mode):
#     if mode == 'Move' and last_message_id != 0:
#     file = types.InputMediaPhoto(media=FSInputFile('start.png'), caption='move_right')
#     await message.message.edit_media(media=file, reply_markup=keyboard)

if __name__ == '__main__':
    asyncio.run(main())