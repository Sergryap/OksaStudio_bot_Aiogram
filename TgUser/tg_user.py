from create_bot import bot
from aiogram import types
import asyncio
import re
import time
import random

from .photos import photos
from keyboards import MyKeyboardButton
from .verify_msg import VerifyMsg


class TgUser(MyKeyboardButton, VerifyMsg):

	bot = bot
	"""
	Основной класс взаимодействия пользователя и бота
	"""

	COMMAND = f"""
	✔️ Помочь записатьcя - "z"
	✔️️ Сориентировать по ценам - "p"
	✔️️ Помочь найти нас - "h"
	✔️️ Показать наши работы - "ex"
	✔️️ Связаться с администрацией - "ad"
	✔️️ Начать с начала - "start"
	"""

	VERIFY_FUNC = {
		'verify_address': 'send_address',
		'verify_entry': 'send_link_entry',
		'verify_price': 'send_price',
		'verify_contact_admin': 'send_contact_admin',
		'verify_thank_you': 'send_bay_bay',
		'verify_our_site': 'send_site',
		'verify_work_example': 'send_work_example',
	}

	def __init__(self, context):
		super().__init__()
		self.username = context.get('from_user').get('username')
		self.first_name = context.get('from_user').get('first_name', self.username)
		self.chat_id = context.get('chat_id')
		self.msg = context.get('text')
		self.msg_previous = context.get('text')
		self.users_admin = [1642719191]  # администраторы
		self.markup = self.get_markup()

	async def send_message_to_admins(self, msg=None):
		msg = f'Сообщение:\n "{self.msg}"\n от @{self.username}' if not msg else msg
		for user in self.users_admin:
			await self.bot.send_message(user, msg)

	async def handler_msg(self):
		"""Функция-обработчик сообщений пользователя"""
		if await self.verify_hello():
			await self.send_message_to_admins()
			return await self.send_hello()
		for verify, func in self.VERIFY_FUNC.items():
			if await eval(f'self.{verify}()'):
				await self.send_message_to_admins()
				return await eval(f'self.{func}()')
		await self.clarification()
		await self.send_message_to_admins()

	async def clarification(self):
		text = f"""
		{self.first_name}, я еще молодой бот и только учусь, поэтому уточните, пожалуйста что бы выхотели, отправив одну из команд:\n
		{self.COMMAND} 
		"""
		await self.bot.send_message(self.chat_id, text)

	async def send_hello(self):

		def good_time():
			tm = time.ctime()
			pattern = re.compile(r"(\d+):\d+:\d+")
			h = int(pattern.search(tm).group(1))
			h = h + 5 if h < 19 else (h + 5) // 24
			if h < 6:
				return "Доброй ночи"
			elif h < 11:
				return "Доброе утро"
			elif h < 18:
				return "Добрый день"
			elif h <= 23:
				return "Добрый вечер"

		d = [
			'\nНапишите, что бы вы хотели или выберите выше.',
			'\nНапишите мне, что вас интересует или выберите выше.',
			'\nЧто вас интересует? Напишите пожалуйста или выберите выше.'
		]

		t = f"""
		Пока менеджеры {'спят' if good_time() == 'Доброй ночи' else 'заняты'} я могу:
		{self.COMMAND}
		"""

		delta = random.choice(d) if await self.verify_only_hello() else ''
		t1 = f"{good_time()}, {self.first_name}!\nЯ бот Oksa-studio.\nБуду рад нашему общению.\n{t}{delta}"
		t2 = f"{good_time()}, {self.first_name}!\nЯ чат-бот Oksa-studio.\nОчень рад видеть Вас у нас.\n{t}{delta}"
		t3 = f"{good_time()}, {self.first_name}!\nЯ бот этого чата.\nРад видеть Вас у нас в гостях.\n{t}{delta}"
		await self.bot.send_message(self.chat_id, random.choice([t1, t2, t3]), reply_markup=self.markup)

	async def send_link_entry(self):
		markup = self.get_inline_markup_one(text="ON-LINE ЗАПИСЬ", url='https://dikidi.net/72910')
		text = f"""
		{self.first_name}, узнать о свободных местах, своих записях и/или записаться можно:\n
		✔️ Самостоятельно: <a href="https://dikidi.net/72910">ON-LINE</a>
		✔️ По тел. +7(919)442-35-36
		✔️ Через личные сообщения: @oksarap (Оксана)
		✔ Дождаться сообщения от нашего менеджера\n
		Что вас еще интересует напишите или выберите ниже:
		{self.COMMAND}
		"""
		await self.bot.send_message(self.chat_id, text, parse_mode="HTML", reply_markup=markup)

	async def send_price(self):
		markup = self.get_inline_markup_one(text="СМОТРЕТЬ PRICE", url="https://vk.com/uslugi-142029999")
		text = f"""		
		{self.first_name}, цены на наши услуги можно посмотреть здесь: ️<a href="https://vk.com/uslugi-142029999">PRICE</a>\n		
		Что вас еще интересует напишите или выберите ниже:
		{self.COMMAND}
		"""
		await self.bot.send_message(self.chat_id, text, parse_mode="HTML", reply_markup=markup)

	async def send_contact_admin(self):
		text = f"""
		{self.first_name}, мы обязательно свяжемся с Вами в ближайшее время.
		Кроме того, для связи с руководством Вы можете воспользоваться следующими контактами:
		✔ @oksarap (чат администратора)
		✔ https://vk.com/id448564047
		✔ https://vk.com/id9681859
		✔ Email: oksarap@mail.ru
		✔ Тел.: +7(919)442-35-36\n
		Что вас еще интересует напишите или выберите ниже:
		{self.COMMAND}	
		"""
		await self.bot.send_message(self.chat_id, text, reply_markup=self.markup)

	async def send_site(self):
		markup = self.get_inline_markup_one(text="НАШ САЙТ", url='https://oksa-studio.ru/')
		text = f"""
		{self.first_name}, много полезной информации о наращивании ресниц смотрите на нашем сайте:
		https://oksa-studio.ru/
		\nЧто вас еще интересует напишите или выберите ниже.\n
		{self.COMMAND}
		"""
		await self.bot.send_message(self.chat_id, text, reply_markup=markup)

	async def send_address(self):
		text1 = f"""
		{self.first_name}, мы находимся по адресу:\n
		📍 г.Пермь, ул.Тургенева, д.23.\n
		"""
		text2 = f"""
		Это малоэтажное кирпичное здание слева от ТЦ "Агат" 
		Вход через "Идеал-Лик", большой стеклянный тамбур\n
		Что вас еще интересует напишите или выберите ниже.\n
		{self.COMMAND}	
		"""
		await self.bot.send_message(
				self.chat_id,
				'<a href="https://vk.com/photo-195118308_457239030">Вход</a>',
				parse_mode="HTML"
			)
		await self.bot.send_message(
			self.chat_id,
			'<a href="https://vk.com/photo-142029999_457243624">На карте</a>',
			parse_mode="HTML"
		)
		await self.bot.send_message(self.chat_id, text1)
		await self.bot.send_message(self.chat_id, text2, reply_markup=self.markup)

	async def send_bay_bay(self):
		text1 = f"До свидания, {self.first_name}. Будем рады видеть вас снова!"
		text2 = f"До скорых встреч, {self.first_name}. Было приятно с Вами пообщаться. Ждём вас снова!"
		text3 = f"Всего доброго Вам, {self.first_name}. Надеюсь мы ответили на Ваши вопросы. Ждём вас снова! До скорых встреч."
		text = random.choice([text1, text2, text3])
		await self.bot.send_message(self.chat_id, text, reply_markup=self.markup)

	async def send_work_example(self):
		text = f"""
		{self.first_name}, больше работ здесь:
		vk.com/albums-142029999
		Что вас еще интересует напишите или выберите ниже.\n
		{self.COMMAND}
		"""
		await self.send_photo()
		await self.bot.send_message(self.chat_id, text, reply_markup=self.markup)

	async def send_photo(self, photo_id=None, n=5):
		attachment = photo_id if photo_id else await self.get_photos_example(n)
		markup = self.get_inline_markup_one(text="БОЛЬШЕ РАБОТ", url='https://vk.com/albums-142029999/')
		for i, photo in enumerate(attachment, start=1):
			if i == n:
				await self.bot.send_message(
					self.chat_id,
					f'<a href="{photo}">Наши работы</a>',
					parse_mode="HTML",
					reply_markup=markup
				)
			else:
				await self.bot.send_message(
					self.chat_id,
					f'<a href="{photo}">Наши работы</a>',
					parse_mode="HTML"
				)

	@staticmethod
	async def get_photos_example(n):
		attachment = []
		for photo in random.sample(photos, n):
			attachment.append(f"https://vk.com/{photo}")
		return attachment
