import logging
import random
from aiogram import Bot, Dispatcher
from aiogram import Router
from handlers import router
from confa import TOKEN

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

alphabet = 'abcdefghijklmnopqrstuvwxyz'

#инициаллизируем объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

users = {}

#кол-во попыток в игре
ATTEMPTS = 7

dp.include_router(router)

# Функция генерирует случайную букву от a-z
def get_random_letter() -> str:
    return chr(random.randint(ord('a'), ord('z')))




# Основной блок запуска бота
if __name__ == "__main__":
    try:
        dp.run_polling(bot)
    except Exception as e:
        logger.exception("An error occurred while running the bot:", exc_info=e)
