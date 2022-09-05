from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton  # , ReplyKeyboardRemove
from aiogram import types


class MyKeyboardButton:

	def __init__(self):
		self.buttons = [
			"Start",
			"Записаться",
			"Адрес",
			"Price",
			"Наши работы",
			"Наш сайт",
		]

	def get_markup(self):
		b = []
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		for button in self.buttons:
			b.append(types.KeyboardButton(button))
		markup.add(*b)
		return markup

	@staticmethod
	def get_inline_markup_one(text, url=None):
		markup = types.InlineKeyboardMarkup()
		button = types.InlineKeyboardButton(text=text, url=url)
		markup.add(button)
		return markup


# b1 = KeyboardButton('/Режим_работы')
# b2 = KeyboardButton('/Расположение')
# b3 = KeyboardButton('/Меню')
# b4 = KeyboardButton('Поделиться номером', request_contact=True)
# b5 = KeyboardButton('Отправить где я', request_location=True)

# kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
# kb_client.add(b1).add(b2).insert(b3)
# kb_client.row(b1, b2, b3)
# kb_client.add(b1).add(b2).add(b3)#.row(b4, b5)
