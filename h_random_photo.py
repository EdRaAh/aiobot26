import os
import random
import logging
from aiogram.types import FSInputFile
from aiogram import Router
from aiogram.types import Message

logger = logging.getLogger(__file__)
router: Router = Router()

@router.message(lambda x: x.text.lower() in ['хочу фото', 'want photo','send photo'])
async def send_photo_handler(message:Message):
    logger.info(f"получена команда /send_photo от пользователя {message.from_user.id}")
    folder_path = 'cats'  # path to cats
    try:
        photos = os.listdir(folder_path)

        if not photos:
            await message.answer("в папке нет фото")
            return
        random_photo = random.choice(photos)
        photo_path = os.path.join(folder_path, random_photo)
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo=photo)
    except FileNotFoundError:
        await message.answer("папка с фото не найдена")
    except Exception as e:
        await message.answer(f"произошла ошибка: {str(e)}")
