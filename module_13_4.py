from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = ""
bot = Bot(token = api )
dp = Dispatcher(bot, storage= MemoryStorage())

class UserState(StatesGroup):
    """ Инициализация класса """
    age = State()
    growth = State()
    wight = State()

@dp.message_handler(text='Calories')        # Функция - реакция на определенные сообщения
async def set_message(message):
    await message.answer('Введите свой возраст.')
    await UserState.age.set()        # Запуск видоизменяющейся цепочки состояний от полученной, новой информации

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост.")
    await UserState.growth.set()              # 1-ое звено

@dp.message_handler(state=UserState.growth)
async def set_wight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес.")
    await UserState.wight.set()             # 2-ое звено

@dp.message_handler(state=UserState.wight)
async def send_calories(message, state):
    await state.update_data(wight=message.text)
    data = await  state.get_data()   # Хранилище полученных данных в виде словаря (значение в строковом представление)
    await message.answer(f"Ваша норма калорий на каждый день: "
                         f" {10 * int(data['wight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5}")
                         # Реализация формулы подсчета калорий из полученных данных
    await state.finish()  # Завершающее звено цепочки

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
