

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton('Рассчитать')
button2 = KeyboardButton('Информация')
button3 = KeyboardButton('Купить')

kb.add(button1)
kb.add(button2)
kb.add(button3)

inl_kb = InlineKeyboardMarkup(resize_keyboard=True)
but_1 = InlineKeyboardButton('Продукт1', callback_data='product_buying')
but_2 = InlineKeyboardButton('Продукт2', callback_data='product_buying')
but_3 = InlineKeyboardButton('Продукт3', callback_data='product_buying')
but_4 = InlineKeyboardButton('Продукт4', callback_data='product_buying')

inl_kb.add(but_1)
inl_kb.add(but_2)
inl_kb.add(but_3)
inl_kb.add(but_4)


class UserState(StatesGroup):
    age = State()
    growth =State()
    weight =State()

@dp.message_handler(text = 'Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Расчет калорий для мужчин: 10 * вес(кг) + 6,25 * рост(см) -5 * возраст(лет) + 5')


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1,5):
        with open(f'pictures/{i}.jpg', 'rb') as img:
            await message.answer_photo(img, f'Название: Витамины {i} | Описание: описание {i} | Цена: {i *100}')
    await message.answer("Выберите продукт для покупки", reply_markup = inl_kb)


# 3.  Callback хэндлер, который реагирует на текст "product_buying" и оборачивает функцию send_confirm_message(call).
# 4.  Функция send_confirm_message, присылает сообщение "Вы успешно приобрели продукт!"
@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!", reply_markup = inl_kb)
    await call.answer()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5

    await message.answer(f'Ваша норма калорий {calories}')
    await state.finish()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Начали', reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)