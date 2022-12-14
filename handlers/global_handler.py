from create_bot import bot
from aiogram import types
import asyncio
import string
from TgUser import TgUser
from datetime import datetime

users = {}
count = 0


async def get_context(message: types.Message):
	"""
	Получение контекста для передачи в класс пользователя
	"""
	msg = message.text.split('@')[0] if message.text[0] == '/' else message.text
	return {
		'from_user': {
			'username': message.from_user.username,
			'first_name': message.from_user.first_name
		},
		# 'text': message.text.lower().replace('''"''', '').replace("""'""", '').replace(r'/', ''),
		'text': msg.lower().translate(str.maketrans('', '', string.punctuation)),
		'chat_id': message.from_user.id
	}


async def users_update(user, message: types.Message, user_class):
	"""
	Добавление экземпляра класса пользователя в глобальный словарь для повторного использования
	"""
	global users
	users.update({
		f'user_{user}': {'user_class': user_class, 'time_create': message.date}
	})
	if len(users) == 50:
		min_date = min([users[user]['time_create'] for user in users])
		user_delete = [user for user in users if users[user]['time_create'] == min_date][0]
		del users[user_delete]


async def global_handler(message: types.Message):
	"""
	Обработка сообщений пользователя
	"""
	global users
	user = message.from_user.username
	context = await get_context(message)
	if f'user_{user}' not in users:
		exec(f"user_{user} = TgUser(context={context})")
		await users_update(user, message, user_class=eval(f"user_{user}"))
		await eval(f"user_{user}.handler_msg()")
	else:
		users[f'user_{user}']['user_class'].msg = context['text']
		await users[f'user_{user}']['user_class'].handler_msg()
		users[f'user_{user}']['user_class'].msg_previous = context['text']
