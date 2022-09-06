import time
from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin
from requests import RequestException


async def on_startup(_):
    print('Бот вышел в онлайн')

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except RequestException:
        time.sleep(10)
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

