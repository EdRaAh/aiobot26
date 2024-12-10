import logging

from aiogram import Dispatcher, Router
from confa import bot
router: Router = Router()

from handlers_comand import router as router_2
from handlers_game import router as router_3
from handler_images import router as router_1


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__file__)

#инициаллизируем объекты бота и диспетчера

dp = Dispatcher()
dp.include_router(router_1),
dp.include_router(router_2)
dp.include_router(router_3)

# Основной блок запуска бота
if __name__ == "__main__":
    try:
        dp.run_polling(bot)
    except Exception as e:
        logger.exception("An error occurred while running the bot:", exc_info=e)
