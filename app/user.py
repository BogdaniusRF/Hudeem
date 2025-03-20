from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, CommandObject
from app.generators import gpt_openai
import app.keyboards as kb
from app.database.requests import set_user
from app.states import Chat
from aiogram.fsm.context import FSMContext
from app.generators import gpt_openai
# from middlewares import BaseMiddleware

user = Router()

# user.message.middleware(BaseMiddleware())

@user.message(CommandStart())
async def cmd_start(message: Message):
    #await set_user(message.from_user.id)
    await message.answer('Добро пожаловать в бот!', reply_markup=kb.main)

@user.message(F.text == 'Чат')
async def chatting_openai(message: Message, state: FSMContext):
    await state.set_state(Chat.text) # Юзер в состоянии чатинга и ожидается текст. В примере с фото будет ожидание фото
    await set_user(message.from_user.id)
    await message.answer('Введите важ вопрос к модели')

@user.message(Chat.text)  # Хэндлер, который ловит состояние в ф-ции выше и отвечает на запрос к модели
async def chatting_openai_response(message: Message, state: FSMContext):
    response = await gpt_openai(message.text, "gpt-4o-mini")
    await message.answer(response)
    #await state.clear()  # очитстка состояния. Для продолжения возможно стоит убрать эту стр-ку

@user.message(Chat.wait)
async def wait_wait(message: Message):
    await message.answer('Ваш запрос обрабатывается, подождите')


