from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder



main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Чат')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню')
