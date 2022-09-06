import json
import string
import time

from aiogram import types, Dispatcher
from create_bot import dp, bot
from .global_handler import global_handler


async def try_except(message: types.Message):
	try:
		await global_handler(message)
		await message.delete()
	except:
		await message.reply('Для общения с ботом через ЛС, напишите ему:\nhttps://t.me/Oksa_studio_bot')  # ответ бота с цитированием


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
	await try_except(message)


# @dp.message_handler(commands=['z', 'p', 'h', 'ex', 'ad'])
async def command_basic(message: types.Message):
	await try_except(message)


# @dp.message_handler()
async def basic_send(message: types.Message):
	if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}.intersection(set(json.load(open('cenz.json')))) != set():
		await message.reply('Маты запрещены! Будьте вежливы!')
		await message.delete()
	else:
		await global_handler(message)


# @dp.message_handler(commands=['Меню'])
# async def pizza_menu_command(message: types.Message):
#     for ret in cur.execute('SELECT * FROM menu').fetchall():
#         await bot.send_photo(message.from_user.id, ret[0], F'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')


def register_handlers_client(dp: Dispatcher):
	dp.register_message_handler(command_start, commands=['start', 'help'])
	dp.register_message_handler(command_basic, commands=['z', 'p', 'h', 'ex', 'ad'])
	dp.register_message_handler(basic_send)
