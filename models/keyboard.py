import aiogram

from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove, FSInputFile
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

key = ['Прямо', 'Назад', 'Налево', 'Направо', 'Инвентарь']

keyboard = aiogram.types.InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=key[0], callback_data=key[0]), InlineKeyboardButton(text=key[1], callback_data=key[1]), InlineKeyboardButton(text=key[2], callback_data=key[2]), InlineKeyboardButton(text=key[3], callback_data=key[3])], [InlineKeyboardButton(text=key[4], callback_data=key[4])]], resize_keyboard=True)