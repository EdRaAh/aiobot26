import os
import random
from aiogram.types import InputFile
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router: Router = Router()
@router.message(Command(commands=['send_photo']))  # отправка фото в ответ на команду '/send_photo'
async def send_photo_handler(message:Message):
    folder_path = 'cats'  # path to cats
    try:
        photos = os.listdir(folder_path)
        if not photos:
            await message.answer("в папке нет фото")
            return
        random_photo = random.choice(photos)
        photo_path = os.path.join(folder_path, random_photo)
        photo = InputFile(photo_path)
        await message.answer_photo(photo=photo)
    except FileNotFoundError:
        await message.answer("папка с фото не найдена")
    except Exception as e:
        await message.answer(f"произошла ошибка: {str(e)}")

'''
images_folder: str = 'cats'  # путь к папке с фото


if not os.path.exists(images_folder) or not os.listdir(images_folder):
    raise FileNotFoundError(f"The folder '{images_folder}' does not exist or is empty.")
images = os.listdir(images_folder)

async def send_image(chat_id:int, caption:str):
    try:
        random_image = random.choice(images)
        image_path = os.path.join(images_folder, random_image) #полный путь
        photo = InputFile(file = image_path)
        #with open(image_path, 'rb') as photo:
        await bot.send_photo(chat_id, photo=photo, caption=caption)

    except Exception as e:
        logger.error('Failed to send photo: %s', str(e))

'''