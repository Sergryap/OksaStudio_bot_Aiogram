import json
import string
import asyncio

from aiogram import types, Dispatcher
from create_bot import dp
from .global_handler import global_handler


# @dp.message_handler()
async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}.intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('Маты запрещены!')
        await message.delete()
    else:
        await asyncio.create_task(global_handler(message))


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
