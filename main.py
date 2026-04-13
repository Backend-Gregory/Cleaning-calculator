import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class CleaningForm(StatesGroup):
    area = State()
    name = State()
    phone = State()
    address = State()

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рассчитать уборку')]
    ],
    resize_keyboard=True
)

@dp.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🧹 Привет! Я бот клининговой компании «Чистота».\n"
        "Я помогу рассчитать стоимость уборки твоей квартиры.\n"
        "👇 Нажми на кнопку «Рассчитать уборку», чтобы начать.\n",
        reply_markup=kb
    )

@dp.message(lambda message: message.text == 'Рассчитать уборку')
async def start_calculation(message: types.Message, state: FSMContext):
    await state.set_state(CleaningForm.area)
    await message.answer('Введите площадь квартиры в квадратных метрах (м²)', reply_markup=ReplyKeyboardRemove())