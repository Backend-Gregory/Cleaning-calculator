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

@dp.message(CleaningForm.area)
async def get_area(message: types.Message, state: FSMContext):
    if not message.text.strip():
        await message.answer('❌ Площадь не может быть пустой')
        return
    try:
        area = float(message.text.replace(',', '.'))
    except ValueError:
        await message.answer("❌ Введите число (например, 45 или 45.5)")
        return
    
    price = area * 200
    await state.update_data(area=area, price=price)
    await state.set_state(CleaningForm.name)
    await message.answer('Как вас завут?')

@dp.message(CleaningForm.name)
async def get_name(message: types.Message, state: FSMContext):
    if not message.text.strip():
        await message.answer('❌ Имя не может быть пустым')
        return
    if len(message.text) > 100:
        await message.answer('❌ Имя не должно быть длиннее 100 символов')
        return
    await state.update_data(name=message.text)
    await state.set_state(CleaningForm.phone)
    await message.answer('Какой у вас номер телефона?')

@dp.message(CleaningForm.phone)
async def get_phone(message: types.Message, state: FSMContext):
    if not message.text.strip():
        await message.answer('❌ Номер телефона не может быть пустым')
        return
    await state.update_data(phone=message.text)
    await state.set_state(CleaningForm.address)
    await message.answer('Какой у вас адрес?')

@dp.message(CleaningForm.address)
async def get_address(message: types.Message, state: FSMContext):
    if not message.text.strip():
        await message.answer('❌ Адрес не может быть пустым')
        return
    await state.update_data(address=message.text)
    data = await state.get_data()
    text = "📝 Новая заявка!\n\n"
    text += f"Площадь: {data.get('area')}м²\n"
    text += f"Сумма: {data.get('price')}₽\n"
    text += f"Имя: {data.get('name')}\n"
    text += f"Телефон: {data.get('phone')}\n"
    text += f"Адрес: {data.get('address')}"
    try:
        await bot.send_message(ADMIN_ID, text)
        await state.clear()
        await message.answer('✅ Спасибо! Мы свяжемся с вами.', reply_markup=kb)
    except Exception:
        await message.answer('❌ Не удалось отправить заявку. Попробуйте позже')