import asyncio
import json
import os
from aiogram.types import Message
from aiogram import Router, F
from confa import logger

router: Router = Router()

photo_ids: list = []  # Список для хранения photo_id
@router.message(F.photo)
async def handler_photo(message: Message):
    logger.info(f"получено фото: {message.photo[-1].file_id}")
    photo_ids.append(message.photo[-1].file_id)
    await write_ids_to_file(photo_ids)  # Сохраняем ID сразу после добавления

print(f'1 из папки h_extract_ids:/n {photo_ids}')

async def write_ids_to_file(photos_ids):
        # Проверяем, существует ли файл
    if os.path.exists('list_ids.json'):
            # Читаем существующие данные из файла
        with open('list_ids.json','r') as file:
            try:
                photos_ids = json.load(file)
            except json.JSONDecodeError:
                    photos_ids = []
    else:
            photos_ids = []
    # добавляем новые id в список photos_ids
    for photo_id in photo_ids:
        if photo_id not in photos_ids:
            photos_ids.append(photo_id)

            # Сохраняем обновленный список в файл
    with open('list_ids.json', 'w') as file:
        json.dump(photos_ids, file, indent=4)

print(f'2 из папки h_extract_ids:/n {photo_ids}')
async def main():
            # Пишем ID в файл
    await write_ids_to_file(photo_ids)

            # Запускаем основную функцию
 #  if __name__ == "__main__":
 #     asyncio.run(main())