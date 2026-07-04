import aiogram

from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove, FSInputFile
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

all_buttons = {
    'Вверх ⬆️': 'up',
    'Вниз ⬇️': 'backward',
    '⬅️ Налево': 'left',
    'Направо ➡️': 'right',
    '🎒 Инвентарь': 'inventory'
}
keys = list(all_buttons.keys())

keyboard = [[InlineKeyboardButton(text=keys[0], callback_data=all_buttons[keys[0]])],
           [InlineKeyboardButton(text=keys[2], callback_data=all_buttons[keys[2]]), InlineKeyboardButton(text=keys[3], callback_data=all_buttons[keys[3]])],
           [InlineKeyboardButton(text=keys[1], callback_data=all_buttons[keys[1]])],
           [InlineKeyboardButton(text=keys[4], callback_data=all_buttons[keys[4]])]]