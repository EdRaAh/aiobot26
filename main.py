import logging
from aiogram import Bot, Dispatcher, Router
from confa import TOKEN
router: Router = Router()
from handlers import router
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__file__)

#инициаллизируем объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(router)

# Основной блок запуска бота
if __name__ == "__main__":
    try:
        dp.run_polling(bot)
    except Exception as e:
        logger.exception("An error occurred while running the bot:", exc_info=e)
